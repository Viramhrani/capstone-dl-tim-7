# Catatan Model Temporal Transformer (NIM: 123450070 - Salsabila Putri Maharani)

## Arsitektur Model
- **Jalur:** Transformer (Multi-Head Self-Attention)
- **Input:** Sekuens temporal `[N, 190, 36]`.
- **Struktur:** Linear input projection ke $d_{model}=48$, 2 encoder layer (4 attention heads, $d_{ff}=96$), dropout 0.1, temporal mean pooling, dan linear head regresi.

## Alasan Optimizer & Loss
- **Optimizer:** AdamW dengan cosine decay scheduling sederhana (lr=0.002, weight decay=1e-4).
- **Loss Function:** L1 Loss (MAE).

## Regularisasi
- Attention dropout 0.1 dan residual connection.
- Layer Normalization pada tiap sub-layer untuk menstabilkan gradien self-attention.

## Pencarian Hyperparameter (Tabel)
| Konfigurasi | Heads | Layers | d_model | Val MAE |
|---|---|---|---|---|
| Uji A | 2 | 1 | 32 | 0.395 |
| Uji B | 4 | 2 | 48 | **0.298** |
| Uji C | 4 | 3 | 64 | 0.324 |

## Ablation
1. **Jumlah Attention Heads (2 vs 4 heads):** 4 heads memberikan kemampuan representasi yang lebih baik dalam memisahkan koordinat sendi tangan dan bahu.
2. **Pengaruh Positional Encoding:** Penambahan relasi temporal membantu mendeteksi urutan repetisi lebih baik daripada mean pooling murni.
