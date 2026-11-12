"""Model 1D-CNN untuk Penghitung Repetisi Peregangan Meja Kerja (Jalur Vira Putri Maharani - NIM: 122450129).

Jalur: CNN (1D Temporal Convolution + Adaptive Temporal Pooling + Regresi Repetisi)
Penggunaan:
    python models/122450129/run.py --seed 1
    python models/122450129/run.py --seed 2026 --final

Catatan metodologis:
- Model memakai 4 blok konvolusi 1D dengan dilation bertingkat untuk menangkap pola
  periodik pada runtun pose 10 fps.
- Global average pooling biasa membuang informasi jumlah siklus; karena itu output
  konvolusi dipertahankan ke 12 bin waktu sebelum diregresikan.
- Pemilihan checkpoint memakai validation MAE (early stopping). Data uji P07/P08
  hanya dipakai bila `--final` diberikan pada sprint terakhir.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import random
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

AKAR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(AKAR))
from src.protokol import data  # noqa: E402  (protokol tim yang dibekukan)

NIM = "122450129"
JALUR = "cnn"
EPOCHS = 140
PATIENCE = 30
BATCH = 8


class PoseCNN1D(nn.Module):
    """CNN temporal untuk regresi jumlah repetisi dari sequence pose [N, T, C]."""

    def __init__(self, in_channels: int, width: int = 24):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Conv1d(in_channels, width, kernel_size=5, padding=2),
            nn.BatchNorm1d(width),
            nn.ReLU(),
            nn.Conv1d(width, width, kernel_size=5, padding=4, dilation=2),
            nn.BatchNorm1d(width),
            nn.ReLU(),
            nn.Conv1d(width, width, kernel_size=5, padding=8, dilation=4),
            nn.BatchNorm1d(width),
            nn.ReLU(),
            nn.Conv1d(width, width, kernel_size=5, padding=16, dilation=8),
            nn.BatchNorm1d(width),
            nn.ReLU(),
        )
        # 12 bin waktu mempertahankan informasi jumlah siklus; Flatten setelah GAP
        # akan menghilangkan informasi tersebut.
        self.pool = nn.AdaptiveAvgPool1d(12)
        self.head = nn.Sequential(
            nn.Flatten(),
            nn.Linear(width * 12, 96),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(96, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # [N, T, C] -> [N, C, T] untuk Conv1d
        z = self.encoder(x.transpose(1, 2))
        z = self.pool(z)
        return self.head(z).squeeze(-1)


def augment(x: torch.Tensor) -> torch.Tensor:
    """Augmentasi ringan untuk 40 sampel latih: shift waktu, noise, channel dropout."""
    if random.random() < 0.8:
        shift = random.randint(-8, 8)
        if shift:
            x = torch.roll(x, shifts=shift, dims=1)
    if random.random() < 0.8:
        x = x + 0.008 * torch.randn_like(x)
    if random.random() < 0.5:
        mask = (torch.rand(x.shape[0], 1, x.shape[2], device=x.device) > 0.04).float()
        x = x * mask
    return x


def latih_dan_prediksi(seed: int, final: bool):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(max(1, min(4, os.cpu_count() or 1)))

    Xtr, ytr, Xva, yva, Xte, yte = data.muat()
    ymu = float(ytr.mean())
    ysd = float(ytr.std())

    Xtr_t = torch.tensor(Xtr, dtype=torch.float32)
    ytr_t = torch.tensor((ytr - ymu) / ysd, dtype=torch.float32)
    Xva_t = torch.tensor(Xva, dtype=torch.float32)
    Xte_t = torch.tensor(Xte, dtype=torch.float32) if Xte is not None else None

    model = PoseCNN1D(Xtr.shape[2])
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=EPOCHS)
    criterion = nn.L1Loss()  # selaras dengan metrik utama MAE

    best = {"mae": float("inf"), "state": None, "epoch": 0}
    tanpa_perbaikan = 0
    t0 = time.time()

    for epoch in range(1, EPOCHS + 1):
        model.train()
        urut = torch.randperm(len(Xtr_t))
        for i in range(0, len(Xtr_t), BATCH):
            idx = urut[i:i + BATCH]
            xb = augment(Xtr_t[idx].clone())
            yb = ytr_t[idx]

            optimizer.zero_grad()
            loss = criterion(model(xb), yb)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 2.0)
            optimizer.step()

        scheduler.step()

        model.eval()
        with torch.no_grad():
            pred_val = model(Xva_t).numpy() * ysd + ymu
        mae = float(np.abs(yva - pred_val).mean())

        if mae < best["mae"]:
            best.update(mae=mae, state=copy.deepcopy(model.state_dict()), epoch=epoch)
            tanpa_perbaikan = 0
        else:
            tanpa_perbaikan += 1
            if tanpa_perbaikan >= PATIENCE:
                break

    durasi = time.time() - t0
    model.load_state_dict(best["state"])
    model.eval()
    with torch.no_grad():
        pred_val = model(Xva_t).numpy() * ysd + ymu
        pred_test = None
        if final and Xte_t is not None:
            pred_test = model(Xte_t).numpy() * ysd + ymu

    print(f"CNN seed={seed}: best_epoch={best['epoch']} val_MAE={best['mae']:.4f} durasi={durasi:.1f}s")
    return pred_val, pred_test, best, durasi


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--final", action="store_true", help="sprint terakhir: evaluasi data uji sekali")
    ap.add_argument("--perangkat", default="cpu laptop")
    a = ap.parse_args()

    pred_val, pred_test, best, durasi = latih_dan_prediksi(a.seed, a.final)
    out = AKAR / "results" / NIM
    out.mkdir(parents=True, exist_ok=True)
    np.save(out / "pred_val.npy", np.asarray(pred_val))

    perintah = [
        sys.executable, "-m", "src.common.evaluate",
        "--nim", NIM, "--model", JALUR, "--seed", str(a.seed),
        "--pred-val", str(out / "pred_val.npy"),
        "--durasi", f"{durasi:.1f}", "--perangkat", a.perangkat,
    ]
    if pred_test is not None:
        np.save(out / "pred_test.npy", np.asarray(pred_test))
        perintah += ["--pred-test", str(out / "pred_test.npy")]

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    subprocess.run(perintah, check=True, cwd=AKAR, env=env)

    log = {
        "model": "cnn",
        "nim": NIM,
        "seed": a.seed,
        "arsitektur": "4 x Conv1d + BatchNorm + ReLU (dilation 1,2,4,8) + AdaptiveAvgPool1d(12) + MLP",
        "epoch_maks": EPOCHS,
        "patience": PATIENCE,
        "best_epoch": best["epoch"],
        "best_val_mae": round(float(best["mae"]), 6),
        "durasi_detik": round(float(durasi), 1),
        "catatan": "Checkpoint terbaik dipilih dari validation MAE; data uji P07/P08 tidak dipakai pada Sprint 1.",
    }
    (out / "training_log.json").write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
