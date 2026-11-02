"""Kerangka run.py Monica Patricia Tanjung (123450073)
Jalur: Autoencoder (Temporal Denoising Autoencoder + Regresi Repetisi)
Kasus: Penghitung Repetisi Peregangan Meja Kerja (10 fps, 190 frame, 36 fitur)
Tugas Sampingan: Penguji Purwarupa & Optimasi ONNX
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

NIM = "123450073"
JALUR = "ae"


def latih_dan_prediksi(seed: int, final: bool) -> tuple[np.ndarray, np.ndarray | None]:
    """Model Autoencoder Bottleneck Representation + Regresi Repetisi."""
    np.random.seed(seed)
    Xtr, ytr, Xva, _, Xte, _ = data.muat()

    try:
        import torch
        import torch.nn as nn

        torch.manual_seed(seed)

        class TemporalAE(nn.Module):
            def __init__(self, in_features=36, latent_dim=16):
                super().__init__()
                # Encoder
                self.encoder = nn.Sequential(
                    nn.Linear(in_features, 24),
                    nn.ReLU(),
                    nn.Linear(24, latent_dim)
                )
                # Decoder
                self.decoder = nn.Sequential(
                    nn.Linear(latent_dim, 24),
                    nn.ReLU(),
                    nn.Linear(24, in_features)
                )
                # Regressor dari representasi laten
                self.regressor = nn.Sequential(
                    nn.Linear(latent_dim, 16),
                    nn.ReLU(),
                    nn.Linear(16, 1)
                )

            def forward(self, x):
                # x: [Batch, T, C]
                latent = self.encoder(x)  # [Batch, T, Latent]
                recon = self.decoder(latent)
                # Pooling representasi laten atas langkah waktu
                pooled_latent = torch.mean(latent, dim=1)
                pred = self.regressor(pooled_latent).squeeze(-1)
                return recon, pred

        model = TemporalAE(in_features=Xtr.shape[-1], latent_dim=16)
        optimizer = torch.optim.Adam(model.parameters(), lr=0.005, weight_decay=1e-4)

        t_Xtr = torch.tensor(Xtr, dtype=torch.float32)
        t_ytr = torch.tensor(ytr, dtype=torch.float32)
        t_Xva = torch.tensor(Xva, dtype=torch.float32)

        model.train()
        for _ in range(40):
            optimizer.zero_grad()
            recon, pred = model(t_Xtr)
            loss_recon = nn.functional.mse_loss(recon, t_Xtr)
            loss_pred = nn.functional.l1_loss(pred, t_ytr)
            loss = loss_recon + loss_pred
            loss.backward()
            optimizer.step()

        model.eval()
        with torch.no_grad():
            _, pred_val = model(t_Xva)
            pred_val = pred_val.numpy()
            pred_test = None
            if final and Xte is not None:
                _, pred_test = model(torch.tensor(Xte, dtype=torch.float32))
                pred_test = pred_test.numpy()

    except ImportError:
        # Fallback NumPy PCA/SVD Bottleneck Features + Ridge
        def ae_latent_extractor(X: np.ndarray, k: int = 8) -> np.ndarray:
            N, T, C = X.shape
            X_flat = X.reshape(N, -1)
            # SVD basis
            u, s, vt = np.linalg.svd(X_flat, full_matrices=False)
            latent = u[:, :k] * s[:k]
            return latent.astype(np.float32)

        Xtr_l = ae_latent_extractor(Xtr, k=8)
        Xva_l = ae_latent_extractor(Xva, k=8)
        Xb = np.hstack([Xtr_l, np.ones((len(Xtr_l), 1), dtype=np.float32)])
        A = Xb.T @ Xb + 4.0 * np.eye(Xb.shape[1], dtype=np.float32)
        w = np.linalg.solve(A, Xb.T @ ytr.astype(np.float32))

        pred_val = (np.hstack([Xva_l, np.ones((len(Xva_l), 1), dtype=np.float32)]) @ w).astype(np.float32)
        pred_test = None
        if final and Xte is not None:
            Xte_l = ae_latent_extractor(Xte, k=8)
            pred_test = (np.hstack([Xte_l, np.ones((len(Xte_l), 1), dtype=np.float32)]) @ w).astype(np.float32)

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
