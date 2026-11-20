def proses_data_panjang(data):
    hasil = []
    total = 0
    minimum = None
    maksimum = None

    for item in data:
        if item is None:
            continue
        if not isinstance(item, (int, float)):
            continue

        total += item

        if minimum is None or item < minimum:
            minimum = item
        if maksimum is None or item > maksimum:
            maksimum = item

        if item % 2 == 0:
            hasil.append(("genap", item))
        else:
            hasil.append(("ganjil", item))

    rata_rata = total / len(hasil) if hasil else 0

    ringkasan = {
        "total": total,
        "rata_rata": rata_rata,
        "minimum": minimum,
        "maksimum": maksimum,
        "jumlah_item": len(hasil),
    }

    for label, nilai in hasil:
        print(f"{label}: {nilai}")

    print("Ringkasan:", ringkasan)

    return ringkasan