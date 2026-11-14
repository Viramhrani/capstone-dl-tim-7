# Pembagian Peran Slot Meja dan Manajemen Partisipan — Tim 7

**Nomor Tugas:** #2 (Review / Menunggu Persetujuan Pembimbing)  
**Tenggat:** 10 November 2026  
**Poin:** 3 poin  
**Label:** `sprint 1`, `koordinator`  
**Kasus:** Penghitung repetisi peregangan meja kerja (Ruang Cerdas 5 Volt)  

---

## 1. Pembagian Peran Anggota Tim Saat Slot
Sesuai kesepakatan pembagian tugas lapangan pada saat sesi pengambilan data di meja uji:

| Nama Anggota | NIM | Peran Utama di Slot | Tanggung Jawab Teknis Lapangan |
|---|---|---|---|
| **Vira Putri Maharani** | 122450129 | **Operator Meja & Perekam** | Mengoperasikan laptop meja uji, memverifikasi `python meja.py periksa`, memeriksa pratinjau citra webcam ($640 \times 480$), menekan tombol Enter saat blok partisipan berganti, dan memantau status perekaman ESP32. |
| **Salsabila Putri Maharani** | 123450070 | **Koordinator Partisipan** | Menyambut partisipan P01–P08, memastikan formulir persetujuan etika ditandatangani, memeriksa busana partisipan (kontras, sendi terlihat), mendudukkan partisipan di kursi bertanda selotip, dan mengatur urutan giliran blok. |
| **Monica Patricia Tanjung** | 123450073 | **Pencatat Sesi & Metronom** | Memegang ponsel dengan metronom (tempo 1 ketukan / 2 detik), menghitung repetisi kasat mata secara independen, dan menuliskan catatan jumlah repetisi serta kondisi gangguan pada Lembar Sesi. |
| **Arya Muda Siregar** | 123450063 | **Pengawas Mutu & Logistik** | Memeriksa stabilitas pencahayaan meja kerja, memastikan tidak ada orang yang melintas di latar belakang kamera selama kondisi aktif, dan membantu pencadangan data segera setelah sesi selesai. |

---

## 2. Rencana Partisipan (P01–P08)
- **Karakteristik Partisipan:** 8 orang mahasiswa/staf di luar anggota tim (untuk menjaga validitas dan generalisasi model).
- **ID Samaran:** P01, P02, P03, P04, P05, P06, P07, P08.
- **Kondisi Per Partisipan:** Setiap partisipan menjalankan 1 blok yang berisi 8 kondisi (4 latihan $\times$ 2 ulangan).
- **Prosedur Etika:**
  - Partisipan diberikan penjelasan singkat mengenai tujuan penelitian.
  - Penandatanganan formulir persetujuan (*informed consent*).
  - Partisipan memiliki hak penuh untuk menghentikan rekaman kapan saja.
  - Data wajah/identitas visual tidak dipublikasikan secara langsung; hanya koordinat pose sendi 33 titik yang diekstraksi untuk analisis deep learning.

---

## 3. Protokol Pergantian Blok dan Penanganan Gangguan
1. **Pergantian Blok:**
   - Skrip berhenti sejenak di akhir kondisi ke-8 pada suatu blok dan menampilkan pesan:
     `Siapkan: Partisipan Pxx siap di posisi (formulir persetujuan sudah ditandatangani)`.
   - Koordinator mengarahkan partisipan berikutnya untuk duduk dan tenang.
   - Operator memastikan seluruh tubuh atas berada di dalam bingkai, lalu menekan Enter untuk memulai blok.
2. **Penanganan Gangguan (Insiden):**
   - Apabila terjadi gerakan salah, batuk, atau partisipan berhenti di tengah jalan, rekaman **tidak diulang di tempat** demi menjaga integritas deret waktu.
   - Pencatat menuliskan nomor kondisi (misal `[23/64]`) dan deskripsi insiden di Lembar Sesi.
   - Kondisi tersebut akan dievaluasi pada saat pemeriksaan mutu data di luar slot.
