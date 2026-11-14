# Pembagian Peran Slot Meja dan Manajemen Partisipan — Tim 7

**Nomor Tugas:** #2 (Review / Menunggu Persetujuan Pembimbing)  
**Tenggat:** 10 November 2026  
**Poin:** 3 poin  
**Label:** `sprint 1`, `koordinator`  
**Kasus:** Penghitung repetisi peregangan meja kerja (Ruang Cerdas 5 Volt)  

---

## 1. Pembagian Peran Anggota Tim Saat Slot
Sesuai kesepakatan pembagian tugas lapangan pada saat sesi pengambilan data di meja uji (komentar Vira Putri Maharani tanggal 10 Nov 2026):

| Nama Anggota | NIM | Peran Utama di Slot | Tanggung Jawab Teknis Lapangan |
|---|---|---|---|
| **Vira Putri Maharani** | 122450129 | **Koordinator Partisipan** | Menyambut partisipan P01–P08, memastikan formulir persetujuan etika ditandatangani, memeriksa busana partisipan (warna kontras, sendi kepala/leher/bahu/lengan tidak tertutup), mendudukkan partisipan di kursi bertanda selotip, dan mengoordinasikan kesiapan tiap blok. |
| **Salsabila Putri Maharani** | 123450070 | **Operator Perekam** | Mengoperasikan antarmuka laptop perekam meja uji, menjalankan `python meja.py jalankan rencana/t07-repetisi-peregangan.yaml`, menekan Enter setelah partisipan siap di awal setiap blok, dan memantau status rekaman kondisi. |
| **Monica Patricia Tanjung** | 123450073 | **Operator Alat** | Memeriksa perangkat keras meja 5V (`python meja.py periksa`), memastikan sensor ESP32, daya, dan aktuator terhubung, memegang metronom ponsel (tempo 1 ketukan per 2 detik / 30 BPM) untuk memandu ritme repetisi partisipan. |
| **Arya Muda Siregar** | 123450063 | **Pencatat Kejadian dan Penjaga Bingkai Kamera** | Menjaga sudut pandang webcam $640 \times 480$ agar seluruh persendian atas partisipan masuk bingkai, memastikan area bebas dari orang melintas, menghitung repetisi kasat mata secara langsung, dan mencatat nomor kondisi serta gangguan pada Lembar Sesi. |

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
   - Koordinator Partisipan (Vira) mengarahkan partisipan berikutnya untuk duduk dan tenang.
   - Penjaga Bingkai Kamera (Arya) mengonfirmasi posisi tubuh partisipan berada dalam bingkai.
   - Operator Perekam (Salsabila) menekan Enter untuk memulai blok.
2. **Penanganan Gangguan (Insiden):**
   - Apabila terjadi gerakan salah, batuk, atau partisipan berhenti di tengah jalan, rekaman **tidak diulang di tempat** demi menjaga integritas deret waktu.
   - Pencatat Kejadian (Arya) menuliskan nomor kondisi (misal `[23/64]`) dan deskripsi insiden di Lembar Sesi.
   - Kondisi tersebut akan dievaluasi pada saat pemeriksaan mutu data di luar slot.
