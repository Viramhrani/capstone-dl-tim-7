# Catatan Model Bidirectional GRU (NIM: 123450063 - Arya Muda Siregar)

## Arsitektur Model
- **Jalur:** RNN (Bidirectional GRU)
- **Input:** Sekuens temporal `[N, 190, 36]`.
- **Struktur:** 2 lapis Bi-GRU dengan 48 hidden unit, dropout 0.2 antar-lapis, temporal pooling, dan 2-layer MLP regressor untuk menghitung estimasi jumlah repetisi.

## Alasan Optimizer & Loss
- **Optimizer:** Adam (lr=0.003, weight decay=1e-4) dengan gradient clipping norm 5.0 untuk stabilitas recurrent gate.
- **Loss Function:** L1 Loss (MAE).

## Regularisasi
- Recurrent dropout 0.2 dan MLP Dropout 0.2.
- Pengaturan hidden dimension yang ramping (48 unit) agar model ringan (< 500 KB ONNX).

## Pencarian Hyperparameter (Tabel)
| Konfigurasi | Layer | Hidden Units | Learning Rate | Val MAE |
|---|---|---|---|---|
| Uji A (LSTM) | 1 | 64 | 0.005 | 0.385 |
| Uji B (Bi-GRU) | 2 | 48 | 0.003 | **0.310** |
| Uji C (Bi-GRU) | 2 | 64 | 0.001 | 0.334 |

## Ablation
1. **Unidirectional vs Bidirectional GRU:** Penggunaan Bidirectional meningkatkan tangkapan transisi fase naik-turun pada siklus gerakan peregangan.
2. **Temporal Mean Pooling vs Last Hidden State:** Rata-rata temporal jauh lebih stabil terhadap fluktuasi akhir sekuens dibandingkan hanya mengambil frame terakhir.
