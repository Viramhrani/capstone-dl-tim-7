"""Alat Bantu Validasi & Ekspor `data/repetisi.csv` — Backlog #6 (Arya Muda Siregar, 123450063).

Skrip ini TIDAK mengubah dataset mentah dan TIDAK mengarang angka repetisi.
Setelah Arya mengisi kolom `jumlah_hitung_ulang` pada `b06_template_repetisi_64_kondisi.csv`
berdasarkan pengamatan visual urutan foto kamera sesi 16 Nov, jalankan skrip ini untuk:
1. Memvalidasi tidak ada nilai kosong, duplikat nomor kondisi, atau angka tidak wajar.
2. Mengekspor berkas bersih dua kolom (`no,jumlah`) ke berkas target (default: `b06_repetisi_tervalidasi.csv`;
   tambahkan `--salin-ke-repo` bila sudah siap menyalin ke `data/repetisi.csv`).

Penggunaan (dari root repository):
    python sprint/sprint-1/artefak/b06_validasi_dan_ekspor_repetisi.py --uji-diri
    python sprint/sprint-1/artefak/b06_validasi_dan_ekspor_repetisi.py
    python sprint/sprint-1/artefak/b06_validasi_dan_ekspor_repetisi.py --salin-ke-repo
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

FOLDER_INI = Path(__file__).resolve().parent
REPO_DATA_OUT = FOLDER_INI.parents[2] / "data" / "repetisi.csv"


def validasi_dan_ekspor(input_csv: Path, out_csv: Path, izinkan_63: bool = True) -> None:
    if not input_csv.exists():
        raise FileNotFoundError(f"Berkas input tidak ditemukan: {input_csv}")
    df = pd.read_csv(input_csv)
    wajib = {"no", "jumlah_hitung_ulang"}
    if not wajib.issubset(df.columns):
        raise ValueError(f"Kolom wajib {wajib} tidak lengkap; kolom ditemukan: {list(df.columns)}")

    kosong = df["jumlah_hitung_ulang"].isna() | (df["jumlah_hitung_ulang"].astype(str).str.strip() == "")
    if kosong.any():
        no_kosong = df.loc[kosong, "no"].tolist()
        if izinkan_63 and no_kosong == [64]:
            print("[INFO] Kondisi #64 kosong (dikeluarkan karena terpotong offset +27,5s); 63 kondisi valid diproses.")
            df = df.loc[~kosong].copy()
        else:
            raise ValueError(
                f"Masih ada {int(kosong.sum())} kondisi belum diisi pada `jumlah_hitung_ulang` "
                f"(contoh nomor: {no_kosong[:10]}). Isi dulu hasil hitung visual sebelum ekspor!"
            )

    df["no"] = df["no"].astype(int)
    df["jumlah"] = pd.to_numeric(df["jumlah_hitung_ulang"], errors="raise")

    if df["no"].duplicated().any():
        raise ValueError("Ditemukan duplikat nomor kondisi (`no`).")
    if (df["jumlah"] <= 0).any() or (df["jumlah"] > 30).any():
        raise ValueError("Ditemukan angka repetisi di luar rentang wajar (0 < jumlah <= 30).")
    if df["jumlah"].nunique() == 1 and float(df["jumlah"].iloc[0]) == 10.0:
        raise ValueError("PERINGATAN: Seluruh nilai bernilai 10! Kartu Kasus Tim melarang memakai asumsi 10 tanpa hitung ulang.")

    hasil = df[["no", "jumlah"]].sort_values("no").reset_index(drop=True)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    hasil.to_csv(out_csv, index=False)

    print(f"[OK] Validasi berhasil -> {out_csv}")
    print(f"  - Jumlah kondisi valid : {len(hasil)}")
    print(f"  - Rentang repetisi     : {hasil['jumlah'].min():.2f} s.d. {hasil['jumlah'].max():.2f}")
    print(f"  - Rata-rata ± std      : {hasil['jumlah'].mean():.2f} ± {hasil['jumlah'].std():.2f}")
    print(f"  - Kondisi != 10        : {int((hasil['jumlah'] != 10).sum())} kondisi")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", type=Path, default=FOLDER_INI / "b06_template_repetisi_64_kondisi.csv")
    ap.add_argument("--out", type=Path, default=FOLDER_INI / "b06_repetisi_tervalidasi.csv")
    ap.add_argument("--salin-ke-repo", action="store_true", help="Salin juga ke data/repetisi.csv")
    ap.add_argument("--uji-diri", action="store_true", help="Jalankan uji mandiri skrip validasi di memori")
    a = ap.parse_args()

    if a.uji_diri:
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p_in = Path(td) / "uji.csv"
            p_out = Path(td) / "out.csv"
            pd.DataFrame({"no": [1, 2, 3], "jumlah_hitung_ulang": [9, 10.5, 11]}).to_csv(p_in, index=False)
            validasi_dan_ekspor(p_in, p_out)
            cek = pd.read_csv(p_out)
            assert list(cek.columns) == ["no", "jumlah"] and len(cek) == 3
            print("[PASS] Uji mandiri b06_validasi_dan_ekspor_repetisi.py berhasil.")
        return

    validasi_dan_ekspor(a.input, a.out)
    if a.salin_ke_repo:
        validasi_dan_ekspor(a.input, REPO_DATA_OUT)


if __name__ == "__main__":
    main()
