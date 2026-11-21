"""Uji asap kerangka CNN pada data simulasi (Backlog #12).

Skrip ini membuat dataset simulasi 64 kondisi (8 partisipan x 8 kondisi),
200 frame x 36 fitur pose, lalu menjalankan ``models/122450129/run.py``
di salinan sementara repositori. Data asli di ``data/`` dan hasil asli di
``results/`` tidak disentuh.

Penggunaan:
    python models/122450129/uji_simulasi.py
    python models/122450129/uji_simulasi.py --keep   # simpan direktori sementara
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

AKAR = Path(__file__).resolve().parents[2]
NIM = "122450129"


def buat_data_simulasi(root: Path, seed: int = 1007) -> None:
    """Membuat NPZ sintetis dengan skema yang sama seperti data primer tim."""
    rng = np.random.default_rng(seed)
    n, t, c = 64, 200, 36
    partisipan = np.repeat([f"P{i:02d}" for i in range(1, 9)], 8)
    y = np.tile(
        np.array([8.9, 10.0, 11.1, 12.2, 13.3, 14.4, 15.5, 16.4], dtype=np.float32),
        8,
    )
    y_kelas = np.tile(np.arange(4, dtype=np.int64), 16)
    waktu = np.arange(t, dtype=np.float32) / 10.0
    X = np.empty((n, t, c), dtype=np.float32)

    for i in range(n):
        # Satu siklus penuh per repetisi: target 8,9-16,4 repetisi per 19 detik.
        frekuensi = float(y[i]) / 19.0
        for kanal in range(c):
            fase = (kanal % 6) * 0.7
            amplitudo = 0.5 + 0.03 * (kanal % 9)
            X[i, :, kanal] = (
                amplitudo * np.sin(2 * np.pi * frekuensi * waktu + fase)
                + 0.2 * np.sin(4 * np.pi * frekuensi * waktu + fase / 2)
                + 0.03 * rng.normal(size=t)
            )

    (root / "data").mkdir(parents=True, exist_ok=True)
    np.savez(
        root / "data" / "peregangan_meja.npz",
        X=X,
        y=y,
        y_kelas=y_kelas,
        partisipan=partisipan,
    )
    manifest = {
        "sumber": "simulasi lokal untuk uji kerangka CNN",
        "berkas": ["data/peregangan_meja.npz"],
        "catatan": "64 kondisi, 8 partisipan, 200 frame, 36 fitur; data sintetis.",
    }
    (root / "data" / "MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def siapkan_salinan(root: Path) -> None:
    """Menyalin src/ dan run.py ke direktori sementara."""
    shutil.copytree(
        AKAR / "src",
        root / "src",
        ignore=shutil.ignore_patterns("__pycache__"),
    )
    tujuan = root / "models" / NIM
    tujuan.mkdir(parents=True, exist_ok=True)
    shutil.copy2(AKAR / "models" / NIM / "run.py", tujuan / "run.py")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep", action="store_true", help="simpan direktori sementara")
    a = ap.parse_args()

    root = Path(tempfile.mkdtemp(prefix="cnn_simulasi_"))
    sukses = False
    try:
        siapkan_salinan(root)
        buat_data_simulasi(root)

        env = os.environ.copy()
        env["PYTHONUTF8"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"
        perintah = [sys.executable, "models/122450129/run.py", "--seed", "1"]
        print("$", " ".join(perintah))
        hasil = subprocess.run(
            perintah,
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=600,
        )
        print(hasil.stdout.replace("→", "->").strip())
        if hasil.returncode != 0:
            raise SystemExit(
                "run.py gagal (kode "
                f"{hasil.returncode}):\n{hasil.stderr.replace('→', '->').strip()}"
            )

        metrik_path = root / "results" / NIM / "metrics.json"
        log_path = root / "results" / NIM / "training_log.json"
        pred_path = root / "results" / NIM / "pred_val.npy"
        for jalur in (metrik_path, log_path, pred_path):
            if not jalur.exists():
                raise SystemExit(f"artefak tidak dibuat: {jalur}")

        metrics = json.loads(metrik_path.read_text(encoding="utf-8"))
        log = json.loads(log_path.read_text(encoding="utf-8"))
        pred = np.load(pred_path)

        assert metrics["seed"] == 1
        assert metrics["model"] == "cnn"
        assert metrics["n_val"] == 8
        assert metrics["n_test"] == 0
        assert len(metrics["data_hash"]) == 32
        assert {"val_mae", "val_rmse", "val_r2"} <= set(metrics["metrik"])
        assert log["best_epoch"] >= 1
        assert pred.shape == (8,)

        print(
            "PASS uji simulasi: "
            f"val_MAE={metrics['metrik']['val_mae']:.6f} "
            f"val_RMSE={metrics['metrik']['val_rmse']:.6f} "
            f"val_R2={metrics['metrik']['val_r2']:.6f} "
            f"best_epoch={log['best_epoch']} "
            f"pred_shape={pred.shape} "
            f"data_hash={metrics['data_hash']}"
        )
        sukses = True
    finally:
        if sukses and not a.keep:
            shutil.rmtree(root, ignore_errors=True)
        else:
            print("Direktori uji:", root)


if __name__ == "__main__":
    main()
