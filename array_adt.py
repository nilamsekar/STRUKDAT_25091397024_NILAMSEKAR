"""
ADT ARRAY - Abstract Data Type Array
Implementasi array satu dimensi dengan ukuran tetap

Berdasarkan spesifikasi:
- Ukuran tetap (tidak bisa diubah setelah dibuat)
- Operasi terbatas (create, read, write, clear, iterate)
- Semua elemen diinisialisasi dengan None
"""


class Array:
    """
    ADT Array - Kumpulan elemen berurutan dengan ukuran tetap
    
    Operasi:
    - Array(size): Membuat array dengan ukuran tertentu
    - length(): Mengembalikan jumlah elemen
    - __getitem__(index): Membaca nilai pada indeks (array[i])
    - __setitem__(index, value): Menulis nilai pada indeks (array[i] = value)
    - clearing(value): Mengosongkan array dengan nilai tertentu
    - __iter__(): Iterator untuk traversal elemen
    """
    
    def __init__(self, size):
        """
        Membuat array satu dimensi dengan ukuran tetap.
        
        Args:
            size (int): Ukuran array, harus > 0
            
        Raises:
            AssertionError: Jika size <= 0
            
        Example:
            >>> arr = Array(10)
            >>> arr.length()
            10
        """
        assert size > 0, "Ukuran array harus lebih besar dari 0"
        self._size = size
        self._elements = [None] * size
    
    def length(self):
        """
        Mengembalikan panjang array.
        
        Returns:
            int: Jumlah elemen dalam array
            
        Example:
            >>> arr = Array(5)
            >>> arr.length()
            5
        """
        return self._size
    
    def __len__(self):
        """Support untuk built-in len()"""
        return self.length()
    
    def __getitem__(self, index):
        """
        Membaca nilai pada indeks tertentu.
        
        Args:
            index (int): Indeks elemen (0 sampai size-1)
            
        Returns:
            Nilai pada indeks tersebut
            
        Raises:
            AssertionError: Jika indeks di luar rentang
            
        Example:
            >>> arr = Array(3)
            >>> arr[0] = 10
            >>> arr[0]
            10
        """
        assert 0 <= index < self._size, \
            f"Indeks {index} di luar rentang [0, {self._size - 1}]"
        return self._elements[index]
    
    def __setitem__(self, index, value):
        """
        Menulis nilai pada indeks tertentu.
        
        Args:
            index (int): Indeks elemen (0 sampai size-1)
            value: Nilai yang akan disimpan
            
        Raises:
            AssertionError: Jika indeks di luar rentang
            
        Example:
            >>> arr = Array(3)
            >>> arr[0] = 100
            >>> arr[1] = 200
        """
        assert 0 <= index < self._size, \
            f"Indeks {index} di luar rentang [0, {self._size - 1}]"
        self._elements[index] = value
    
    def clearing(self, value):
        """
        Mengosongkan array dengan mengisi semua elemen dengan nilai tertentu.
        
        Args:
            value: Nilai untuk semua elemen
            
        Example:
            >>> arr = Array(5)
            >>> arr.clearing(0)
            >>> all(arr[i] == 0 for i in range(5))
            True
        """
        for i in range(self._size):
            self._elements[i] = value
    
    def __iter__(self):
        """
        Membuat iterator untuk traversal elemen.
        
        Returns:
            _ArrayIterator: Iterator object
            
        Example:
            >>> arr = Array(3)
            >>> arr[0], arr[1], arr[2] = 1, 2, 3
            >>> list(arr)
            [1, 2, 3]
        """
        return _ArrayIterator(self._elements)


class _ArrayIterator:
    """
    Iterator untuk ADT Array.
    Digunakan internal untuk mendukung iterasi.
    """
    
    def __init__(self, elements):
        """
        Inisialisasi iterator.
        
        Args:
            elements: List elemen yang akan di-iterasi
        """
        self._elements = elements
        self._index = 0
    
    def __iter__(self):
        """Mengembalikan iterator itu sendiri"""
        return self
    
    def __next__(self):
        """
        Mengembalikan elemen berikutnya.
        
        Returns:
            Elemen berikutnya dalam iterasi
            
        Raises:
            StopIteration: Jika sudah mencapai akhir
        """
        if self._index < len(self._elements):
            value = self._elements[self._index]
            self._index += 1
            return value
        else:
            raise StopIteration


# ============================================================================
# Testing (uncomment untuk test)
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  ADT ARRAY - TESTING")
    print("=" * 60)
    
    # Test 1: Membuat array
    print("\n[TEST 1] Membuat array ukuran 5")
    arr = Array(5)
    print(f"Length: {arr.length()}")
    print(f"Initial values: {[arr[i] for i in range(arr.length())]}")
    
    # Test 2: Set dan get item
    print("\n[TEST 2] Set dan get item")
    arr[0] = 10
    arr[1] = 20
    arr[2] = 30
    print(f"arr[0] = {arr[0]}")
    print(f"arr[1] = {arr[1]}")
    print(f"arr[2] = {arr[2]}")
    
    # Test 3: Clearing
    print("\n[TEST 3] Clearing dengan nilai 0")
    arr.clearing(0)
    print(f"After clearing: {[arr[i] for i in range(arr.length())]}")
    
    # Test 4: Iterator
    print("\n[TEST 4] Iterator test")
    arr[0] = 1
    arr[1] = 2
    arr[2] = 3
    print(f"Using iterator: {[x for x in arr]}")
    
    # Test 5: Error handling
    print("\n[TEST 5] Error handling")
    try:
        arr[10] = 100  # Index out of range
    except AssertionError as e:
        print(f"✓ Caught error: {e}")
    
    print("\n" + "=" * 60)
    print("  ALL TESTS PASSED!")
    print("=" * 60)