"""
Advanced Linked Lists - Implementasi Lengkap
Sumber: Chapter 9 - Advanced Linked Lists (Struktur Data Lanjut)

Topik:
1. Doubly Linked List (DLL)
2. Circular Linked List
3. Multi-Linked List (Student Records & Sparse Matrix)
4. Complex Iterator (Sparse Matrix Iterator)
5. Text Editor Buffer ADT
"""

# ============================================================
# BAGIAN 1: DOUBLY LINKED LIST (DLL)
# ============================================================

class DListNode:
    """Node untuk Doubly Linked List dengan pointer prev dan next."""
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class DoublyLinkedList:
    """
    Doubly Linked List dengan operasi:
    - Traversal forward dan reverse O(n)
    - Insert sorted O(n)
    - Delete O(1) jika referensi node diketahui
    """

    def __init__(self):
        self.head = None
        self.tail = None

    def forward_traversal(self):
        """Traversal dari head ke tail. O(n)"""
        cur = self.head
        result = []
        while cur is not None:
            result.append(cur.data)
            cur = cur.next
        return result

    def reverse_traversal(self):
        """Traversal dari tail ke head. O(n) — lebih efisien dari Singly List."""
        cur = self.tail
        result = []
        while cur is not None:
            result.append(cur.data)
            cur = cur.prev
        return result

    def insert_sorted(self, value):
        """
        Insert node dengan nilai terurut (sorted ascending).
        4 kasus: empty, depan, belakang, tengah.
        """
        new_node = DListNode(value)

        if self.head is None:
            # Kasus 1: List kosong
            self.head = self.tail = new_node

        elif value < self.head.data:
            # Kasus 2: Insert di depan
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        elif value > self.tail.data:
            # Kasus 3: Insert di belakang
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        else:
            # Kasus 4: Insert di tengah
            node = self.head
            while node.data < value:
                node = node.next
            new_node.next = node
            new_node.prev = node.prev
            node.prev.next = new_node
            node.prev = new_node

    def delete_node(self, node):
        """
        Hapus node tertentu. O(1) jika referensi node diketahui.
        Tidak perlu tracking predecessor karena ada .prev.
        """
        if node is self.head and node is self.tail:
            # Satu-satunya node
            self.head = self.tail = None
        elif node is self.head:
            self.head = self.head.next
            self.head.prev = None
        elif node is self.tail:
            self.tail = self.tail.prev
            self.tail.next = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev


# ============================================================
# BAGIAN 2: CIRCULAR LINKED LIST
# ============================================================

class CListNode:
    """Node untuk Circular Linked List."""
    def __init__(self, data):
        self.data = data
        self.next = None


class CircularLinkedList:
    """
    Circular Linked List: node terakhir menunjuk kembali ke node pertama.
    - Tidak ada NULL terminator
    - listRef menunjuk ke NODE TERAKHIR
    - Akses cepat: first = listRef.next, last = listRef
    - Insert depan/belakang: O(1)
    """

    def __init__(self):
        self.list_ref = None  # Menunjuk ke node terakhir

    def traverse(self):
        """Traversal menggunakan alias check, bukan NULL check."""
        result = []
        if self.list_ref is None:
            return result
        cur = self.list_ref
        done = False
        while not done:
            cur = cur.next
            result.append(cur.data)
            done = (cur is self.list_ref)
        return result

    def search(self, target):
        """
        Cari nilai target. Early exit jika list sorted dan target < current.
        """
        cur = self.list_ref
        done = (self.list_ref is None)
        while not done:
            cur = cur.next
            if cur.data == target:
                return True
            done = (cur is self.list_ref) or (cur.data > target)
        return False

    def insert(self, value):
        """
        Insert node ke circular list (4 kasus):
        1. Empty
        2. Depan
        3. Belakang
        4. Tengah (sorted)
        """
        new_node = CListNode(value)

        if self.list_ref is None:
            # Kasus 1: Empty
            self.list_ref = new_node
            new_node.next = new_node

        elif value <= self.list_ref.next.data:
            # Kasus 2: Insert di depan
            new_node.next = self.list_ref.next
            self.list_ref.next = new_node

        elif value > self.list_ref.data:
            # Kasus 3: Insert di belakang
            new_node.next = self.list_ref.next
            self.list_ref.next = new_node
            self.list_ref = new_node

        else:
            # Kasus 4: Insert di tengah (sorted)
            cur = self.list_ref.next
            while cur.next is not self.list_ref and cur.next.data < value:
                cur = cur.next
            new_node.next = cur.next
            cur.next = new_node


# ============================================================
# BAGIAN 3: MULTI-LINKED LIST
# ============================================================

# --- 3a. Student Records (Multiple Chains) ---

