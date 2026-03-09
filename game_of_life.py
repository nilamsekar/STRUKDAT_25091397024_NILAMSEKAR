"""
GAME OF LIFE - Conway's Cellular Automaton
Implementasi menggunakan ADT Array

ATURAN CONWAY:
1. Sel hidup dengan 2-3 tetangga hidup → tetap hidup
2. Sel hidup dengan 0-1 tetangga hidup → mati (isolasi)
3. Sel hidup dengan 4+ tetangga hidup → mati (overpopulasi)
4. Sel mati dengan tepat 3 tetangga hidup → hidup (kelahiran)

Tetangga = 8 sel di sekitar (vertikal, horizontal, diagonal)
"""

import time
import os
import random
from array_adt import Array


class GameOfLife:
    """
    Conway's Game of Life menggunakan ADT Array.
    Grid direpresentasikan sebagai Array 2D (Array of Arrays).
    """
    
    # Konstanta status sel
    DEAD = 0
    ALIVE = 1
    
    def __init__(self, rows, cols):
        """
        Inisialisasi grid Game of Life.
        
        Args:
            rows (int): Jumlah baris
            cols (int): Jumlah kolom
        """
        self._rows = rows
        self._cols = cols
        
        # Buat grid 2D menggunakan Array of Arrays
        self._grid = Array(rows)
        for i in range(rows):
            self._grid[i] = Array(cols)
            self._grid[i].clearing(self.DEAD)
    
    def num_rows(self):
        """Mengembalikan jumlah baris"""
        return self._rows
    
    def num_cols(self):
        """Mengembalikan jumlah kolom"""
        return self._cols
    
    def configure(self, coord_list):
        """
        Mengatur konfigurasi awal dengan daftar koordinat sel hidup.
        
        Args:
            coord_list: List of tuples (row, col) untuk sel yang hidup
        """
        # Reset semua sel ke mati
        for row in range(self._rows):
            self._grid[row].clearing(self.DEAD)
        
        # Set sel yang hidup
        for row, col in coord_list:
            assert 0 <= row < self._rows and 0 <= col < self._cols, \
                f"Koordinat ({row}, {col}) di luar grid"
            self._grid[row][col] = self.ALIVE
    
    def randomize(self, density=0.3):
        """
        Mengisi grid secara acak.
        
        Args:
            density (float): Probabilitas sel hidup (0.0 - 1.0)
        """
        for row in range(self._rows):
            for col in range(self._cols):
                if random.random() < density:
                    self._grid[row][col] = self.ALIVE
                else:
                    self._grid[row][col] = self.DEAD
    
    def is_live_cell(self, row, col):
        """
        Mengecek apakah sel hidup.
        
        Args:
            row (int): Baris sel
            col (int): Kolom sel
            
        Returns:
            bool: True jika sel hidup
        """
        return self._grid[row][col] == self.ALIVE
    
    def num_live_neighbors(self, row, col):
        """
        Menghitung jumlah tetangga hidup di sekitar sel.
        
        Tetangga = 8 sel di sekitar (vertikal, horizontal, diagonal):
          [NW] [N] [NE]
          [W]  [X]  [E]
          [SW] [S] [SE]
        
        Args:
            row (int): Baris sel
            col (int): Kolom sel
            
        Returns:
            int: Jumlah tetangga hidup (0-8)
        """
        count = 0
        
        # Periksa 8 sel tetangga
        for i in range(-1, 2):
            for j in range(-1, 2):
                # Skip sel itu sendiri
                if i == 0 and j == 0:
                    continue
                
                # Hitung koordinat tetangga dengan wrapping (toroidal grid)
                neighbor_row = (row + i) % self._rows
                neighbor_col = (col + j) % self._cols
                
                # Tambahkan ke count jika tetangga hidup
                if self._grid[neighbor_row][neighbor_col] == self.ALIVE:
                    count += 1
        
        return count
    
    def evolve(self):
        """
        Menghasilkan generasi berikutnya berdasarkan aturan Conway.
        
        ATURAN:
        1. Sel hidup + 2-3 tetangga hidup → tetap hidup
        2. Sel hidup + 0-1 tetangga hidup → mati (isolasi)
        3. Sel hidup + 4+ tetangga hidup → mati (overpopulasi)
        4. Sel mati + tepat 3 tetangga hidup → hidup (kelahiran)
        """
        # Buat grid baru untuk generasi berikutnya
        new_grid = Array(self._rows)
        for i in range(self._rows):
            new_grid[i] = Array(self._cols)
            new_grid[i].clearing(self.DEAD)
        
        # Terapkan aturan Conway pada setiap sel
        for row in range(self._rows):
            for col in range(self._cols):
                neighbors = self.num_live_neighbors(row, col)
                current_state = self._grid[row][col]
                
                if current_state == self.ALIVE:
                    # Sel hidup
                    if neighbors == 2 or neighbors == 3:
                        # Aturan 1: tetap hidup
                        new_grid[row][col] = self.ALIVE
                    # Aturan 2 & 3: mati (default sudah DEAD)
                else:
                    # Sel mati
                    if neighbors == 3:
                        # Aturan 4: kelahiran
                        new_grid[row][col] = self.ALIVE
        
        # Update grid
        self._grid = new_grid
    
    def display(self):
        """
        Menampilkan grid ke terminal.
        
        Returns:
            str: Representasi visual grid
        """
        result = ""
        for row in range(self._rows):
            line = ""
            for col in range(self._cols):
                if self.is_live_cell(row, col):
                    line += "██"  # Sel hidup
                else:
                    line += "  "  # Sel mati
            result += line + "\n"
        return result


