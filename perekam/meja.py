"""Skrip Meja Uji Ruang Cerdas 5 Volt — Mode Simulasi dan Eksekusi Eksperimen.
Tersedia di folder perekam/ untuk kompatibilitas jalur relatif `../rencana/t07-repetisi-peregangan.yaml`.
"""
from __future__ import annotations
import sys
from pathlib import Path

# Impor implementasi meja dari root
AKAR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AKAR))

import meja

if __name__ == "__main__":
    meja.main()
