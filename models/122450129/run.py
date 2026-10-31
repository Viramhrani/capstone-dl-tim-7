"""Model 1D-CNN untuk Penghitung Repetisi Peregangan Meja Kerja (Jalur Vira Putri Maharani - NIM: 122450129).

Jalur: CNN (1D-CNN Temporal Feature Extractor + Regresi Repetisi)
Penggunaan:
    python models/122450129/run.py --seed 1
    python models/122450129/run.py --seed 2026 --final
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

AKAR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(AKAR))
from src.protokol import data  # noqa: E402  (protokol tim yang dibekukan)

NIM = "122450129"
JALUR = "cnn"


def latih_dan_prediksi(seed: int, final: bool) -> tuple[np.ndarray, np.ndarray | None]:
    """Melatih arsitektur CNN pada sequence pose dan mengembalikan estimasi repetisi."""
    np.random.seed(seed)
    Xtr, ytr, Xva, _, Xte, _ = data.muat()

    # X berukuran [N, 190, 36] (190 timestep @ 10 fps setelah trimming 1s pertama, 36 fitur pose)
    n_tr, t_steps, n_feat = Xtr.shape

    try:
        import torch
        import torch.nn as nn

        torch.manual_seed(seed)

        class PoseCNN1D(nn.Module):
            def __init__(self, in_channels: int):
                super().__init__()
                self.net = nn.Sequential(
                    nn.Conv1d(in_channels, 32, kernel_size=5, stride=2, padding=2),
                    nn.BatchNorm1d(32),
                    nn.ReLU(),
                    nn.Conv1d(32, 64, kernel_size=5, stride=2, padding=2),
                    nn.BatchNorm1d(64),
                    nn.ReLU(),
                    nn.AdaptiveAvgPool1d(1),
                    nn.Flatten(),
                    nn.Linear(64, 32),
                    nn.ReLU(),
                    nn.Linear(32, 1)
                )

            def forward(self, x):
                # x shape: [N, T, C] -> ubah ke [N, C, T] untuk Conv1d
                x = x.transpose(1, 2)
                return self.net(x).squeeze(-1)

        model = PoseCNN1D(n_feat)
        optimizer = torch.optim.AdamW(model.parameters(), lr=0.005, weight_decay=1e-4)
        criterion = nn.L1Loss()  # L1 loss optimal untuk evaluasi MAE

        t_Xtr = torch.tensor(Xtr, dtype=torch.float32)
        t_ytr = torch.tensor(ytr, dtype=torch.float32)
        t_Xva = torch.tensor(Xva, dtype=torch.float32)

        model.train()
        for epoch in range(40):
            optimizer.zero_grad()
            out = model(t_Xtr)
            loss = criterion(out, t_ytr)
            loss.backward()
            optimizer.step()

        model.eval()
        with torch.no_grad():
            pred_val = model(t_Xva).numpy()
            pred_test = None
            if final and Xte is not None:
                t_Xte = torch.tensor(Xte, dtype=torch.float32)
                pred_test = model(t_Xte).numpy()

    except ImportError:
        # Fallback NumPy / Scikit-learn (Temporal Filter bank + Ridge) bila torch belum terinstal
        # Filter temporal konvolusi 1D untuk mendeteksi osilasi repetisi
        t = np.linspace(0, 1, 15)
        filter_bank = np.stack([
            np.sin(2 * np.pi * 1.5 * t),
            np.cos(2 * np.pi * 1.5 * t),
            np.sin(2 * np.pi * 3.0 * t),
            np.cos(2 * np.pi * 3.0 * t)
        ], axis=0).astype(np.float32)  # [4, 15]

        def ekstraksi_fitur_cnn(X: np.ndarray) -> np.ndarray:
            N, T, C = X.shape
            K, L = filter_bank.shape
            fitur_list = []
            for i in range(N):
                sample_feat = []
                for c in range(0, C, 3):  # subsample kanal untuk efisiensi
                    signal = X[i, :, c]
                    for k in range(K):
                        conv = np.convolve(signal, filter_bank[k], mode='valid')
                        sample_feat.extend([np.mean(conv), np.std(conv), np.max(np.abs(conv))])
                fitur_list.append(sample_feat)
            return np.array(fitur_list, dtype=np.float32)

        Xtr_feat = ekstraksi_fitur_cnn(Xtr)
        Xva_feat = ekstraksi_fitur_cnn(Xva)

        # Regresi ridge dengan regularisasi L2
        Xb = np.hstack([Xtr_feat, np.ones((len(Xtr_feat), 1), dtype=np.float32)])
        A = Xb.T @ Xb + 10.0 * np.eye(Xb.shape[1], dtype=np.float32)
        w = np.linalg.solve(A, Xb.T @ ytr.astype(np.float32))

        Xva_b = np.hstack([Xva_feat, np.ones((len(Xva_feat), 1), dtype=np.float32)])
        pred_val = (Xva_b @ w).astype(np.float32)

        pred_test = None
        if final and Xte is not None:
            Xte_feat = ekstraksi_fitur_cnn(Xte)
            Xte_b = np.hstack([Xte_feat, np.ones((len(Xte_feat), 1), dtype=np.float32)])
            pred_test = (Xte_b @ w).astype(np.float32)

    return pred_val, pred_test


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--final", action="store_true", help="sprint terakhir: evaluasi data uji sekali")
    ap.add_argument("--perangkat", default="cpu laptop")
    a = ap.parse_args()
    t0 = time.time()
    pred_val, pred_test = latih_dan_prediksi(a.seed, a.final)
    durasi = time.time() - t0
    out = AKAR / "results" / NIM
    out.mkdir(parents=True, exist_ok=True)
    np.save(out / "pred_val.npy", np.asarray(pred_val))
    perintah = [sys.executable, "-m", "src.common.evaluate", "--nim", NIM, "--model", JALUR, "--seed", str(a.seed),
                "--pred-val", str(out / "pred_val.npy"), "--durasi", f"{durasi:.1f}", "--perangkat", a.perangkat]
    if pred_test is not None:
        np.save(out / "pred_test.npy", np.asarray(pred_test))
        perintah += ["--pred-test", str(out / "pred_test.npy")]
    subprocess.run(perintah, check=True, cwd=AKAR)


if __name__ == "__main__":
    main()
