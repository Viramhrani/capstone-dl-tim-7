"""Kerangka run.py Arya Muda Siregar (123450063)
Jalur: RNN (LSTM/GRU untuk Deret Waktu Pose Sendi)
Kasus: Penghitung Repetisi Peregangan Meja Kerja (10 fps, 190 langkah waktu, 36 fitur pose)
Tugas Sampingan: Penjaga Data & Evaluasi
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
from src.protokol import data

NIM = "123450063"
JALUR = "rnn"


def latih_dan_prediksi(seed: int, final: bool) -> tuple[np.ndarray, np.ndarray | None]:
    """Model Sekuensial RNN/GRU untuk memprediksi jumlah repetisi peregangan."""
    np.random.seed(seed)
    Xtr, ytr, Xva, _, Xte, _ = data.muat()

    try:
        import torch
        import torch.nn as nn

        torch.manual_seed(seed)

        class PoseGRU(nn.Module):
            def __init__(self, in_features=36, hidden_dim=48, num_layers=2):
                super().__init__()
                self.gru = nn.GRU(
                    input_size=in_features,
                    hidden_size=hidden_dim,
                    num_layers=num_layers,
                    batch_first=True,
                    bidirectional=True,
                    dropout=0.2 if num_layers > 1 else 0.0
                )
                self.regressor = nn.Sequential(
                    nn.Linear(hidden_dim * 2, 32),
                    nn.ReLU(),
                    nn.Dropout(0.2),
                    nn.Linear(32, 1)
                )

            def forward(self, x):
                out, _ = self.gru(x)
                out = torch.mean(out, dim=1)  # temporal pooling
                return self.regressor(out).squeeze(-1)

        model = PoseGRU(in_features=Xtr.shape[-1])
        optimizer = torch.optim.Adam(model.parameters(), lr=0.003, weight_decay=1e-4)
        criterion = nn.L1Loss()

        t_Xtr = torch.tensor(Xtr, dtype=torch.float32)
        t_ytr = torch.tensor(ytr, dtype=torch.float32)
        t_Xva = torch.tensor(Xva, dtype=torch.float32)

        model.train()
        for _ in range(40):
            optimizer.zero_grad()
            out = model(t_Xtr)
            loss = criterion(out, t_ytr)
            loss.backward()
            optimizer.step()

        model.eval()
        with torch.no_grad():
            pred_val = model(t_Xva).numpy()
            pred_test = model(torch.tensor(Xte, dtype=torch.float32)).numpy() if final and Xte is not None else None

    except ImportError:
        # Fallback NumPy Recurrent Cumulative Dynamics
        def rnn_feature_extractor(X: np.ndarray) -> np.ndarray:
            N, T, C = X.shape
            feats = []
            for i in range(N):
                h = np.zeros(C, dtype=np.float32)
                h_seq = []
                for t in range(T):
                    h = 0.8 * h + 0.2 * np.tanh(X[i, t])
                    h_seq.append(h)
                h_arr = np.array(h_seq)
                feats.append(np.hstack([h_arr.mean(axis=0), h_arr.std(axis=0)]))
            return np.array(feats, dtype=np.float32)

        Xtr_f = rnn_feature_extractor(Xtr)
        Xva_f = rnn_feature_extractor(Xva)
        Xb = np.hstack([Xtr_f, np.ones((len(Xtr_f), 1), dtype=np.float32)])
        A = Xb.T @ Xb + 5.0 * np.eye(Xb.shape[1], dtype=np.float32)
        w = np.linalg.solve(A, Xb.T @ ytr.astype(np.float32))

        pred_val = (np.hstack([Xva_f, np.ones((len(Xva_f), 1), dtype=np.float32)]) @ w).astype(np.float32)
        pred_test = None
        if final and Xte is not None:
            Xte_f = rnn_feature_extractor(Xte)
            pred_test = (np.hstack([Xte_f, np.ones((len(Xte_f), 1), dtype=np.float32)]) @ w).astype(np.float32)

    return pred_val, pred_test


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--final", action="store_true")
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
