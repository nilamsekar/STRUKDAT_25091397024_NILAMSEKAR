# ============================================================
# 1. HAPUS DUPLIKAT (Pertahankan Urutan Kemunculan Pertama)
# ============================================================
def remove_duplicates(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

# ============================================================
# 2. INTERSECTION DUA ARRAY
# ============================================================
def intersection(list1, list2):
    set2 = set(list2)
    return list(set(item for item in list1 if item in set2))

# ============================================================
# 3. ANAGRAM CHECK
# ============================================================
def is_anagram(str1, str2):
    str1 = str1.replace(" ", "").lower()
    str2 = str2.replace(" ", "").lower()
    
    if len(str1) != len(str2):
        return False
    
    count = {}
    for char in str1:
        count[char] = count.get(char, 0) + 1
    for char in str2:
        count[char] = count.get(char, 0) - 1
    
    return all(v == 0 for v in count.values())

# ============================================================
# 4. FIRST RECURRING CHARACTER
# ============================================================
def first_recurring_char(s):
    seen = set()
    for char in s:
        if char in seen:
            return char
        seen.add(char)
    return None

# ============================================================
# 5. SIMULASI BUKU TELEPON
# ============================================================
def phone_book():
    contacts = {}
    
    while True:
        print("\n===== BUKU TELEPON =====")
        print("1. Tambah Kontak")
        print("2. Cari Kontak")
        print("3. Tampilkan Semua Kontak")
        print("4. Keluar")
        
        pilihan = input("Pilih menu (1-4): ").strip()
        
        if pilihan == "1":
            nama = input("Nama: ").strip()
            nomor = input("Nomor: ").strip()
            if nama and nomor:
                contacts[nama.lower()] = {"nama": nama, "nomor": nomor}
                print(f"✓ Kontak '{nama}' berhasil ditambahkan!")
            else:
                print("✗ Nama dan nomor tidak boleh kosong.")
        
        elif pilihan == "2":
            keyword = input("Cari nama: ").strip().lower()
            found = {k: v for k, v in contacts.items() if keyword in k}
            if found:
                print(f"\nDitemukan {len(found)} kontak:")
                for v in found.values():
                    print(f"  {v['nama']:<20} : {v['nomor']}")
            else:
                print("✗ Kontak tidak ditemukan.")
        
        elif pilihan == "3":
            if contacts:
                print(f"\nTotal kontak: {len(contacts)}")
                print("-" * 35)
                for v in sorted(contacts.values(), key=lambda x: x['nama']):
                    print(f"  {v['nama']:<20} : {v['nomor']}")
            else:
                print("✗ Buku telepon masih kosong.")
        
        elif pilihan == "4":
            print("Sampai jumpa!")
            break
        
        else:
            print("✗ Pilihan tidak valid.")


# ============================================================
# DEMO / TESTING
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("1. REMOVE DUPLICATES")
    print("=" * 50)
    data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    print(f"Input : {data}")
    print(f"Output: {remove_duplicates(data)}")

    print("\n" + "=" * 50)
    print("2. INTERSECTION DUA ARRAY")
    print("=" * 50)
    a = [1, 2, 3, 4, 5]
    b = [3, 4, 5, 6, 7]
    print(f"List 1: {a}")
    print(f"List 2: {b}")
    print(f"Irisan: {intersection(a, b)}")

    print("\n" + "=" * 50)
    print("3. ANAGRAM CHECK")
    print("=" * 50)
    pasangan = [("listen", "silent"), ("hello", "world"), ("Astronomer", "Moon starer")]
    for s1, s2 in pasangan:
        hasil = is_anagram(s1, s2)
        print(f"'{s1}' & '{s2}' => {'Anagram ✓' if hasil else 'Bukan Anagram ✗'}")

    print("\n" + "=" * 50)
    print("4. FIRST RECURRING CHARACTER")
    print("=" * 50)
    strings = ["abcdca", "abcd", "aabbcc", "ABCA"]
    for s in strings:
        hasil = first_recurring_char(s)
        print(f"'{s}' => {f'Karakter: {hasil!r}' if hasil else 'Tidak ada'}")

    print("\n" + "=" * 50)
    print("5. SIMULASI BUKU TELEPON")
    print("=" * 50)
    phone_book()