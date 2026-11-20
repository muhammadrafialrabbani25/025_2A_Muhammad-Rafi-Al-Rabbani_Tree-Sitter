# cek.py

CLI sederhana untuk menganalisis file Python dalam sebuah folder menggunakan tree-sitter.

## Fitur
1. Mendeteksi komentar `TODO`/`FIXME`
2. Mendeteksi fungsi dengan body > 30 baris
3. Mendeteksi file dengan syntax error (node ERROR/MISSING)

## Instalasi
pip install tree-sitter tree-sitter-python

## Cara pakai
python cek.py <folder>

Contoh:
python cek.py C:\Users\alrab\Documents\requests

## Catatan
- Folder venv/, .git/, node_modules/, __pycache__/ otomatis dilewati.
- Diuji di folder cek/uji/ (3 file kecil) dan di repo nyata psf/requests (65+ fungsi panjang, 7 TODO, 0 file error — dicocokkan manual pada 2 file acak: adapters.py:634 dan hooks.py:29).