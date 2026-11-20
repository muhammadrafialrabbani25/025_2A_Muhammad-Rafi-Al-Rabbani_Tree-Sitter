# Laporan Tugas Tree-sitter — Programming Pragmatics

**Nama:** Muhammad Rafi Al Rabbani
**NIM:** 251524025
**Kelas:** 2A — D4 Teknik Informatika, Polban

---

## Tugas 1 — Membaca Pohon (`tugas1-3/t1.py`)

Memparsing 3 potongan kode Python (fungsi, if/else, kelas dengan 1 method) dengan `tree-sitter-python`, membandingkan pohon hasil dengan prediksi manual, menunjukkan node anonim, dan menguji kode rusak.

**Hasil:**
```
(module (function_definition name: (identifier) parameters: (parameters (identifier) (identifier)) body: (block (return_statement (binary_operator left: (identifier) right: (identifier))))))
```
Node anonim yang ditemukan (tidak punya field, tercetak tanpa label): `def`, `(`, `)`, `,`, `:`, `+`.

Kode dirusak dengan menghapus `:` setelah parameter fungsi:
```python
rusak = b"def tambah(a, b)\n    return a + b\n"
```
Hasil parse memunculkan node `ERROR` menggantikan `function_definition`, membuktikan parser tetap menghasilkan pohon meski sintaks tidak valid (error recovery).

**Kendala & solusi:** `ModuleNotFoundError: tree_sitter_python` karena paket belum terpasang di environment Python yang dipakai menjalankan skrip. Solusi: `python -m pip install tree-sitter tree-sitter-python tree-sitter-javascript`, dicek dengan `python -c "import sys; print(sys.executable)"` untuk memastikan interpreter yang sama dipakai untuk install dan run.

---

## Tugas 2 — Penjelajah Node (`tugas1-3/jelajah.py`)

Skrip rekursif yang mencetak setiap node bernama beserta kedalaman (indentasi), tipe, posisi baris:kolom, dan nama field (jika ada), menggunakan `node.field_name_for_child(i)`.

Diuji pada file `contoh_100baris.py` (129 baris, berisi 2 class dan beberapa fungsi). Potongan hasil:
```
class_definition (4:0 - 23:59)
  name: identifier (4:6 - 4:15)
  body: block (5:4 - 23:59)
    function_definition (5:4 - 9:23)
      name: identifier (5:8 - 5:16)
      parameters: parameters (5:16 - 5:42)
      body: block (6:8 - 9:23)
        expression_statement (6:8 - 6:24)
          assignment (6:8 - 6:24)
            left: attribute (6:8 - 6:17)
            right: identifier (6:20 - 6:24)
```
Semua field (`name:`, `body:`, `left:`, `right:`, `function:`, dll) tercetak sesuai struktur grammar Python.

**Kendala & solusi:** Awalnya indeks anak node yang dikirim ke `field_name_for_child(i)` harus indeks di `node.children` (semua anak), bukan indeks di `named_children`, kalau salah field tidak muncul.

---

## Tugas 3 — Query Pertama (`tugas1-3/q.py`)

Tiga query `.scm`/inline untuk: (1) nama fungsi + jumlah parameter, (2) pemanggilan `print(...)` spesifik dengan predicate `#eq?`, (3) daftar modul dari `import`/`from...import`.

**Hasil (ringkas):**
- 15 fungsi terdeteksi dengan jumlah parameter masing-masing (mis. `__init__`: 4 parameter, `main`: 0 parameter)
- 6 pemanggilan `print(...)` ditemukan pada baris 102, 104, 115, 118, 121, 124
- 2 modul import: `os` (baris 3), `pathlib` (baris 4)

Dicocokkan manual dengan isi file `contoh_100baris.py`: jumlah fungsi, jumlah pemanggilan print, dan jumlah import sesuai dengan yang tertulis di kode sumber.

**Kendala & solusi:** Draf awal query salah sasaran (mendeteksi semua pemanggilan fungsi, bukan khusus `print`, dan belum menghitung parameter). Diperbaiki dengan memakai `QueryCursor(...).matches()` (bukan `captures()`) untuk pasangan nama+parameter, `named_child_count` untuk menghitung parameter, dan predicate `(#eq? @fn "print")` untuk membatasi hanya pemanggilan `print`.

---

## Tugas 4 — Grammar Kecil `tree-sitter-filter` (bobot 20)

Grammar DSL filter sederhana untuk query enterprise (`status = "aktif" and umur > 17`), mendukung: string, number, boolean, operator perbandingan (`=`, `!=`, `>`, `<`, `>=`, `<=`), logika `and`/`or`/`not` dengan prioritas (`prec`), kurung, serta `in` dan `contains`.

**8 test case di `test/corpus/filter.txt`, semua lolos (100%):**
```
1. ✓ Perbandingan sederhana
2. ✓ And dua kondisi
3. ✓ Or dua kondisi
4. ✓ Prioritas and lebih tinggi dari or
5. ✓ In expression
6. ✓ Contains expression
7. ✓ Not expression
8. ✓ Boolean value
Total parses: 8; successful parses: 8; success percentage: 100.00%
```

