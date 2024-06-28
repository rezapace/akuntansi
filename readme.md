# Deskripsi Proyek

Proyek ini bertujuan untuk mengotomatisasi proses pembukuan transaksi keuangan menggunakan API Groq. Dengan memanfaatkan data transaksi yang ada, program ini akan menghasilkan jurnal umum, buku besar, dan neraca saldo dalam format Excel.

## Kegunaan

Proyek ini sangat berguna bagi perusahaan atau individu yang ingin mengelola pembukuan mereka secara otomatis dan efisien. Dengan menggunakan API Groq, proses pembuatan laporan keuangan menjadi lebih cepat dan akurat.

## Fungsi

1. **Membaca Data Transaksi**: Program akan membaca data transaksi dari file `soal.txt`.
2. **Mengirim Data ke Groq**: Data transaksi akan dikirim ke API Groq untuk diproses.
3. **Memparse Hasil dari Groq**: Hasil yang diterima dari Groq akan diparse menjadi format yang dapat digunakan.
4. **Menyimpan Data ke Excel**: Data yang telah diparse akan disimpan dalam file Excel dengan format yang sesuai.

## Cara Menjalankan

1. **Setel API Key**: Ekspor API key Groq dengan perintah berikut:
    ```bash
    export GROQ_API_KEY="gsk_yIQm2F"
    ```

2. **Instalasi Dependensi**: Instal semua dependensi yang diperlukan dengan perintah:
    ```bash
    pip install -r requirements.txt
    ```

3. **Jalankan Program**: Jalankan program dengan perintah:
    ```bash
    python main.py
    ```

## Kesimpulan

Proyek ini menyediakan solusi otomatis untuk pembukuan transaksi keuangan dengan memanfaatkan API Groq. Dengan mengikuti langkah-langkah di atas, Anda dapat dengan mudah menghasilkan laporan keuangan yang lengkap dan akurat dalam format Excel.