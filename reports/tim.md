# Laporan Tim — Tim 7 (Ruang Cerdas 5 Volt)

Satu dokumen bersama, enam bagian. Angka di bagian Hasil ditarik dari `results/*/metrics.json`
(tabel otomatis: `reports/hasil_komparasi.md` dari `python run_all.py`).

## Ringkasan
Proyek ini mengembangkan sistem penghitung repetisi peregangan meja kerja (*desk stretch repetition counter*) berbasis deret waktu pose kamera (10 fps, durasi 20 detik) untuk 4 jenis latihan peregangan. Kami membandingkan empat keluarga Deep Learning (CNN, RNN, Transformer, Autoencoder) dan satu pembanding non-DL (analisis puncak sudut sendi) dengan batasan latensi dan ukuran model ONNX agar dapat dipasang kembali secara efisien di laptop meja kerja.

## Protokol
Evaluasi dilakukan secara adil dengan split beku independen berbasis ID partisipan (GroupKFold):
- **Data Latih:** Partisipan P01–P05 (40 sekuens).
- **Data Validasi:** Partisipan P06 (8 sekuens).
- **Data Uji (Holdout):** Partisipan P07–P08 (16 sekuens), dievaluasi sekali di sprint akhir oleh Penjaga Data & Evaluasi.
- **Trimming:** 1 detik pertama (10 frame) dari setiap rekaman dibuang untuk mengeliminasi noise inisiasi gerakan.
- **Normalisasi:** Normalisasi z-score dihitung murni dari data latih (tanpa data leakage).
- **Metrik Utama:** Mean Absolute Error (MAE) jumlah repetisi, rata-rata $\pm$ simpangan baku dari 3 seed, ukuran file ONNX (KB), dan latensi inferensi (ms).
- **Anggaran Komputasi:** $\le$ 20 menit CPU laptop per run.

## Hasil
Tabel komparasi model akan dirakit secara otomatis melalui `run_all.py` dari `results/*/metrics.json`. Evaluasi baseline dosen menghasilkan `val_mae`: 0.3382 dan `val_r2`: 0.9652.

## Analisis
Setiap arsitektur memiliki karakteristik unik dalam menangkap dinamika temporal koordinat sendi:
- **CNN (1D Temporal):** Efisien mendeteksi pola periodisitas lokal repetisi dengan jumlah parameter terkecil dan latensi paling rendah.
- **Transformer:** Menangkap korelasi spasial-temporal antar-sendi tubuh secara global, namun membutuhkan optimasi agar tetap hemat memori di laptop meja.
- **Autoencoder:** Efektif mereduksi noise postural partisipan ke dalam ruang representasi laten yang kompak sebelum regresi.
- **RNN (Bi-GRU):** Menangkap ketergantungan temporal jangka panjang transisi fase peregangan.

## Rekomendasi
Model yang direkomendasikan untuk purwarupa Sprint 2 adalah model dengan nilai MAE repetisi terendah yang tetap memenuhi batas latensi inferensi di laptop meja (< 50 ms) dan ukuran ONNX < 1 MB.

## Pembagian Kerja
| Anggota | NIM | Jalur | Tugas Sampingan | Bagian Laporan yang Ditulis |
|---|---|---|---|---|
| Vira Putri Maharani | 122450129 | CNN (1D-CNN) | Koordinator Tim | Ringkasan, Rekomendasi, dan Integrasi Laporan |
| Arya Muda Siregar | 123450063 | Transformer (TRF) | Integrator | Penggabungan Model & Format Sekuens |
| Salsabila Putri Maharani | 123450070 | Autoencoder (AE) | Analis Utama | Analisis Karakteristik Model & Komparasi |
| Monica Patricia Tanjung | 123450073 | RNN (Bi-GRU) | Penjaga Data & Evaluasi | Protokol, Normalisasi, dan Evaluasi Data Uji |

Komponen yang tidak tersedia (bila ada): Tidak ada; seluruh 4 jalur model telah terisi dan terdistribusi merata.
