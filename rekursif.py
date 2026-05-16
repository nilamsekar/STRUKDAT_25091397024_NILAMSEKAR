# =========================
# PROGRAM REKURSIF GABUNGAN
# =========================

# ---------- 1. N-QUEENS ----------
def is_safe(board, row, col, n):
    for i in range(col):
        if board[row][i] == 1:
            return False

    i, j = row, col
    while i >= 0 and j >= 0:
        if board[i][j] == 1:
            return False
        i -= 1
        j -= 1

    i, j = row, col
    while i < n and j >= 0:
        if board[i][j] == 1:
            return False
        i += 1
        j -= 1

    return True


def solve_n_queens(board, col, n):
    if col >= n:
        return True

    for i in range(n):
        if is_safe(board, i, col, n):
            board[i][col] = 1

            if solve_n_queens(board, col + 1, n):
                return True

            board[i][col] = 0

    return False


def n_queens():
    n = int(input("Masukkan ukuran papan (n): "))
    board = [[0] * n for _ in range(n)]

    if solve_n_queens(board, 0, n):
        print("Solusi N-Queens:")
        for row in board:
            print(row)
    else:
        print("Tidak ada solusi")


# ---------- 2. KNIGHT TOUR ----------
def is_valid(x, y, board, n):
    return 0 <= x < n and 0 <= y < n and board[x][y] == -1


def knight_tour_util(x, y, move_i, board, moves, n):
    if move_i == n * n:
        return True

    for dx, dy in moves:
        next_x, next_y = x + dx, y + dy

        if is_valid(next_x, next_y, board, n):
            board[next_x][next_y] = move_i
            if knight_tour_util(next_x, next_y, move_i + 1, board, moves, n):
                return True
            board[next_x][next_y] = -1

    return False


def knight_tour():
    n = int(input("Masukkan ukuran papan: "))
    start_x = int(input("Posisi awal X: "))
    start_y = int(input("Posisi awal Y: "))

    board = [[-1 for _ in range(n)] for _ in range(n)]

    moves = [
        (2, 1), (1, 2), (-1, 2), (-2, 1),
        (-2, -1), (-1, -2), (1, -2), (2, -1)
    ]

    board[start_x][start_y] = 0

    if knight_tour_util(start_x, start_y, 1, board, moves, n):
        print("Solusi Knight's Tour:")
        for row in board:
            print(row)
    else:
        print("Tidak ada solusi")


# ---------- 3. KNAPSACK ----------
def knapsack_recursive(weights, target, index=0, current=[]):
    if target == 0:
        return current

    if index >= len(weights) or target < 0:
        return None

    # Ambil item
    result = knapsack_recursive(
        weights,
        target - weights[index],
        index + 1,
        current + [weights[index]]
    )

    if result:
        return result

    # Tidak ambil item
    return knapsack_recursive(weights, target, index + 1, current)


def knapsack():
    weights = list(map(int, input("Masukkan berat barang (pisahkan spasi): ").split()))
    target = int(input("Masukkan berat target: "))

    result = knapsack_recursive(weights, target)

    if result:
        print("Solusi ditemukan:", result)
    else:
        print("Tidak ada kombinasi yang cocok")


# ---------- MENU ----------
def main():
    while True:
        print("\n=== MENU PROGRAM REKURSIF ===")
        print("1. N-Queens")
        print("2. Knight's Tour")
        print("3. Knapsack")
        print("4. Keluar")

        pilihan = input("Pilih menu (1-4): ")

        if pilihan == '1':
            n_queens()
        elif pilihan == '2':
            knight_tour()
        elif pilihan == '3':
            knapsack()
        elif pilihan == '4':
            print("Program selesai.")
            break
        else:
            print("Pilihan tidak valid!")


# Jalankan program
if __name__ == "__main__":
    main()