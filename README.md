# Dashboard Ranking CASN Mahkamah Agung 2024

Dashboard interaktif untuk melihat dan membandingkan hasil seleksi CASN Mahkamah Agung 2024 berdasarkan nilai integrasi SKD+SKB.

## Fitur

- Cek ranking peserta berdasarkan formasi jabatan dan provinsi
- Visualisasi distribusi nilai seluruh peserta
- Perbandingan dengan peserta peringkat teratas
- Analisis komponen nilai (SKD dan SKB)
- Informasi status kelulusan berdasarkan kuota yang tersedia

## Cara Penggunaan

1. Pastikan Python (versi 3.7+) terinstal di komputer Anda
2. Instal dependencies yang dibutuhkan:
   ```
   pip install -r requirements.txt
   ```
3. Jalankan aplikasi dengan perintah:
   ```
   streamlit run app.py
   ```
4. Buka browser dan akses URL yang ditampilkan di terminal (biasanya http://localhost:8501)

## Struktur Data

Dashboard ini menggunakan dataset dengan struktur sebagai berikut:
- `nomor_peserta`: Nomor peserta ujian
- `nama`: Nama peserta
- `jabatan`: Formasi jabatan yang dilamar
- `ipk`: IPK peserta
- `twk`, `tiu`, `tkp`: Komponen nilai SKD
- `nilai_skd`: Total nilai SKD
- `nilai_skb`: Nilai SKB
- `nilai_akhir`: Nilai integrasi SKD+SKB
- `province_rank`: Ranking peserta di provinsi
- `kuota_provinsi`: Kuota yang tersedia di provinsi
- `national_rank`: Ranking nasional
- `LOKASI_SKB`: Provinsi lokasi ujian SKB

## Formasi Tersedia

Dashboard mendukung beberapa formasi jabatan dengan kode sebagai berikut:
- apkaap: ANALIS PENGELOLAAN KEUANGAN APBN AHLI PERTAMA
- app: ANALIS PERKARA PERADILAN
- aap: ARSIPARIS AHLI PERTAMA
- ap: AUDITOR AHLI PERTAMA
- at: AUDITOR TERAMPIL
- dgap: DOKTER GIGI AHLI PERTAMA
- dh: DOKUMENTALIS HUKUM
- pksti: PENATA KELOLA SISTEM DAN TEKNOLOGI INFORMASI
- pk: PENATA KEPROTOKOLAN
- ptpap: PENGEMBANG TEKNOLOGI PEMBELAJARAN AHLI PERTAMA
- pt: PERAWAT TERAMPIL
- tsp: TEKNISI SARANA DAN PRASARANA
- tgmt: TERAPIS GIGI DAN MULUT TERAMPIL
- wap: WIDYAISWARA AHLI PERTAMA

## Disclaimer

Dashboard ini menggunakan data dari Mahkamah Agung 2024. Hasil analisis bersifat informatif dan tidak menggantikan pengumuman resmi dari instansi terkait.
