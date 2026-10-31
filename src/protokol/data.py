"""Pemuat data kasus tim — MILIK TIM, dibekukan setelah Sprint 0 dengan persetujuan pembimbing.

Kasus Tim 7: Penghitung repetisi peregangan meja kerja
Tugas: Regresi (penghitungan jumlah repetisi pose urutan 10 fps)
Batasan:
1. 1 detik pertama (10 frame) dibuang.
2. Data uji dipisah berdasarkan partisipan (P07 & P08 untuk data uji holdout).
3. Data validasi dipisahkan per grup partisipan (P06 untuk validasi, P01-P05 untuk latih).
4. Normalisasi fitur hanya dihitung dari data latih (mencegah data leakage).
"""
from __future__ import annotations

import numpy as np

from src.common import manifest, split

TUGAS = "regresi"


def muat():
    """Memuat dataset peregangan meja kerja sesuai protokol Tim 7."""
    manifest.baca()
    jalur_data = manifest.AKAR / "data" / "peregangan_meja.npz"
    if not jalur_data.exists():
        raise FileNotFoundError(f"Berkas dataset {jalur_data} tidak ditemukan.")

    with np.load(jalur_data) as d:
        X_raw = d["X"].astype(np.float32)       # [64, 200, 36]
        y_raw = d["y"].astype(np.float32)       # [64]
        partisipan = d["partisipan"]            # [64]

    # Batasan 1: Buang 1 detik pertama (10 frame pertama pada 10 fps)
    X_trimmed = X_raw[:, 10:, :]  # [64, 190, 36]

    # Batasan 2: Pemisahan data uji per partisipan (P07, P08 untuk data uji holdout)
    mask_test = np.isin(partisipan, ["P07", "P08"])
    mask_val = np.isin(partisipan, ["P06"])
    mask_train = ~mask_test & ~mask_val

    X_train = X_trimmed[mask_train]
    y_train = y_raw[mask_train]

    X_val = X_trimmed[mask_val]
    y_val = y_raw[mask_val]

    X_test = X_trimmed[mask_test]
    y_test = y_raw[mask_test]

    # Batasan 3: Normalisasi dihitung HANYA dari data latih
    mu = X_train.mean(axis=(0, 1), keepdims=True)
    std = X_train.std(axis=(0, 1), keepdims=True) + 1e-6

    X_train = (X_train - mu) / std
    X_val = (X_val - mu) / std
    X_test = (X_test - mu) / std

    return X_train, y_train, X_val, y_val, X_test, y_test
