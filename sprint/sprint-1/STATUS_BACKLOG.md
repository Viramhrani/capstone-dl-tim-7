# Status Backlog Sprint 1 — Tim 7 (Ruang Cerdas 5 Volt)

**Diperbarui:** 28 November 2026  
**Sumber:** Sinkronisasi Papan Tim Workbench (`tim_61f8f0b37084`, 19 kartu) dengan kondisi aktual repositori lokal & GitHub (`Viramhrani/capstone-dl-tim-7`).  
**Batas Log Sprint & Demo Sprint 1:** `1 Desember 2026, pukul 23.59 WIB`

---

## 1. Status Seluruh 19 Backlog Sprint 1

*(Seluruh 19 kartu di Workbench sudah memiliki penanggung jawab resmi — `0` kartu kosong. Perhatikan perbedaan antara **Status di Workbench** dengan **Kesiapan Kode/Bukti Lokal**.)*

| # | Tugas | Penanggung Jawab (Workbench) | Prioritas | Status Workbench | Kondisi Aktual Lokal & GitHub | Bukti / Catatan |
|---:|---|---|---|---|---|---|
| **1** | Rencana final `t07-repetisi-peregangan.yaml` disetujui pembimbing dan diserahkan ke pengelola meja | **Vira Putri Maharani** (`122450129`) | Mendesak | **Review** | Masuk `main`, menunggu persetujuan pembimbing | `rencana/t07-repetisi-peregangan.yaml` |
| **2** | Peran slot meja 11 Nov dan partisipan | **Vira Putri Maharani** (`122450129`) | Tinggi | **Review** | Masuk `main`, sesi 16 Nov terlaksana, menunggu persetujuan pembimbing | `rencana/PERAN_SLOT_DAN_PARTISIPAN.md` & komentar `#2` |
| **3** | Sprint Goal, Log Sprint, dan Demo Sprint 1 | **Vira Putri Maharani** (`122450129`) | Tinggi | **Backlog** | **Belum selesai** | Draf log (`sprint/sprint-1/122450129.md`) & naskah demo (`DEMO_SPRINT_1.md`) siap; Sprint Goal, Log 4/4 anggota, dan unggah Demo di Workbench masih perlu dituntaskan |
| **4** | Pemotong jendela dan `PROTOKOL.md` dari data simulasi | **Monica Patricia Tanjung** (`123450073`) | Mendesak | **Backlog** | Kode siap lokal (**belum PR ke `main`**) | `src/protokol/data.py`, `pemotong_jendela.py`, `PROTOKOL.md`; unit test `test_pemotong_jendela.py` **6/6 PASS** |
| **5** | Terima data sesi meja (11 Nov), `MANIFEST.json`, dan pemeriksaan mutu | **Monica Patricia Tanjung** (`123450073`) | Mendesak | **Backlog** | **Sebagian** (audit 16 Nov selesai, menunggu kunci `MANIFEST.json` final) | Arsip 16 Nov lengkap (`tim07_sesi-...` & `tim07_web-...`); draf `data/CATATAN-SESI.md` & `pose_sesi_16nov.npz` ada; menunggu konfirmasi offset `+27,5s` & `#64` lalu PR |
| **6** | Pekerjaan lapangan di luar slot (1): Hitung ulang repetisi ke `data/repetisi.csv` | **Arya Muda Siregar** (`123450063`) *(kolab: Monica)* | Tinggi | **Backlog** | **Belum dikerjakan** | Wajib hitung ulang 64 kondisi dari urutan foto ke `data/repetisi.csv` (`no,jumlah`) & catat selisihnya di `data/CATATAN-SESI.md` |
| **7** | Repo tim siap: folder tiap anggota dan `run_all.py` pada data simulasi | **Salsabila Putri Maharani** (`123450070`) | Tinggi | **Review** | Diuji simulasi & diajukan ke Review (25 Nov) | `models/<nim>/`, `src/common/` utuh, `run_all.py` |
| **8** | Merge komponen tiap jalur dan `run_all.py` pada data primer meja | **Salsabila Putri Maharani** (`123450070`) *(kolab: Vira)* | Tinggi | **Dikerjakan** | Uji awal di `123450070/kerja`; menunggu semua PR masuk `main` | `run_all.py`, `reports/hasil_komparasi.md` |
| **9** | Pembanding non-DL: Hitung puncak sinyal sudut sendi | **Salsabila Putri Maharani** (`123450070`) *(kolab: Monica)* | Mendesak | **Backlog** | Kode siap lokal (**belum PR**; perlu jalankan ulang pada data final 16 Nov) | `src/pembanding/puncak_sudut.py`, `tests/test_pembanding_puncak.py` (**4/4 PASS**), `val_MAE = 0,369841` (data protokol aktif) |
| **10** | Gladi rencana: mode simulasi dan persiapan bahan slot | **Arya Muda Siregar** (`123450063`) | Tinggi | **Backlog** | Kode & bukti siap lokal (**belum PR ke `main`**) | `rencana/GLADI_RENCANA.md`, `python test_simulasi.py` (**PASS** 64 kondisi) |
| **11** | Rekaman Demo Sprint 1 | **Arya Muda Siregar** (`123450063`) *(kolab: Vira & Salsabila)* | Sedang | **Backlog** | **Belum dikerjakan** (menunggu `#8` selesai di `main`) | Naskah siap di `sprint/sprint-1/DEMO_SPRINT_1.md`; rekam `≤ 10 mnt`, `≤ 50 MB` |
| **12** | [CNN] Kerangka `models/122450129/run.py` pada data simulasi | **Vira Putri Maharani** (`122450129`) | Tinggi | **Review** | Masuk `main`, uji simulasi **PASS** (`val_MAE 0,0332`) | `models/122450129/run.py`, `uji_simulasi.py` |
| **13** | [CNN] Latih pada data primer meja (seed 1) dan `metrics.json` valid | **Vira Putri Maharani** (`122450129`) | Mendesak | **Backlog** | Siap pada data 1 Nov (`val_MAE 0,1961`); perlu latih ulang bila data 16 Nov dibekukan | `results/122450129/metrics.json` (`41.089` param, `3,72 ms`) |
| **14** | [RNN] Kerangka `models/123450063/run.py` pada data simulasi | **Arya Muda Siregar** (`123450063`) | Tinggi | **Backlog** | Kode siap lokal (**belum PR** dari `123450063/kerja`) | `models/123450063/run.py` (uji simulasi **PASS**) |
| **15** | [RNN] Latih pada data primer meja (seed 1) dan `metrics.json` valid | **Arya Muda Siregar** (`123450063`) | Mendesak | **Backlog** | Siap lokal pada data 1 Nov (`val_MAE 0,1882`); perlu PR & latih ulang pada data 16 Nov | `results/123450063/metrics.json` (`172.545` param) |
| **16** | [Transformer] Kerangka `models/123450070/run.py` pada data simulasi | **Salsabila Putri Maharani** (`123450070`) | Tinggi | **Review** | Diuji & diajukan ke Review (commit `3c12bef` di `123450070/kerja`) | `models/123450070/run.py` |
| **17** | [Transformer] Latih pada data primer meja (seed 1) dan `metrics.json` valid | **Salsabila Putri Maharani** (`123450070`) | Mendesak | **Backlog** | Siap lokal pada data 1 Nov (`val_MAE 0,1780`); perlu PR & latih ulang pada data 16 Nov | `results/123450070/metrics.json` (`73.281` param, `3,38 ms`) |
| **18** | [AE] Kerangka `models/123450073/run.py` pada data simulasi | **Monica Patricia Tanjung** (`123450073`) | Tinggi | **Backlog** | Kode siap lokal (**belum PR** dari `123450073/kerja`) | `models/123450073/run.py` (uji simulasi **PASS**) |
| **19** | [AE] Latih pada data primer meja (seed 1) dan `metrics.json` valid | **Monica Patricia Tanjung** (`123450073`) | Mendesak | **Backlog** | Siap lokal pada data 1 Nov (`val_MAE 0,2545`); perlu PR & latih ulang pada data 16 Nov | `results/123450073/metrics.json` (`12.733` param, `1,57 ms`) |

