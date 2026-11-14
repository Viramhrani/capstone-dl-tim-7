# Laporan Gladi Rencana dan Persiapan Bahan Slot — Tim 7

**Nomor Tugas:** #10 (Backlog)  
**Tenggat:** 10 November 2026  
**Poin:** 2 poin  
**Label:** `sprint 1`, `reproduksi demo`  
**Kasus:** Penghitung repetisi peregangan meja kerja (Ruang Cerdas 5 Volt)  

---

## 1. Eksekusi Mode Simulasi
Gladi rencana dijalankan menggunakan skrip `meja.py` berbasis rencana eksperimen `rencana/t07-repetisi-peregangan.yaml`:

```bash
# Dari direktori utama proyek:
python meja.py --simulasi jalankan rencana/t07-repetisi-peregangan.yaml

# Atau dari direktori perekam/:
cd perekam && python meja.py --simulasi jalankan ../rencana/t07-repetisi-peregangan.yaml
```

### Hasil Verifikasi Simulasi:
- **Seed Eksperimen:** `1007` (pengacakan blok partisipan dan kondisi dalam blok bersifat deterministik).
- **Jumlah Total Kondisi:** **64 kondisi** (8 blok partisipan $\times$ 8 kondisi per blok).
- **Struktur Per Blok:**
  - 4 variasi gerakan: `putar bahu`, `angkat kedua lengan`, `putar leher pelan`, `peregangan pergelangan`.
  - 2 ulangan per variasi gerakan.
- **Urutan Blok Terverifikasi:**
  1. Blok 1: Partisipan P06 (8 kondisi)
  2. Blok 2: Partisipan P08 (8 kondisi)
  3. Blok 3: Partisipan P04 (8 kondisi)
  4. Blok 4: Partisipan P03 (8 kondisi)
  5. Blok 5: Partisipan P02 (8 kondisi)
  6. Blok 6: Partisipan P05 (8 kondisi)
  7. Blok 7: Partisipan P07 (8 kondisi)
  8. Blok 8: Partisipan P01 (8 kondisi)
- **Estimasi Waktu Pelaksanaan:**
  - Waktu rekam bersih: $64 \times 20\text{ detik} = 1.280\text{ detik}$ ($\approx 21,3$ menit).
  - Jeda antar-kondisi: $64 \times 0,5\text{ detik} = 32\text{ detik}$.
  - Transisi pergantian 8 blok partisipan: $\approx 8\text{ menit}$.
  - Total estimasi sesi: $\approx 30$ menit (muat aman dalam alokasi slot operator 50 menit).
- **Log Lengkap Hasil Simulasi:** Disimpan di `rencana/simulasi_output.txt`.
- **Pengujian Otomatis:** Lolos uji melalui `python test_simulasi.py`.

---

## 2. Bahan dan Kebutuhan Slot (Checklist Persiapan)
Sesuai instruksi khusus kasus Tim 7 dan panduan metode eksperimen lapangan:

| No | Kebutuhan | Spesifikasi / Keterangan | Status Kesiapan |
|---|---|---|---|
| 1 | **Metronom Ponsel** | Tempo **1 ketukan per 2 detik** (30 BPM / 0,5 Hz). Digunakan untuk memandu ritme partisipan (10 repetisi dalam 20 detik). Boleh dibunyikan bebas karena kasus tidak merekam audio. | **Siap** |
| 2 | **Selotip Penanda Posisi** | Selotip kertas di lantai untuk menandai posisi kaki kursi/posisi duduk partisipan agar bidang pandang kamera (FoV) konstan. | **Siap** |
| 3 | **Kamera / Webcam Meja** | Resolusi $640 \times 480$ @ 10 fps. Diarahkan miring 45° dari tiang 75 cm untuk menangkap seluruh persendian atas (kepala, leher, bahu, siku, pergelangan). | **Siap** |
| 4 | **Pakaian Partisipan** | Pakaian berwarna kontras dengan latar belakang dinding/meja kerja; tanpa topi, masker, atau tudung kepala (hoodie) yang menutupi leher/sendi. | **Siap** |
| 5 | **Formulir Persetujuan Etika** | 8 lembar *informed consent* untuk partisipan P01–P08 (diutamakan mahasiswa dari luar tim). | **Siap** (`rencana/FORMULIR_PERSETUJUAN.md`) |
| 6 | **Lembar Sesi Fisik** | Lembar pencatat untuk menulis nomor kondisi, jumlah repetisi yang tampak langsung, dan catatan gangguan per kondisi. | **Siap** (`rencana/LEMBAR_SESI.md`) |

---

## 3. Pembagian Peran Anggota Tim Saat Slot
Pembagian peran lapangan yang disepakati untuk slot pengambilan data:
- **Vira Putri Maharani (122450129)** : Koordinator Partisipan
- **Salsabila Putri Maharani (123450070)** : Operator Perekam
- **Monica Patricia Tanjung (123450073)** : Operator Alat
- **Arya Muda Siregar (123450063)** : Pencatat Kejadian dan Penjaga Bingkai Kamera

---

## 4. Prosedur Latihan Kering (*Dry Run*)
Sebelum sesi rekaman sebenarnya di meja uji, tim melakukan latihan kering tanpa perangkat meja:
1. **Instruksi Standar:**
   Operator membacakan instruksi dengan kalimat baku yang sama kepada setiap partisipan:
   - *"Duduk tegak menghadap layar. Ikuti ketukan metronom (satu gerakan penuh tiap 2 detik). Lakukan gerakan sesuai teks yang tampil di layar sebanyak 10 kali, lalu berhenti."*
2. **Demonstrasi Gerakan:**
   Operator mencontohkan masing-masing gerakan sekali dengan amplitudo gerakan yang cukup besar:
   - *Putar bahu*: Putar kedua bahu ke arah belakang secara penuh.
   - *Angkat kedua lengan*: Angkat kedua tangan ke atas kepala membentuk huruf V lalu turunkan kembali.
   - *Putar leher pelan*: Putar kepala pelan secara memutar dengan rentang gerak wajar.
   - *Peregangan pergelangan*: Tautkan jari-jari kedua tangan dan dorong telapak ke arah depan menjauhi dada.
3. **Penyelarasan Pencatat:**
   Pencatat sesi berlatih menghitung repetisi bersamaan dengan metronom guna meminimalkan galat hitung manual saat sesi sebenarnya berlangsung.
