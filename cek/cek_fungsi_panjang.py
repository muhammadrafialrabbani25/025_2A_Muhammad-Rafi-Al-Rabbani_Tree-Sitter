import os
import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

TARGET_DIR = r"C:\Users\alrab\Documents\requests"
BATAS_BARIS = 50

parser = Parser(Language(tspython.language()))

def cari_fungsi_panjang(root, batas=BATAS_BARIS):
    hasil = []
    for dirpath, _, filenames in os.walk(root):
        if ".git" in dirpath:
            continue
        for fname in filenames:
            if not fname.endswith(".py"):
                continue
            path = os.path.join(dirpath, fname)
            try:
                with open(path, "rb") as f:
                    kode = f.read()
                tree = parser.parse(kode)
                cek_node(tree.root_node, path, batas, hasil)
            except Exception as e:
                print(f"Gagal parse {path}: {e}")
    return hasil

def cek_node(node, path, batas, hasil):
    if node.type == "function_definition":
        jumlah_baris = node.end_point[0] - node.start_point[0] + 1
        if jumlah_baris > batas:
            nama_node = node.child_by_field_name("name")
            nama = nama_node.text.decode() if nama_node else "?"
            hasil.append((path, nama, node.start_point[0] + 1, jumlah_baris))
    for child in node.children:
        cek_node(child, path, batas, hasil)

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else TARGET_DIR
    temuan = cari_fungsi_panjang(root)
    print(f"Ditemukan {len(temuan)} fungsi > {BATAS_BARIS} baris di {root}\n")
    for path, nama, baris_mulai, jumlah in sorted(temuan, key=lambda x: -x[3]):
        print(f"{path}:{baris_mulai}: fungsi '{nama}' ({jumlah} baris)")