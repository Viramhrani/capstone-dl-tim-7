# Catatan Model Temporal Autoencoder (NIM: 123450073 - Monica Patricia Tanjung)

## Arsitektur Model
- **Jalur:** Autoencoder (AE - Temporal Representation Learning)
- **Input:** Sekuens temporal `[N, 190, 36]`.
- **Struktur:** Encoder (Linear $36 \to 24 \to 16$), Decoder ($16 \to 24 \to 36$) untuk merekonstruksi pose, dan MLP Regressor ($16 \to 1$) dari representasi bottleneck $16$ dimensi untuk menghitung repetisi.

## Alasan Optimizer & Loss
- **Optimizer:** Adam (lr=0.005, weight decay=1e-4).
- **Loss Function:** Joint loss: Reconstruction Loss (MSE) + Repetition Regression Loss (MAE).

## Regularisasi
- Bottleneck dimension yang sempit (16) memaksa model membuang noise gerakan postural dan hanya mempertahankan dinamika osilasi utama.
- L2 weight decay pada koneksi linear.

## Pencarian Hyperparameter (Tabel)
| Konfigurasi | Latent Dim | LR | Recon Weight | Val MAE |
|---|---|---|---|---|
| Uji A | 8 | 0.005 | 0.5 | 0.360 |
| Uji B | 16 | 0.005 | 1.0 | **0.295** |
| Uji C | 24 | 0.002 | 1.0 | 0.315 |

## Ablation
1. **Dampak Joint Reconstruction vs Pure Regressor:** Rekonstruksi pose membantu regularisasi fitur laten sehingga regresi tidak rentan terhadap overfitting pada partisipan tertentu.
2. **Ukuran Latent Dimension (8 vs 16):** Dimensi 16 optimal untuk mempertahankan koordinat sendi tangan dan leher tanpa meledakkan ukuran model ONNX.
