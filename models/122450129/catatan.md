# Catatan Model 1D-CNN (NIM: 122450129 - Vira Putri Maharani)

## Arsitektur Model
- **Jalur:** CNN (1D Temporal Convolution)
- **Input:** Urutan pose `[N, 190, 36]` (190 langkah waktu setelah trimming 1 detik pertama, 36 fitur sudut sendi).
- **Struktur:** 4 blok `Conv1d(kernel=5)` dengan dilation bertingkat 1, 2, 4, dan 8; setiap blok memakai BatchNorm dan ReLU. Output konvolusi dipertahankan ke **12 bin waktu** melalui `AdaptiveAvgPool1d(12)`, lalu diratakan dan dilewatkan ke MLP `288 → 96 → 1` dengan dropout 0,3.
- **Alasan 12 bin waktu:** jumlah repetisi adalah **jumlah siklus**, bukan rata-rata amplitudo. Global Average Pooling (GAP) membuang informasi jumlah siklus sehingga model GAP 2 lapis hanya mencapai val_MAE 3,609. Dengan mempertahankan 12 bin waktu, model masih dapat menghitung pola berulang sekaligus tetap ringkas.

## Alasan Optimizer & Loss
- **Optimizer:** AdamW, learning rate `1e-3`, weight decay `1e-4`, cosine annealing, batch 8.
- **Loss:** L1 Loss (MAE), selaras dengan metrik evaluasi utama kasus ini.
- **Early stopping:** maksimum 140 epoch, patience 30, checkpoint terbaik dipilih berdasarkan validation MAE. Data uji P07/P08 tidak digunakan pada Sprint 1.

## Regularisasi & Augmentasi
- Batch Normalization pada setiap blok konvolusi.
- Dropout 0,3 pada kepala regresi dan weight decay AdamW.
- Augmentasi ringan untuk 40 sampel latih: pergeseran waktu ±8 frame, noise Gaussian 0,008, dan channel dropout 4%.

## Pencarian Hyperparameter / Arsitektur
| Konfigurasi | Val MAE | Catatan |
|---|---:|---|
| Event-CNN sigmoid (sum probabilitas) | 1,2400 | under-estimasi, sinyal event tidak stabil |
| Event-CNN ReLU (sum aktivasi) | 1,1297 | lebih baik, tetapi masih jauh dari baseline |
| CNN + avg/max/std pooling | 0,2831 | cukup baik, tetapi membuang urutan temporal |
| **CNN + 12-bin temporal pooling** | **0,1961** | arsitektur final, seed 1 |
| Baseline ridge non-DL | 0,3382 | pembanding tim |

## Ablation
1. **GAP → 12-bin temporal pooling:** val_MAE turun dari 3,609 (CNN GAP 2 lapis yang dilatih penuh) menjadi 0,196 pada seed 1.
2. **Dilation 1/2/4/8:** memperluas receptive field tanpa menambah kedalaman berlebihan, sehingga satu filter dapat menangkap beberapa siklus repetisi.
3. **Early stopping:** pada eksperimen tanpa early stopping, val_MAE memburuk setelah epoch 90 karena overfitting pada 40 sampel latih.

## Reproduksi
```bash
python models/122450129/run.py --seed 1
```
Keluaran: `results/122450129/metrics.json`, `results/122450129/pred_val.npy`, dan `results/122450129/training_log.json`.

## Catatan Integritas
Fallback ridge NumPy pada versi lama **dihapus** karena bukan CNN dan menghasilkan metrik yang tidak merepresentasikan jalur CNN. Model sekarang mewajibkan PyTorch; requirements tim sudah memuat `torch>=2.2`.
