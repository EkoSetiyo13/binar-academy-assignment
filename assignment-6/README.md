# Assignment 6: Debugging Your MCP Integration

Folder `image-debugging` berisi kumpulan skrip dan dokumentasi yang digunakan untuk melakukan debugging pada proses pengolahan gambar. Berikut adalah ringkasan dari isi dan fungsionalitas utama di dalam folder ini:

## Struktur Folder

- **src/**  
  Berisi kode sumber utama untuk proses debugging gambar, termasuk script untuk membaca, memproses, dan menganalisis gambar.

- **test/**  
  Berisi unit test untuk memastikan setiap fungsi berjalan dengan baik.

- **assets/**  
  Berisi contoh gambar yang digunakan untuk pengujian dan debugging.

## Fitur Utama

- **Membaca dan menampilkan gambar**  
  Script dapat membaca berbagai format gambar dan menampilkannya untuk keperluan analisis.

- **Deteksi error pada gambar**  
  Terdapat fungsi untuk mendeteksi error umum seperti gambar rusak, format tidak didukung, atau metadata yang hilang.

- **Logging proses debugging**  
  Setiap proses dan error yang terjadi selama debugging akan dicatat ke dalam log untuk memudahkan pelacakan.

- **Unit testing**  
  Seluruh fungsi utama telah dilengkapi dengan unit test untuk memastikan stabilitas dan keandalan.

## Cara Menggunakan

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Jalankan script debugging**
   ```bash
   npm run debug
   ```

3. **Cek hasil log**
   - Log proses dan error dapat ditemukan di folder `logs/`.

## Catatan

- Pastikan gambar yang diuji berada di folder `assets/`.
- Untuk menambah format gambar baru, modifikasi file di `src/reader.ts`.

---

### Pertanyaan: Apa masalah yang kamu temukan dan bagaimana cara menyelesaikannya?

**Jawaban 1:**  
Masalah utama yang sering saya temui adalah terkait path, terutama saat integrasi ke MCP Inspector dan Claude. Saya sempat mencoba bertanya ke AI, namun jawabannya kurang membantu. Setelah mencari referensi di YouTube dan membaca dokumentasi, saya akhirnya memahami bahwa masalahnya ada pada argumen (args) yang diberikan ke server, sehingga saya bisa memperbaikinya.

**Jawaban 2:**  
Selain masalah path, saya juga menemukan error terkait environment variable yang tidak terbaca saat menjalankan script debugging. Setelah menelusuri error log dan mencoba beberapa solusi, saya menyadari bahwa saya salah penulisan di beberapa variabel. Setelahnya, proses debugging berjalan lancar tanpa error konfigurasi.

---

_Ini adalah ringkasan otomatis berdasarkan isi folder `image-debugging`. Silakan cek setiap file untuk detail lebih lanjut._