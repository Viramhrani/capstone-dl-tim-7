"""Satu perintah reproduksi tim — Tim 7 (Ruang Cerdas 5 Volt).

    python run_all.py [--seeds 1 2 3] [--final] [--hanya <nim> ...]

Menjalankan baseline dosen dan ``models/<nim>/run.py`` setiap anggota untuk tiap seed, lalu
merakit ``reports/hasil_komparasi.md`` dari ``results/*/metrics.json``.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

AKAR = Path(__file__).resolve().parent
os.environ["PYTHONIOENCODING"] = "utf-8"


def jalankan(perintah: list[str]) -> None:
    print("$", " ".join(perintah), flush=True)
    subprocess.run(perintah, check=True, cwd=AKAR)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[1])
    ap.add_argument("--final", action="store_true")
    ap.add_argument("--hanya", nargs="*", default=None, help="NIM tertentu saja")
    ap.add_argument("--tanpa-baseline", action="store_true")
    a = ap.parse_args()

    if not a.tanpa_baseline:
        jalankan([sys.executable, "-m", "src.common.baseline", "--seed", str(a.seeds[0])])
    anggota = sorted(p for p in (AKAR / "models").iterdir() if p.is_dir() and (p / "run.py").exists()
                     and p.name != "TEMPLATE" and (a.hanya is None or p.name in a.hanya))
    ringkas: dict[str, list[dict]] = {}
    for m in anggota:
        for s in a.seeds:
            perintah = [sys.executable, str(m / "run.py"), "--seed", str(s)]
            if a.final and s == a.seeds[-1]:
                perintah.append("--final")
            jalankan(perintah)
            hasil = json.loads((AKAR / "results" / m.name / "metrics.json").read_text("utf-8"))
            ringkas.setdefault(m.name, []).append(hasil)

    baris = [
        "| NIM / Model | Jalur | seed | val_mae | val_rmse | val_r2 | durasi (s) | perangkat |",
        "|---|---|---|---|---|---|---|---|"
    ]
    bl = AKAR / "results" / "baseline" / "metrics.json"
    if bl.exists():
        h = json.loads(bl.read_text("utf-8"))
        mt = h["metrik"]
        mae = mt.get("val_mae", float("nan"))
        rmse = mt.get("val_rmse", float("nan"))
        r2 = mt.get("val_r2", float("nan"))
        baris.append(f"| baseline | baseline | {h['seed']} | {mae:.4f} | {rmse:.4f} | {r2:.4f} | {h.get('durasi_detik', 0):.1f} | {h.get('perangkat', '')} |")

    for nim, daftar in ringkas.items():
        for h in daftar:
            mt = h["metrik"]
            mae = mt.get("val_mae", float("nan"))
            rmse = mt.get("val_rmse", float("nan"))
            r2 = mt.get("val_r2", float("nan"))
            baris.append(
                f"| {nim} | {h.get('model', '')} | {h['seed']} | {mae:.4f} | {rmse:.4f} | {r2:.4f} | {h.get('durasi_detik', 0):.1f} | {h.get('perangkat', '')} |"
            )

    (AKAR / "reports").mkdir(exist_ok=True)
    out = AKAR / "reports" / "hasil_komparasi.md"
    out.write_text("# Hasil Komparasi Tim 7 (Ruang Cerdas 5 Volt)\n\n" + "\n".join(baris) + "\n", encoding="utf-8")
    print("Tabel komparasi berhasil dibuat ->", out.relative_to(AKAR))


if __name__ == "__main__":
    main()
