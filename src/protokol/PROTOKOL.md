# Protokol evaluasi tim — Tim 7

Diisi Penjaga Data & Evaluasi pada Sprint 0, digabung ke `main` lewat *pull request* yang
disetujui pembimbing, lalu **dibekukan**. Perubahan setelah itu hanya lewat *pull request*
baru yang disetujui pembimbing.

| Butir | Isi |
|---|---|
| Kasus (dari kartu Kasus tim) | Penghitung repetisi peregangan meja kerja: hitung repetisi + klasifikasi latihan dari Urutan pose 10 fps, 20 s, dengan pembanding non-deep-learning dan batasan ukuran/latensi untuk dipasang kembali di laptop meja. |
| Sumber dataset | https://github.com/sains-data/capstone-dl-2026-starter (Data primer direkam mandiri di meja uji) |
| Jenis tugas (`TUGAS`) | regresi |
| Target / label | Jumlah repetisi peregangan (desain 10 repetisi per kondisi) |
| Ukuran data latih / validasi / uji | 40 sekuens (P01–P05) / 8 sekuens (P06) / 16 sekuens (P07–P08) |
| Cara split | Pemisahan berbasis Partisipan (GroupKFold / Holdout partisipan independen) |
| Metrik utama untuk komparasi | MAE (Mean Absolute Error) jumlah repetisi, stabilitas 3 seed, ukuran ONNX (KB), dan latensi inferensi (ms) |
| Praproses yang sama untuk semua model | 1 detik pertama (10 frame awal) dibuang, normalisasi fitur dihitung murni dari data latih |
| Anggaran komputasi per run | ≤ 20 menit CPU laptop meja |
| Evaluasi data uji | Sekali, oleh Penjaga Data & Evaluasi, pada sprint terakhir (`--final`) |
| `data_hash` saat dibekukan | aeda5c2993d852ca51dea5162745d11c |

Disetujui pembimbing pada: Menunggu review Sprint 0