class StudentMListNode:
    """
    Node dengan MULTIPLE link fields.
    1 node fisik → multiple logical views (by ID & by Name).
    """
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.next_by_id = None    # Chain sorted by ID
        self.next_by_name = None  # Chain sorted by Name

    def __repr__(self):
        return f"Student(id={self.student_id}, name={self.name})"


class StudentMultiList:
    """
    Multi-Linked List untuk Student Records.
    Satu koleksi node, dua chain (by ID dan by Name).
    Keuntungan: hemat memori, akses fleksibel.
    """

    def __init__(self):
        self.head_by_id = None
        self.head_by_name = None

    def insert(self, student_id, name):
        """Insert 1 node instance ke SEMUA chains."""
        new_node = StudentMListNode(student_id, name)

        # Insert ke chain by ID (sorted ascending)
        if self.head_by_id is None or student_id < self.head_by_id.student_id:
            new_node.next_by_id = self.head_by_id
            self.head_by_id = new_node
        else:
            cur = self.head_by_id
            while cur.next_by_id and cur.next_by_id.student_id < student_id:
                cur = cur.next_by_id
            new_node.next_by_id = cur.next_by_id
            cur.next_by_id = new_node

        # Insert ke chain by Name (sorted ascending)
        if self.head_by_name is None or name < self.head_by_name.name:
            new_node.next_by_name = self.head_by_name
            self.head_by_name = new_node
        else:
            cur = self.head_by_name
            while cur.next_by_name and cur.next_by_name.name < name:
                cur = cur.next_by_name
            new_node.next_by_name = cur.next_by_name
            cur.next_by_name = new_node

    def get_by_id(self):
        """Traversal chain sorted by ID."""
        result, cur = [], self.head_by_id
        while cur:
            result.append(cur)
            cur = cur.next_by_id
        return result

    def get_by_name(self):
        """Traversal chain sorted by Name."""
        result, cur = [], self.head_by_name
        while cur:
            result.append(cur)
            cur = cur.next_by_name
        return result


# --- 3b. Sparse Matrix (Multi-Linked) ---

class MatrixMListNode:
    """
    Node untuk Sparse Matrix Multi-Linked.
    nextRow: link ke elemen berikutnya di row yang sama.
    nextCol: link ke elemen berikutnya di column yang sama.
    """
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value
        self.next_row = None  # Link dalam row
        self.next_col = None  # Link dalam column


class SparseMatrix:
    """
    Sparse Matrix menggunakan Multi-Linked List.
    Solusi untuk matriks besar dengan banyak elemen 0.
    Hanya menyimpan elemen non-zero.
    - Row traversal: O(k), k = elemen non-zero di row
    - Column traversal: O(m), m = elemen non-zero di col
    """

    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.list_of_rows = [None] * num_rows  # Head tiap row
        self.list_of_cols = [None] * num_cols  # Head tiap col

    def set_value(self, row, col, value):
        """Tambah atau update elemen non-zero."""
        if value == 0:
            return  # Tidak simpan elemen nol

        new_node = MatrixMListNode(row, col, value)

        # Insert ke row chain
        if self.list_of_rows[row] is None or col < self.list_of_rows[row].col:
            new_node.next_row = self.list_of_rows[row]
            self.list_of_rows[row] = new_node
        else:
            cur = self.list_of_rows[row]
            while cur.next_row and cur.next_row.col < col:
                cur = cur.next_row
            new_node.next_row = cur.next_row
            cur.next_row = new_node

        # Insert ke col chain
        if self.list_of_cols[col] is None or row < self.list_of_cols[col].row:
            new_node.next_col = self.list_of_cols[col]
            self.list_of_cols[col] = new_node
        else:
            cur = self.list_of_cols[col]
            while cur.next_col and cur.next_col.row < row:
                cur = cur.next_col
            new_node.next_col = cur.next_col
            cur.next_col = new_node

    def get_row(self, row):
        """Ambil semua elemen non-zero dari sebuah row."""
        result, cur = [], self.list_of_rows[row]
        while cur:
            result.append((cur.col, cur.value))
            cur = cur.next_row
        return result

    def get_col(self, col):
        """Ambil semua elemen non-zero dari sebuah column."""
        result, cur = [], self.list_of_cols[col]
        while cur:
            result.append((cur.row, cur.value))
            cur = cur.next_col
        return result

    def __iter__(self):
        return SparseMatrixIterator(self.list_of_rows, self.num_rows)


# ============================================================
# BAGIAN 4: COMPLEX ITERATOR (Sparse Matrix Iterator)
# ============================================================

