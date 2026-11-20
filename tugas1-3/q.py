import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

parser = Parser(Language(tspython.language()))

with open("contoh_100baris.py", "rb") as f:
    kode = f.read()
tree = parser.parse(kode)
LANG = Language(tspython.language())

print("===== 1. Nama fungsi + jumlah parameter =====")
q1 = Query(LANG, "(function_definition name: (identifier) @nama parameters: (parameters) @params)")
for match_id, cap in QueryCursor(q1).matches(tree.root_node):
    nama = cap["nama"][0]
    params = cap["params"][0]
    nama_teks = kode[nama.start_byte:nama.end_byte].decode()
    jumlah_param = params.named_child_count
    print(f"{nama_teks}: {jumlah_param} parameter (baris {nama.start_point[0]+1})")

print("\n===== 2. Pemanggilan print(...) =====")
q2 = Query(LANG, '(call function: (identifier) @fn arguments: (argument_list) @args (#eq? @fn "print"))')
for match_id, cap in QueryCursor(q2).matches(tree.root_node):
    args = cap["args"][0]
    print(f"print(...) di baris {args.start_point[0]+1}")

print("\n===== 3. Daftar modul import =====")
q3 = Query(LANG, """
[
  (import_statement name: (dotted_name) @modul)
  (import_from_statement module_name: (dotted_name) @modul)
]
""")
for match_id, cap in QueryCursor(q3).matches(tree.root_node):
    modul = cap["modul"][0]
    teks = kode[modul.start_byte:modul.end_byte].decode()
    print(f"import: {teks} (baris {modul.start_point[0]+1})")