---

## 2. Ringkasan Hasil Terverifikasi Sementara (Seed 1 — Dataset Protokol Aktif)

> **Catatan integritas data:** Angka di bawah terverifikasi 100% reproduktif pada `data/peregangan_meja.npz` (`data_hash: aeda5c2993d852ca51dea5162745d11c`, bertanggal 1 Nov 2026, `n_test = 0`). Seluruh model wajib dijalankan ulang serentak apabila tim & pembimbing membekukan dataset hasil sesi asli **16 Nov 2026** (`pose_sesi_16nov.npz` + `data/repetisi.csv`).

| Model & Pemilik | `val_MAE` | `val_RMSE` | `val_R²` | Parameter | Latensi CPU (1 sampel) |
|---|---:|---:|---:|---:|---:|
| **Transformer patchify (`123450070` — Salsabila)** | **0,1780** | **0,2205** | **0,9905** | `73.281` | `3,38 ms` |
| **RNN Bi-GRU (`123450063` — Arya)** | `0,1882` | `0,2453` | `0,9882` | `172.545` | `46,1–65,4 ms` |
| **CNN 1D (`122450129` — Vira)** | `0,1961` | `0,2574` | `0,9870` | `41.089` | `3,72 ms` |
| **Autoencoder (`123450073` — Monica)** | `0,2545` | `0,3290` | `0,9788` | **`12.733`** | **`1,57–1,81 ms`** |
| Baseline ridge (starter) | `0,3382` | `0,4210` | `0,9652` | — | `< 1 ms` |
| Pembanding puncak sudut (`#9`) | `0,3698` | `0,4299` | `0,9638` | `0` | `< 5 ms` |

