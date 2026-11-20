# Draf Proposal Proyek — Tree-sitter untuk Pengembangan Web Enterprise

**Nama:** Muhammad Rafi Al Rabbani — NIM 251524025 — Kelas 2A

## 1. Judul
**Pendeteksi Potensi SQL Injection pada Kode Backend Node.js/Express menggunakan Tree-sitter**

## 2. Masalah
Di tim pengembangan web enterprise, query database yang dibangun dengan penggabungan string (bukan parameterized query) adalah penyebab umum kerentanan SQL injection. Developer junior maupun senior sering tidak sadar sudah menulis pola berbahaya seperti `db.query("SELECT * FROM users WHERE id = " + userInput)`, terutama di proyek besar dengan banyak endpoint API. Code review manual untuk pola ini melelahkan dan mudah terlewat, terutama saat deadline sprint mepet.

## 3. Kenapa Tidak Cukup dengan AI Saja
Meminta AI code-review membaca seluruh file dan "mencari SQL injection" hasilnya tidak konsisten antar run, lambat untuk ratusan file sekaligus, dan mahal (biaya API per request) jika dijalankan otomatis setiap push ke repository. Tree-sitter memberi deteksi berbasis struktur sintaks yang deterministik, cepat, gratis dijalankan lokal, dan bisa diintegrasikan sebagai gate otomatis di CI tanpa bergantung pada ketersediaan/biaya API eksternal.

## 4. Bahasa dan Framework Target
JavaScript/TypeScript (Node.js, Express), menggunakan grammar `tree-sitter-javascript` dan `tree-sitter-typescript` (tersedia di PyPI/npm).

## 5. Contoh Kode

**Harus terdeteksi (berbahaya — string concatenation ke query):**
```javascript
db.query("SELECT * FROM users WHERE id = " + req.params.id);
const sql = `DELETE FROM orders WHERE user = ${userId}`;
db.query(sql);
```

**Tidak boleh ikut terdeteksi (aman — parameterized query):**
```javascript
db.query("SELECT * FROM users WHERE id = ?", [req.params.id]);
db.query("SELECT * FROM users WHERE id = $1", [userId]);
```

## 6. Rancangan Query (S-expression)

Mendeteksi pemanggilan `.query(...)` yang argumennya adalah hasil binary concatenation (`+`) atau template literal yang menyisipkan variabel:

```scheme
(call_expression
  function: (member_expression
    property: (property_identifier) @method
    (#eq? @method "query"))
  arguments: (arguments
    [
      (binary_expression operator: "+") @bahaya
      (template_string (template_substitution)) @bahaya
    ]))
```

## 7. Bentuk Output
Laporan terminal berwarna (seperti ESLint) untuk pemakaian lokal developer, plus mode `--json` yang menghasilkan file JSON berisi daftar `{file, baris, kutipan_kode}` agar bisa dipakai sebagai komentar otomatis di pull request (via GitHub Actions) atau dikonsumsi AI coding agent sebagai konteks tambahan saat review.

## 8. Cara Evaluasi
Diuji pada 1 repository open source Express.js berskala menengah (misal salah satu starter template Express + MySQL di GitHub) dan 1 proyek tugas kuliah sendiri yang sengaja disisipkan 10 kasus (5 berbahaya, 5 aman). Evaluasi: hitung berapa dari 10 kasus suntikan yang terdeteksi benar (true positive) dan berapa kasus aman yang salah ditandai (false positive), target akurasi ≥ 80%.

## 9. Rencana Kerja per Minggu & Risiko

- **Minggu 1:** Setup `tree-sitter-javascript`, eksplorasi node `call_expression`/`template_string` dengan Playground, tulis query dasar untuk pola `+` concatenation.
- **Minggu 2:** Tambah dukungan template literal (`` ` ``), tangani kasus `.query()` dipanggil tidak langsung (lewat variabel perantara) — risiko: analisis statis murah tidak bisa melacak alias variabel lintas fungsi, jadi skop dibatasi hanya pola langsung di argumen.
- **Minggu 3:** Bangun output JSON + mode CLI, integrasi contoh GitHub Actions workflow.
- **Minggu 4:** Uji pada repo nyata + proyek kuliah berisi 10 kasus uji, hitung akurasi, perbaiki query berdasarkan false positive yang ditemukan.
- **Minggu 5:** Tulis dokumentasi (README) dan laporan akhir, buffer untuk perbaikan jika akurasi belum mencapai target.

**Risiko utama:** pola string concatenation sangat bervariasi (bisa lewat fungsi helper, lewat spread variable), sehingga false negative sulit dihindari sepenuhnya — proyek ini disebut sebagai alat bantu (assist), bukan jaminan keamanan mutlak.
