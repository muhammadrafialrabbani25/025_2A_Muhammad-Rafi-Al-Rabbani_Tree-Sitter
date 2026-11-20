import os
import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

TARGET_DIR = r"C:\Users\alrab\Documents\requests"

parser = Parser(Language(tspython.language()))

def ada_error(node):
    if node.type == "ERROR" or node.is_missing:
        return True
    for child in node.children:
        if ada_error(child):
            return True
    return False

def cari_file_error(root):
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
                if ada_error(tree.root_node):
                    hasil.append(path)
            except Exception as e:
                print(f"Gagal parse {path}: {e}")
    return hasil

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else TARGET_DIR
    temuan = cari_file_error(root)
    print(f"Ditemukan {len(temuan)} file dengan ERROR/MISSING node di {root}\n")
    for path in temuan:
        print(path)