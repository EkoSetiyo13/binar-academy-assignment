# Assignment 6: Debugging Your MCP Integration

Folder `image-debugging` berisi kumpulan skrip dan dokumentasi yang digunakan untuk melakukan debugging pada proses pengolahan gambar. Berikut adalah ringkasan dari isi dan fungsionalitas utama di dalam folder ini:

## Struktur Folder

- **project/**  
  Berisi project mcp
- **image-debugging/**  
  Berisi hasil screenshot hasil debugging dan custom logging

## Fitur Utama

- **Membaca dan menampilkan gambar**  
  Script dapat membaca berbagai format gambar dan menampilkannya untuk keperluan analisis.

- **Deteksi error pada gambar**  
  Terdapat fungsi untuk mendeteksi error umum seperti gambar rusak, format tidak didukung, atau metadata yang hilang.

- **Logging proses debugging**  
  Setiap proses dan error yang terjadi selama debugging akan dicatat ke dalam log untuk memudahkan pelacakan.

## Cara Menggunakan

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Build**
   ```bash
   npm run build
   ```

3. **Cek hasil log**
   - Log proses dan error dapat ditemukan di folder `build/`.

_Ini adalah ringkasan otomatis berdasarkan isi folder `image-debugging`. Silakan cek setiap file untuk detail lebih lanjut._
---

### Pertanyaan: Apa masalah yang kamu temukan dan bagaimana cara menyelesaikannya?

**Jawaban 1:**  
Masalah utama yang sering saya temui adalah terkait path, terutama saat integrasi ke MCP Inspector dan Claude. Saya sempat mencoba bertanya ke AI, namun jawabannya kurang membantu. Setelah mencari referensi di YouTube dan membaca dokumentasi, saya akhirnya memahami bahwa masalahnya ada pada argumen (args) yang diberikan ke server, sehingga saya bisa memperbaikinya.

**Jawaban 2:**  
Selain masalah path, saya juga menemukan error terkait environment variable yang tidak terbaca saat menjalankan script debugging. Setelah menelusuri error log dan mencoba beberapa solusi, saya menyadari bahwa saya salah penulisan di beberapa variabel. Setelahnya, proses debugging berjalan lancar tanpa error konfigurasi.

---