class SparseMatrixIterator:
    """
    Stateful Iterator untuk Sparse Matrix.
    Track: current row index + current node dalam row.
    _find_next_element() untuk skip row kosong.
    """

    def __init__(self, row_array, num_rows):
        self._row_array = row_array
        self._num_rows = num_rows
        self._cur_row = 0
        self._cur_node = None
        self._find_next_element()  # Inisialisasi ke elemen pertama

    def _find_next_element(self):
        """Lompat ke row berikutnya yang memiliki elemen."""
        while self._cur_row < self._num_rows and self._row_array[self._cur_row] is None:
            self._cur_row += 1
        if self._cur_row < self._num_rows:
            self._cur_node = self._row_array[self._cur_row]
        else:
            self._cur_node = None

    def __iter__(self):
        return self

    def __next__(self):
        if self._cur_node is None:
            raise StopIteration
        value = self._cur_node.value
        self._cur_node = self._cur_node.next_row
        if self._cur_node is None:
            self._cur_row += 1
            self._find_next_element()
        return value


# ============================================================
# BAGIAN 5: TEXT EDITOR BUFFER ADT
# ============================================================

class _EditBufferNode:
    """
    Node untuk Text Editor Buffer.
    Setiap node = satu baris teks (list of characters).
    Bagian dari Doubly Linked List of Vectors.
    """
    def __init__(self, text=None):
        self.text = text if text is not None else ['\n']
        self.next = None
        self.prev = None


class EditBuffer:
    """
    Text Editor Buffer menggunakan Doubly Linked List of Vectors.
    - Setiap node = satu baris (list of char)
    - Cursor: (lineIndex, columnIndex)
    - Mendukung insert/overwrite mode
    - Operasi: addChar, deleteChar, breakLine, moveCursor
    """

    def __init__(self):
        self._first_line = _EditBufferNode(['\n'])
        self._last_line = self._first_line
        self._cur_line = self._first_line
        self._cur_line_ndx = 0   # Index baris saat ini
        self._cur_col_ndx = 0    # Index kolom saat ini
        self._num_lines = 1
        self._insert_mode = True

    # --- Status Methods ---

    def num_lines(self):
        return self._num_lines

    def num_chars(self):
        """Jumlah karakter di baris saat ini (termasuk \\n)."""
        return len(self._cur_line.text)

    def line_index(self):
        return self._cur_line_ndx

    def column_index(self):
        return self._cur_col_ndx

    def get_char(self):
        """Karakter di posisi cursor saat ini."""
        return self._cur_line.text[self._cur_col_ndx]

    # --- Cursor Movement ---

    def move_up(self, nlines=1):
        """Pindah cursor ke atas. Adjust col jika baris lebih pendek."""
        if nlines <= 0:
            return
        nlines = min(nlines, self._cur_line_ndx)
        for _ in range(nlines):
            self._cur_line = self._cur_line.prev
        self._cur_line_ndx -= nlines
        if self._cur_col_ndx >= self.num_chars():
            self.move_line_end()

    def move_down(self, nlines=1):
        """Pindah cursor ke bawah. Adjust col jika baris lebih pendek."""
        if nlines <= 0:
            return
        max_down = self._num_lines - 1 - self._cur_line_ndx
        nlines = min(nlines, max_down)
        for _ in range(nlines):
            self._cur_line = self._cur_line.next
        self._cur_line_ndx += nlines
        if self._cur_col_ndx >= self.num_chars():
            self.move_line_end()

    def move_left(self):
        """Pindah cursor ke kiri. Wrap ke akhir baris sebelumnya jika di awal baris."""
        if self._cur_col_ndx == 0:
            if self._cur_line_ndx > 0:
                self.move_up(1)
                self.move_line_end()
        else:
            self._cur_col_ndx -= 1

    def move_right(self):
        """Pindah cursor ke kanan. Wrap ke awal baris berikutnya jika di akhir baris."""
        if self._cur_col_ndx < self.num_chars() - 1:
            self._cur_col_ndx += 1
        elif self._cur_line is not self._last_line:
            self.move_down(1)
            self.move_line_home()

    def move_line_home(self):
        """Pindah cursor ke awal baris."""
        self._cur_col_ndx = 0

    def move_line_end(self):
        """Pindah cursor ke akhir baris (sebelum \\n)."""
        self._cur_col_ndx = self.num_chars() - 1

    def move_doc_home(self):
        """Pindah cursor ke awal dokumen."""
        self._cur_line = self._first_line
        self._cur_line_ndx = 0
        self._cur_col_ndx = 0

    def move_doc_end(self):
        """Pindah cursor ke akhir dokumen."""
        self._cur_line = self._last_line
        self._cur_line_ndx = self._num_lines - 1
        self.move_line_end()

    # --- Editing Operations ---

    def _insert_node(self, after_node, text):
        """Helper: Insert node baru setelah after_node."""
        new_node = _EditBufferNode(text)
        new_node.next = after_node.next
        new_node.prev = after_node
        if after_node.next:
            after_node.next.prev = new_node
        else:
            self._last_line = new_node
        after_node.next = new_node
        self._num_lines += 1

    def _remove_node(self, node):
        """Helper: Hapus node dari linked list."""
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        if node is self._last_line:
            self._last_line = node.prev
        self._num_lines -= 1

    def break_line(self):
        """
        Pecah baris di posisi cursor (Enter key).
        Teks setelah cursor pindah ke baris baru.
        """
        new_line_contents = self._cur_line.text[self._cur_col_ndx:]
        del self._cur_line.text[self._cur_col_ndx:]
        self._cur_line.text.append('\n')
        self._insert_node(self._cur_line, new_line_contents)
        self._cur_line = self._cur_line.next
        self._cur_line_ndx += 1
        self._cur_col_ndx = 0

    def add_char(self, char):
        """
        Tambah karakter di posisi cursor.
        - Jika \\n: panggil break_line()
        - Insert mode: sisipkan karakter
        - Overwrite mode: ganti karakter
        """
        if char == '\n':
            self.break_line()
            return
        if self._insert_mode or self._cur_col_ndx == self.num_chars() - 1:
            self._cur_line.text.insert(self._cur_col_ndx, char)
        else:
            self._cur_line.text[self._cur_col_ndx] = char
        self._cur_col_ndx += 1

    def delete_char(self):
        """
        Hapus karakter di posisi cursor (Delete key).
        Jika di \\n: merge baris ini dengan baris berikutnya.

        Ilustrasi merge:
        Sebelum: Line1=['a','b','c','\\n'], Line2=['x','y','z','\\n'] (cursor di \\n line1)
        Sesudah: Line1=['a','b','c','x','y','z','\\n'] (Line2 dihapus)
        """
        if self.get_char() != '\n':
            self._cur_line.text.pop(self._cur_col_ndx)
        else:
            if self._cur_line is self._last_line:
                return  # Tidak bisa hapus \\n di baris terakhir
            next_line = self._cur_line.next
            self._cur_line.text.pop()          # Hapus \\n
            self._cur_line.text.extend(next_line.text)  # Gabung dengan baris berikutnya
            self._remove_node(next_line)

    def get_content(self):
        """Kembalikan seluruh isi buffer sebagai string."""
        lines = []
        cur = self._first_line
        while cur:
            lines.append(''.join(cur.text))
            cur = cur.next
        return ''.join(lines)


