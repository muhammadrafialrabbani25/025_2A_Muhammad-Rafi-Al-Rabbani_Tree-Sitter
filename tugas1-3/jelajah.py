import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

def jelajah(node, depth=0):
    if node.is_named:
        field = ""
        print("  " * depth + f"{node.type} ({node.start_point[0]+1}:{node.start_point[1]} - {node.end_point[0]+1}:{node.end_point[1]})")
    for child in node.children:
        jelajah(child, depth + 1)

if __name__ == "__main__":
    path = sys.argv[1]
    with open(path, "rb") as f:
        kode = f.read()
    tree = parser.parse(kode)
    jelajah(tree.root_node)