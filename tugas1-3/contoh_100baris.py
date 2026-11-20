"""Contoh file Python >=100 baris untuk menguji jelajah.py (Tugas 2)."""

import os
from pathlib import Path

class Mahasiswa:
    def __init__(self, nama, nim, jurusan):
        self.nama = nama
        self.nim = nim
        self.jurusan = jurusan
        self.nilai = []

    def tambah_nilai(self, mata_kuliah, nilai):
        self.nilai.append((mata_kuliah, nilai))

    def rata_rata(self):
        if not self.nilai:
            return 0
        total = 0
        for _, n in self.nilai:
            total += n
        return total / len(self.nilai)

    def __str__(self):
        return f"{self.nama} ({self.nim}) - {self.jurusan}"


class Dosen:
    def __init__(self, nama, nip):
        self.nama = nama
        self.nip = nip
        self.mahasiswa_bimbingan = []

    def bimbing(self, mahasiswa):
        self.mahasiswa_bimbingan.append(mahasiswa)

    def jumlah_bimbingan(self):
        return len(self.mahasiswa_bimbingan)


def buat_mahasiswa_contoh():
    data = [
        ("Rafi", "251524025", "D4 Teknik Informatika"),
        ("Budi", "251524026", "D4 Teknik Informatika"),
        ("Siti", "251524027", "D3 Teknik Komputer"),
    ]
    hasil = []
    for nama, nim, jurusan in data:
        m = Mahasiswa(nama, nim, jurusan)
        hasil.append(m)
    return hasil


def tambahkan_nilai_acak(mahasiswa_list):
    mata_kuliah = ["Algoritma", "Basis Data", "Jaringan", "PLP"]
    nilai_dummy = [80, 85, 90, 75, 88]
    for m in mahasiswa_list:
        for i, mk in enumerate(mata_kuliah):
            nilai = nilai_dummy[i % len(nilai_dummy)]
            m.tambah_nilai(mk, nilai)


def cari_mahasiswa_terbaik(mahasiswa_list):
    terbaik = None
    nilai_tertinggi = -1
    for m in mahasiswa_list:
        rata = m.rata_rata()
        if rata > nilai_tertinggi:
            nilai_tertinggi = rata
            terbaik = m
    return terbaik


def hitung_statistik(mahasiswa_list):
    semua_rata = []
    for m in mahasiswa_list:
        semua_rata.append(m.rata_rata())

    if not semua_rata:
        return {"min": 0, "max": 0, "avg": 0}

    return {
        "min": min(semua_rata),
        "max": max(semua_rata),
        "avg": sum(semua_rata) / len(semua_rata),
    }


def filter_berdasarkan_jurusan(mahasiswa_list, jurusan):
    hasil = []
    for m in mahasiswa_list:
        if m.jurusan == jurusan:
            hasil.append(m)
    return hasil


def urutkan_berdasarkan_nilai(mahasiswa_list):
    return sorted(mahasiswa_list, key=lambda m: m.rata_rata(), reverse=True)


def cetak_laporan(mahasiswa_list):
    print("=== Laporan Mahasiswa ===")
    for m in mahasiswa_list:
        print(f"{m} - rata-rata: {m.rata_rata():.2f}")


def main():
    mahasiswa_list = buat_mahasiswa_contoh()
    tambahkan_nilai_acak(mahasiswa_list)

    dosen = Dosen("Pak Agus", "198001012005011001")
    for m in mahasiswa_list:
        dosen.bimbing(m)

    print(f"Dosen {dosen.nama} membimbing {dosen.jumlah_bimbingan()} mahasiswa")

    terbaik = cari_mahasiswa_terbaik(mahasiswa_list)
    print(f"Mahasiswa terbaik: {terbaik}")

    statistik = hitung_statistik(mahasiswa_list)
    print(f"Statistik nilai: {statistik}")

    informatika = filter_berdasarkan_jurusan(mahasiswa_list, "D4 Teknik Informatika")
    print(f"Jumlah mahasiswa Informatika: {len(informatika)}")

    urutan = urutkan_berdasarkan_nilai(mahasiswa_list)
    cetak_laporan(urutan)


if __name__ == "__main__":
    main()