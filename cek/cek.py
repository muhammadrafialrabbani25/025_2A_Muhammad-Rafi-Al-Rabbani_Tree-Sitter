import sys
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

LANG = Language(tspython.language())
parser = Parser(LANG)

BATAS_BARIS = 30
SKIP_DIRS = {"venv", ".venv", ".git", "node_modules", "__pycache__"}


def file_list(folder):
    for path in Path(folder).rglob("*.py"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def cek_todo_fixme(path, tree, kode):
    hasil = []
    q = Query(LANG, '((comment) @c (#match? @c "TODO|FIXME"))')
    for match_id, cap in QueryCursor(q).matches(tree.root_node):
        for node in cap["c"]:
            teks = kode[node.start_byte:node.end_byte].decode(errors="replace")
            hasil.append((node.start_point[0] + 1, teks.strip()))
    return hasil


def cek_fungsi_panjang(path, tree, kode, batas=BATAS_BARIS):
    hasil = []
    q = Query(LANG, "(function_definition name: (identifier) @nama) @fungsi")
    for match_id, cap in QueryCursor(q).matches(tree.root_node):
        fungsi = cap["fungsi"][0]
        nama = cap["nama"][0]
        jumlah = fungsi.end_point[0] - fungsi.start_point[0] + 1
        if jumlah > batas:
            nama_teks = kode[nama.start_byte:nama.end_byte].decode(errors="replace")
            hasil.append((fungsi.start_point[0] + 1, nama_teks, jumlah))
    return hasil


def cari_error_pertama(node):
    if node.is_error or node.is_missing:
        return node
    for child in node.children:
        hasil = cari_error_pertama(child)
        if hasil:
            return hasil
    return None


def cek_file(path):
    try:
        kode = path.read_bytes()
    except Exception as e:
        print(f"Gagal baca {path}: {e}")
        return
    tree = parser.parse(kode)

    todo = cek_todo_fixme(path, tree, kode)
    for baris, teks in todo:
        print(f"[TODO/FIXME] {path}:{baris}: {teks}")

    panjang = cek_fungsi_panjang(path, tree, kode)
    for baris, nama, jumlah in panjang:
        print(f"[FUNGSI PANJANG] {path}:{baris}: '{nama}' ({jumlah} baris, > {BATAS_BARIS})")

    if tree.root_node.has_error:
        node_error = cari_error_pertama(tree.root_node)
        if node_error:
            print(f"[FILE ERROR] {path}: syntax error mulai baris {node_error.start_point[0] + 1}")
        else:
            print(f"[FILE ERROR] {path}: ada error tapi node spesifik tidak ditemukan")


def main():
    if len(sys.argv) < 2:
        print("Pemakaian: python cek.py <folder>")
        sys.exit(1)
    folder = sys.argv[1]
    for path in file_list(folder):
        cek_file(path)


if __name__ == "__main__":
    main()