class GameOfLifeSimulator:
    """Simulator dengan menu interaktif untuk Game of Life"""
    
    def __init__(self):
        self.game = None
        self.rows = 30
        self.cols = 60
    
    def clear_screen(self):
        """Membersihkan layar terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_main_menu(self):
        """Menampilkan menu utama"""
        self.clear_screen()
        print("╔" + "═" * 58 + "╗")
        print("║" + " " * 58 + "║")
        print("║" + "  CONWAY'S GAME OF LIFE - ADT Array  ".center(58) + "║")
        print("║" + " " * 58 + "║")
        print("╚" + "═" * 58 + "╝")
        print("\n1. Konfigurasi Acak")
        print("2. Pola Klasik")
        print("3. Atur Ukuran Grid (saat ini: {}x{})".format(self.rows, self.cols))
        print("4. Informasi Aturan Conway")
        print("5. Keluar")
        print("\n" + "─" * 60)
    
    def show_pattern_menu(self):
        """Menampilkan menu pola klasik"""
        print("\n" + "─" * 60)
        print("  POLA KLASIK")
        print("─" * 60)
        print("\n1. Glider       - Pola bergerak diagonal")
        print("2. Blinker      - Oscillator periode 2")
        print("3. Toad         - Oscillator periode 2")
        print("4. Beacon       - Oscillator periode 2")
        print("5. Block        - Still life (stabil)")
        print("6. Beehive      - Still life (stabil)")
        print("7. Kembali")
        print("\n" + "─" * 60)
    
    def load_pattern(self, pattern_name):
        """
        Memuat pola klasik ke grid.
        
        Args:
            pattern_name (str): Nama pola
        """
        center_row = self.rows // 2
        center_col = self.cols // 2
        
        patterns = {
            'glider': [
                (center_row - 1, center_col),
                (center_row, center_col + 1),
                (center_row + 1, center_col - 1),
                (center_row + 1, center_col),
                (center_row + 1, center_col + 1)
            ],
            'blinker': [
                (center_row, center_col - 1),
                (center_row, center_col),
                (center_row, center_col + 1)
            ],
            'toad': [
                (center_row, center_col),
                (center_row, center_col + 1),
                (center_row, center_col + 2),
                (center_row + 1, center_col - 1),
                (center_row + 1, center_col),
                (center_row + 1, center_col + 1)
            ],
            'beacon': [
                (center_row, center_col),
                (center_row, center_col + 1),
                (center_row + 1, center_col),
                (center_row + 2, center_col + 3),
                (center_row + 3, center_col + 2),
                (center_row + 3, center_col + 3)
            ],
            'block': [
                (center_row, center_col),
                (center_row, center_col + 1),
                (center_row + 1, center_col),
                (center_row + 1, center_col + 1)
            ],
            'beehive': [
                (center_row, center_col + 1),
                (center_row, center_col + 2),
                (center_row + 1, center_col),
                (center_row + 1, center_col + 3),
                (center_row + 2, center_col + 1),
                (center_row + 2, center_col + 2)
            ]
        }
        
        if pattern_name in patterns:
            self.game.configure(patterns[pattern_name])
        else:
            print(f"Pola '{pattern_name}' tidak ditemukan!")
    
    def show_info(self):
        """Menampilkan informasi aturan Conway"""
        self.clear_screen()
        print("╔" + "═" * 58 + "╗")
        print("║" + " " * 58 + "║")
        print("║" + "  ATURAN CONWAY'S GAME OF LIFE  ".center(58) + "║")
        print("║" + " " * 58 + "║")
        print("╚" + "═" * 58 + "╝")
        
        print("\nTetangga = 8 sel di sekitar (vertikal, horizontal, diagonal)")
        print("\n[ATURAN 1] Sel hidup dengan 2-3 tetangga hidup")
        print("           → Tetap hidup di generasi berikutnya")
        
        print("\n[ATURAN 2] Sel hidup dengan 0-1 tetangga hidup")
        print("           → Mati karena isolasi")
        
        print("\n[ATURAN 3] Sel hidup dengan 4+ tetangga hidup")
        print("           → Mati karena overpopulasi")
        
        print("\n[ATURAN 4] Sel mati dengan tepat 3 tetangga hidup")
        print("           → Hidup (kelahiran)")
        
        print("\n" + "─" * 60)
        print("Implementasi menggunakan ADT Array:")
        print("  • Grid 2D = Array of Arrays")
        print("  • Ukuran tetap setelah dibuat")
        print("  • Operasi: length, getitem, setitem, clearing, iterator")
        print("─" * 60)
        
        input("\nTekan Enter untuk kembali...")
    
    def run_simulation(self, generations, delay=0.2):
        """
        Menjalankan simulasi.
        
        Args:
            generations (int): Jumlah generasi
            delay (float): Delay antar generasi (detik)
        """
        for gen in range(generations):
            self.clear_screen()
            print("═" * 60)
            print(f"  Generasi: {gen + 1}/{generations}")
            print(f"  Grid: {self.game.num_rows()} x {self.game.num_cols()}")
            print(f"  Tekan Ctrl+C untuk berhenti")
            print("═" * 60)
            print()
            print(self.game.display())
            
            # Evolusi ke generasi berikutnya
            self.game.evolve()
            time.sleep(delay)
    
    def run(self):
        """Menjalankan aplikasi simulator"""
        while True:
            self.show_main_menu()
            choice = input("Pilih menu (1-5): ").strip()
            
            if choice == "1":
                # Konfigurasi Acak
                self.game = GameOfLife(self.rows, self.cols)
                
                density = input("\nKepadatan sel hidup (0.1-0.9, default 0.3): ").strip()
                try:
                    density = float(density) if density else 0.3
                    density = max(0.1, min(0.9, density))
                except:
                    density = 0.3
                
                self.game.randomize(density)
                
                generations = input("Jumlah generasi (default 100): ").strip()
                try:
                    generations = int(generations) if generations else 100
                except:
                    generations = 100
                
                delay = input("Delay antar generasi dalam detik (default 0.2): ").strip()
                try:
                    delay = float(delay) if delay else 0.2
                except:
                    delay = 0.2
                
                try:
                    self.run_simulation(generations, delay)
                except KeyboardInterrupt:
                    print("\n\nSimulasi dihentikan!")
                    input("Tekan Enter untuk kembali ke menu...")
            
            elif choice == "2":
                # Pola Klasik
                self.game = GameOfLife(self.rows, self.cols)
                
                while True:
                    self.clear_screen()
                    self.show_pattern_menu()
                    pattern_choice = input("Pilih pola (1-7): ").strip()
                    
                    patterns = {
                        "1": "glider",
                        "2": "blinker",
                        "3": "toad",
                        "4": "beacon",
                        "5": "block",
                        "6": "beehive"
                    }
                    
                    if pattern_choice in patterns:
                        self.load_pattern(patterns[pattern_choice])
                        
                        generations = input("\nJumlah generasi (default 50): ").strip()
                        try:
                            generations = int(generations) if generations else 50
                        except:
                            generations = 50
                        
                        try:
                            self.run_simulation(generations, 0.3)
                        except KeyboardInterrupt:
                            print("\n\nSimulasi dihentikan!")
                            input("Tekan Enter untuk kembali ke menu...")
                        break
                    
                    elif pattern_choice == "7":
                        break
                    else:
                        print("Pilihan tidak valid!")
                        input("Tekan Enter untuk melanjutkan...")
            
            elif choice == "3":
                # Atur Ukuran Grid
                rows = input("\nJumlah baris (default 30): ").strip()
                cols = input("Jumlah kolom (default 60): ").strip()
                
                try:
                    self.rows = int(rows) if rows else 30
                    self.cols = int(cols) if cols else 60
                    print(f"\nUkuran grid diatur ke {self.rows} x {self.cols}")
                except:
                    print("Input tidak valid! Ukuran tidak diubah.")
                
                input("Tekan Enter untuk kembali ke menu...")
            
            elif choice == "4":
                # Informasi
                self.show_info()
            
            elif choice == "5":
                # Keluar
                self.clear_screen()
                print("\nTerima kasih telah menggunakan Game of Life!")
                print("─" * 60)
                break
            
            else:
                print("\nPilihan tidak valid! Silakan pilih 1-5.")
                input("Tekan Enter untuk melanjutkan...")


def main():
    """Entry point aplikasi"""
    try:
        simulator = GameOfLifeSimulator()
        simulator.run()
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan. Sampai jumpa!")
    except Exception as e:
        print(f"\nTerjadi error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()