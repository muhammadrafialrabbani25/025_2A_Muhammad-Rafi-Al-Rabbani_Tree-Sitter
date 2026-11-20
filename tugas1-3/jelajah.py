import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

def jelajah(node, depth=0, field_name=None):
    if node.is_named:
        prefix = f"{field_name}: " if field_name else ""
        posisi = f"({node.start_point[0]+1}:{node.start_point[1]} - {node.end_point[0]+1}:{node.end_point[1]})"
        print("  " * depth + f"{prefix}{node.type} {posisi}")
    for i in range(node.child_count):
        child = node.child(i)
        fname = node.field_name_for_child(i)
        jelajah(child, depth + 1, fname)

if __name__ == "__main__":
    path = sys.argv[1]
    with open(path, "rb") as f:
        kode = f.read()
    tree = parser.parse(kode)
    jelajah(tree.root_node)