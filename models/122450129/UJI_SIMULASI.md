# Uji Kerangka CNN pada Data Simulasi — Backlog #12

**NIM:** 122450129 (Vira Putri Maharani)
**Tanggal:** 21 November 2026
**Tujuan:** memastikan `models/122450129/run.py` berjalan sampai akhir pada data simulasi
dan ukuran masukan/keluaran sesuai tugas regresi repetisi.

## Data simulasi yang dipakai
- 64 kondisi: 8 partisipan × 8 kondisi (4 latihan × 2 ulangan).
- NPZ `[64, 200, 36]`; setelah trimming protokol 10 frame menjadi `[64, 190, 36]`.
- Target repetisi 8,9–16,4; sinyal sintetis dibuat satu siklus per repetisi ditambah noise.
- Split mengikuti `src.protokol.data.muat()`: P01–P05 latih, P06 validasi, P07–P08 uji
  (data uji tidak dipakai pada uji ini).

## Cara menjalankan
```bash
python models/122450129/uji_simulasi.py
```

Skrip menyalin `src/` dan `run.py` ke direktori sementara, membuat NPZ + `MANIFEST.json`
simulasi, menjalankan `run.py --seed 1`, lalu memeriksa `metrics.json`,
`training_log.json`, dan `pred_val.npy`. Data asli di `data/` dan hasil asli di
`results/` tidak disentuh.

## Hasil aktual
```text
$ python models/122450129/run.py --seed 1
{"val_rmse": 0.038573, "val_mae": 0.03315, "val_r2": 0.999759} -> results\122450129\metrics.json
CNN seed=1: best_epoch=108 val_MAE=0.0332 durasi=55.1s
PASS uji simulasi: val_MAE=0.033150 val_RMSE=0.038573 val_R2=0.999759 best_epoch=108 pred_shape=(8,) data_hash=699b9f44c8b9ba6f86643b7fa01ecbeb
```

Pemeriksaan yang lolos:
- `metrics.json` memuat `val_mae`, `val_rmse`, `val_r2`, `seed=1`, `model=cnn`,
  `n_val=8`, `n_test=0`, dan `data_hash` 32 karakter.
- `training_log.json` memuat `best_epoch` dan durasi.
- `pred_val.npy` berbentuk `(8,)`, yaitu satu prediksi repetisi per kondisi validasi.
- Masukan model `[N, 190, 36]` dan keluaran `[N]` sesuai tugas regresi.

## Catatan
Angka MAE di atas berasal dari data sintetis, bukan hasil primer. Hasil primer CNN
tetap `val_mae=0,196114`, `val_rmse=0,257379`, `val_r2=0,987011` dengan
`data_hash=aeda5c2993d852ca51dea5162745d11c`.