**Kendala & solusi:**
1. `npx tree-sitter generate` gagal dengan `ReferenceError: module is not defined` karena `package.json` punya `"type": "module"` (ES module), sedangkan `grammar.js` memakai sintaks CommonJS (`module.exports`). Solusi: hapus baris `"type": "module"` dari `package.json`.
2. Menambahkan `not_expression` menyebabkan *unresolved conflict* dengan `comparison_expression` (tree-sitter bingung antara `not (a = b)` vs `(not a) = b`). Solusi: beri `not_expression` prioritas di antara `and`/`or` dan `comparison` (`prec(3, ...)` untuk `not`, `prec.left(4, ...)` untuk `comparison`/`in`/`contains`), sehingga `not` membungkus seluruh ekspresi perbandingan, bukan cuma identifier.

---

## Tugas 5 — Syntax Highlighting (`tree-sitter-filter/queries/highlights.scm`)

Query highlight untuk kata kunci (`and`, `or`, `not`, `in`, `contains`), operator, string, number, boolean (`@constant.builtin`), dan field identifier pada posisi kiri perbandingan (`@property`) vs identifier biasa (`@variable`).

Diverifikasi dengan `npx tree-sitter query queries/highlights.scm examples/contoh.filter` pada ekspresi:
```
not status = "aktif" and umur > 17 or (kategori in ["a", "b"] and nama contains "budi") and aktif = true
```
Semua token ter-capture dengan benar, contoh:
```
capture: keyword   text: `not`
capture: property  text: `status`
capture: variable  text: `status`
capture: operator  text: `=`
capture: string     text: `"aktif"`
capture: constant.builtin  text: `true`
```

**Kendala & solusi:** Perintah `tree-sitter highlight` tidak menampilkan warna sama sekali di terminal VS Code (meski exit code 0 dan parse bersih). Karena `tree-sitter query` menampilkan nama capture secara eksplisit tanpa bergantung pada rendering warna terminal, dipakai sebagai bukti verifikasi yang lebih reliable untuk laporan ini.

---

## Tugas 6 — Tool Analisis Nyata (`cek/cek.py`)

CLI `python cek.py <folder>` yang memakai tree-sitter untuk melaporkan: (1) komentar TODO/FIXME, (2) fungsi dengan body > 30 baris, (3) file dengan syntax error (node `ERROR`/`is_missing`).

**Validasi di `cek/uji/` (3 file buatan sendiri):**
```
[TODO/FIXME] cek\uji\ada_todo.py:2: # TODO: perbaiki ini nanti
[FUNGSI PANJANG] cek\uji\fungsi_panjang.py:1: 'proses_data_panjang' (40 baris, > 30)
[FILE ERROR] cek\uji\rusak.py: syntax error mulai baris 1
```
Ketiga fitur terbukti jalan sebelum diuji pada repo nyata.

**Diuji pada repo open source `psf/requests`:**
- 7 komentar TODO/FIXME ditemukan
- 65+ fungsi dengan body > 30 baris
- 0 file dengan syntax error (diharapkan, karena kode production-grade valid secara sintaks)

**Verifikasi manual pada 2 file acak:**
- `src/requests/adapters.py` baris 634: `def send(...)` berakhir di baris 748 (`return self.build_response(request, resp)`) → 748 − 634 + 1 = **115 baris**, cocok dengan output `cek.py`.
- `src/requests/hooks.py` baris 29: ditemukan `# TODO: response is the only one` persis sesuai laporan `cek.py`.

**Kendala & solusi:** Desain awal memakai 3 skrip terpisah per fitur dengan path target di-hardcode. Diperbaiki menjadi 1 CLI `cek.py <folder>` sesuai spesifikasi, dengan ambang fungsi panjang disesuaikan ke >30 baris (bukan >50), serta melewati folder `.git/`, `venv/`, `node_modules/`, `__pycache__/` agar tidak lambat di repo besar.

---

## Catatan Penggunaan AI

Seluruh tugas dikerjakan dengan bantuan AI coding agent (Claude) untuk menyusun kerangka skrip, grammar, dan query, sambil tetap menjalankan setiap perintah secara manual di laptop sendiri dan memverifikasi hasilnya.

**Kesalahan AI yang ditemukan dan cara verifikasi:**
1. **Tugas 3** — draf query awal dari AI salah sasaran: mendeteksi *semua* pemanggilan fungsi dan literal string generik, padahal instruksi resmi meminta query yang lebih spesifik (jumlah parameter per fungsi, pemanggilan `print(...)` saja, dan daftar modul `import`). Dibuktikan dengan membandingkan ulang isi dokumen instruksi resmi (`Panduan Detail Penugasan`) terhadap output query lama, lalu query ditulis ulang dan hasilnya dicocokkan manual dengan jumlah fungsi, `print()`, dan `import` yang benar-benar ada di `contoh_100baris.py`.
2. **Tugas 5** — AI awalnya menyarankan `not_expression` dengan prioritas yang sama level dengan `comparison_expression`, menyebabkan `tree-sitter generate` gagal dengan *unresolved conflict* (parser salah mengelompokkan `not status = "aktif"` menjadi `(not status) = "aktif"`). Dibuktikan lewat pesan error `tree-sitter generate` yang eksplisit menunjukkan 2 interpretasi yang bentrok, kemudian diperbaiki dengan menaikkan prioritas `not` di antara `and`/`or` dan `comparison`, dan test case baru (`not status = "aktif"`) ditambahkan untuk memverifikasi pohon yang dihasilkan sudah benar.

---
