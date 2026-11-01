# AI_LOG — Tim 7 (Ruang Cerdas 5 Volt)

Satu baris per pemakaian AI yang bermakna (ChatGPT, Claude, Copilot, Bravais, dan sejenisnya).
Ringkas dan jujur; transkrip penuh tidak diminta. Yang dinilai bukan "pakai AI atau tidak",
melainkan "mengerti atau tidak" — isi kolom terakhir dengan apa yang Anda ubah dari keluarannya.

| Tanggal | Siapa (NIM) | Alat | Untuk apa | Apa yang diubah dari keluarannya |
|---|---|---|---|---|
| 2026-10-31 | 122450129 | Gemini | Desain arsitektur 1D-CNN untuk deteksi osilasi temporal pose | Mengganti kernel konvolusi dari 3 menjadi 5 dan menambahkan Global Average Pooling untuk mematuhi batasan ukuran ONNX di laptop meja |
| 2026-10-31 | 123450063 | Claude | Template Multi-Head Self-Attention untuk data deret waktu pose | Menyesuaikan dimensi model menjadi $d_{model}=48$ dan $nhead=4$ agar waktu komputasi $\le 20$ menit CPU laptop |
| 2026-10-31 | 123450070 | Copilot | Boilerplate arsitektur Joint Autoencoder-Regressor | Mengubah loss function regresi dari MSE menjadi L1 Loss agar selaras dengan metrik MAE repetisi tim |
| 2026-10-31 | 123450073 | ChatGPT | Skema recurrent Bi-GRU dan pembagian GroupKFold berbasis ID Partisipan | Memastikan 1 detik pertama tiap kondisi dibuang dan normalisasi dihitung hanya dari data latih (mencegah data leakage) |