# ============================================================
# DEMO & PENGUJIAN
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("1. DOUBLY LINKED LIST")
    print("=" * 60)
    dll = DoublyLinkedList()
    for val in [30, 10, 50, 20, 40]:
        dll.insert_sorted(val)
    print("Forward :", dll.forward_traversal())   # [10, 20, 30, 40, 50]
    print("Reverse :", dll.reverse_traversal())   # [50, 40, 30, 20, 10]

    print("\n" + "=" * 60)
    print("2. CIRCULAR LINKED LIST")
    print("=" * 60)
    cll = CircularLinkedList()
    for val in [10, 30, 20, 50, 40]:
        cll.insert(val)
    print("Traversal :", cll.traverse())          # [10, 20, 30, 40, 50]
    print("Search 30 :", cll.search(30))          # True
    print("Search 99 :", cll.search(99))          # False

    print("\n" + "=" * 60)
    print("3. MULTI-LINKED LIST (Student Records)")
    print("=" * 60)
    sml = StudentMultiList()
    sml.insert(3, "Charlie")
    sml.insert(1, "Alice")
    sml.insert(2, "Bob")
    print("By ID  :", sml.get_by_id())
    print("By Name:", sml.get_by_name())

    print("\n" + "=" * 60)
    print("4. SPARSE MATRIX (Multi-Linked)")
    print("=" * 60)
    sm = SparseMatrix(4, 4)
    sm.set_value(0, 1, 5)
    sm.set_value(0, 3, 8)
    sm.set_value(1, 2, 3)
    sm.set_value(3, 0, 7)
    print("Row 0:", sm.get_row(0))   # [(1, 5), (3, 8)]
    print("Col 1:", sm.get_col(1))   # [(0, 5)]
    print("Iterator:", list(sm))     # [5, 8, 3, 7]

    print("\n" + "=" * 60)
    print("5. TEXT EDITOR BUFFER")
    print("=" * 60)
    buf = EditBuffer()
    for ch in "Hello":
        buf.add_char(ch)
    buf.add_char('\n')
    for ch in "World":
        buf.add_char(ch)
    print("Isi buffer:")
    print(repr(buf.get_content()))   # 'Hello\nWorld\n'

    # Test deleteChar (merge lines)
    buf.move_up(1)
    buf.move_line_end()
    buf.delete_char()  # Hapus \n → merge "Hello" + "World"
    print("Setelah merge:")
    print(repr(buf.get_content()))   # 'HelloWorld\n'

    print("\nSemua implementasi berhasil dijalankan!")