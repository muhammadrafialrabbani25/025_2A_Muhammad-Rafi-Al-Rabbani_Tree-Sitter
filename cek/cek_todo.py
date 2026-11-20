import os
import sys

TARGET_DIR = r"C:\Users\alrab\Documents\requests"

def scan_todo(root):
    hasil = []
    for dirpath, _, filenames in os.walk(root):
        if ".git" in dirpath:
            continue
        for fname in filenames:
            if not fname.endswith(".py"):
                continue
            path = os.path.join(dirpath, fname)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f, start=1):
                        if "TODO" in line or "FIXME" in line:
                            hasil.append((path, i, line.strip()))
            except Exception as e:
                print(f"Gagal baca {path}: {e}")
    return hasil

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else TARGET_DIR
    temuan = scan_todo(root)
    print(f"Ditemukan {len(temuan)} TODO/FIXME di {root}\n")
    for path, lineno, isi in temuan:
        print(f"{path}:{lineno}: {isi}")