---

## 3. Tindakan Prioritas Sebelum Penutupan Sprint 1 (`1 Desember 2026, 23.59 WIB`)

1. **Sinkronkan profil Kontrak Tim di Workbench** (`/workbench/capstone/aturan`): Arya pindah dari Transformer → RNN dulu, lalu Salsabila pilih Transformer, dan Monica pilih Autoencoder + tugas sampingan masing-masing.
2. **Konfirmasi pembimbing & pengelola meja:** Offset `+27,5` detik, pengeluaran Kondisi `#64`, deteksi rendah `#48/#56` (`putar leher pelan`), serta peralihan dataset 1 Nov → 16 Nov.
3. **Tuntaskan jalur data (`#6`, `#4`, `#5`):** Arya isi `data/repetisi.csv` (`#6`), Monica cek silang & bekukan `data/MANIFEST.json` + PR protokol (`#4`, `#5`).
4. **Latih ulang `--seed 1` & buka PR dari akun GitHub masing-masing:** Vira (`#13`), Arya (`#10, #14, #15`), Salsabila (`#9, #17`), Monica (`#18, #19`); Vira review & merge semua PR ke `main`.
5. **Jalankan integrasi pusat (`#8`) & Demo Sprint 1 (`#11`, `#3`):** Salsabila jalankan `python run_all.py --seeds 1` di `main` dan loloskan *Periksa artefak* → Arya rekam Demo Sprint 1 (`≤ 10 mnt`, `≤ 50 MB`) bersama Vira & Salsabila → Vira isi **Sprint Goal**, seluruh **4/4 anggota isi Log Sprint 1**, unggah Demo Sprint 1, dan pindahkan semua kartu tuntas ke **Review**.
