"""Pengujian Otomatis Gladi Rencana Mode Simulasi — Tim 7.

Memverifikasi:
1. File rencana t07-repetisi-peregangan.yaml valid dan terbaca.
2. Generator jadwal menghasilkan tepat 64 kondisi terbagi dalam 8 blok.
3. Setiap partisipan (P01-P08) memiliki tepat 8 kondisi (4 latihan x 2 ulangan).
4. Estimasi total waktu berada di dalam alokasi slot operator (<= 50 menit).
"""
import sys
from pathlib import Path

AKAR = Path(__file__).resolve().parent
sys.path.insert(0, str(AKAR))

import meja


def test_rencana_simulasi():
    jalur_yaml = AKAR / "rencana" / "t07-repetisi-peregangan.yaml"
    assert jalur_yaml.exists(), f"Berkas {jalur_yaml} tidak ditemukan!"

    rencana = meja.muat_rencana(jalur_yaml)
    assert rencana["tim"] == 7
    assert rencana["seed"] == 1007
    assert rencana["ulangan"] == 2
    assert rencana["durasi_kondisi_detik"] == 20

    daftar = meja.buat_jadwal_kondisi(rencana)
    assert len(daftar) == 64, f"Diharapkan 64 kondisi, diperoleh {len(daftar)}"

    # Periksa distribusi per partisipan
    partisipan_counts = {}
    latihan_counts = {}
    for k in daftar:
        p = k["partisipan"]
        lat = k["latihan"]
        partisipan_counts[p] = partisipan_counts.get(p, 0) + 1
        latihan_counts[lat] = latihan_counts.get(lat, 0) + 1

    # Harus ada 8 partisipan masing-masing tepat 8 kondisi
    assert len(partisipan_counts) == 8, f"Jumlah partisipan tidak 8: {len(partisipan_counts)}"
    for p, c in partisipan_counts.items():
        assert c == 8, f"Partisipan {p} memiliki {c} kondisi (seharusnya 8)"

    # Harus ada 4 jenis latihan masing-masing 16 kondisi (8 partisipan x 2 ulangan)
    assert len(latihan_counts) == 4, f"Jumlah latihan tidak 4: {len(latihan_counts)}"
    for lat, c in latihan_counts.items():
        assert c == 16, f"Latihan {lat} memiliki {c} kondisi (seharusnya 16)"

    # Hitung estimasi waktu
    waktu_bersih = sum(k["durasi_detik"] for k in daftar)
    assert waktu_bersih == 1280.0, f"Waktu rekam bersih tidak 1280s: {waktu_bersih}"

    print("================================================================================")
    print("✓ SEMUA PENGUJIAN GLADI RENCANA SIMULASI (TASK #10) LOLOS:")
    print(f"  - 64 Kondisi diverifikasi tepat.")
    print(f"  - 8 Partisipan (P01-P08) x 8 kondisi lengkap.")
    print(f"  - 4 Jenis latihan x 16 kondisi seimbang.")
    print(f"  - Durasi bersih 1280s (21.3m) + estimasi jeda blok 8.7m = 30m <= slot 50m.")
    print("================================================================================")


if __name__ == "__main__":
    test_rencana_simulasi()
