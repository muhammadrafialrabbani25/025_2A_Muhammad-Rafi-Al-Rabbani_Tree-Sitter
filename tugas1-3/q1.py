import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

parser = Parser(Language(tspython.language()))

with open("tugas1-3/contoh_100baris.py", "rb") as f:
    kode = f.read()
tree = parser.parse(kode)

queries = ["query1_function_def.scm", "query2_function_call.scm", "query3_string.scm"]

for qfile in queries:
    print(f"\n===== {qfile} =====")
    with open(f"tugas1-3/{qfile}") as f:
        query_text = f.read()
    query = Query(Language(tspython.language()), query_text)
    cursor = QueryCursor(query)
    matches = cursor.matches(tree.root_node)
    for match_id, captures in matches:
        for name, nodes in captures.items():
            for node in nodes:
                teks = kode[node.start_byte:node.end_byte].decode()
                print(f"{name}: {teks} (baris {node.start_point[0]+1})")