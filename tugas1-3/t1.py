import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

contoh = {
    "fungsi": b"def tambah(a, b):\n    return a + b\n",
    "if_else": b"if x > 0:\n    print('positif')\nelse:\n    print('negatif')\n",
    "kelas": b"class Hewan:\n    def suara(self):\n        print('Suaranya...')\n",
}

def cetak_pohon(node, indent=0):
    print("  " * indent + f"{node.type} [{node.start_point} - {node.end_point}]" + (f" field={node.grammar_name}" if False else ""))
    for child in node.children:
        cetak_pohon(child, indent + 1)

for nama, kode in contoh.items():
    print(f"\n===== {nama} =====")
    tree = parser.parse(kode)
    print(tree.root_node)
    print("\n-- detail pohon --")
    cetak_pohon(tree.root_node)

print("\n===== RUSAK (tanpa titik dua) =====")
rusak = b"def tambah(a, b)\n    return a + b\n"
tree_rusak = parser.parse(rusak)
print(tree_rusak.root_node)
print("\n-- detail pohon --")
cetak_pohon(tree_rusak.root_node)

print("\n===== RUSAK (tanpa tutup kurung) =====")
rusak2 = b"def tambah(a, b:\n    return a + b\n"
tree_rusak2 = parser.parse(rusak2)
print(tree_rusak2.root_node)
print("\n-- detail pohon --")
cetak_pohon(tree_rusak2.root_node)