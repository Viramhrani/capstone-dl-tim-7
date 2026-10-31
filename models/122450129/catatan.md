# Catatan Model 1D-CNN (NIM: 122450129 - Vira Putri Maharani)

## Arsitektur Model
- **Jalur:** CNN (1D Temporal Convolution)
- **Input:** Urutan pose `[N, 190, 36]` (190 langkah waktu setelah trimming 1 detik pertama, 36 fitur koordinat sendi atas).
- **Struktur:** 2 lapis konvolusi 1D dengan BatchNorm dan ReLU untuk mengekstraksi pola periodisitas dan pergerakan sudut sendi, dilanjutkan dengan Global Average Pooling dan Dense layer untuk estimasi jumlah repetisi.

## Alasan Optimizer & Loss
- **Optimizer:** AdamW dengan learning rate $5 \times 10^{-3}$ dan bobot peluruhan (*weight decay*) $10^{-4}$. AdamW dipilih karena konvergensi yang cepat dan stabilitasnya terhadap deret waktu.
- **Loss Function:** L1 Loss (MAE), selaras dengan metrik evaluasi utama pada kasus ini (MAE repetisi).

## Regularisasi
- Batch Normalization pada setiap blok konvolusi 1D.
- Weight decay pada optimizer AdamW untuk mencegah overfitting pada sekuens gerakan yang serupa.

## Pencarian Hyperparameter (Tabel)
| Konfigurasi | Kernel Size | Filters | Learning Rate | Val MAE |
|---|---|---|---|---|
| Uji A | 3 | [16, 32] | 0.01 | 0.412 |
| Uji B | 5 | [32, 64] | 0.005 | **0.285** |
| Uji C | 7 | [32, 64] | 0.001 | 0.340 |

## Ablation
1. **Dampak Trimming 1 Detik Pertama:** Membuang 10 frame awal menurunkan noise inisiasi gerakan pengguna sehingga estimasi awal repetisi lebih konsisten.
2. **Global Average Pooling vs Flatten:** Penggunaan Global Average Pooling mengurangi parameter drastis (memenuhi syarat batasan ukuran ONNX dan latensi di laptop meja).
