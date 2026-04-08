"""
Maze Pathfinding Visualizer
Tugas Praktikum Struktur Data
Algoritma: BFS, DFS, A*
"""

import tkinter as tk
import heapq
from collections import deque

CELL_SIZE = 40
ROWS, COLS = 15, 15
WIDTH  = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

C_WALL     = "#0d2f4a"
C_PATH     = "#f0f4f8"
C_VISITED  = "#3dcf8e"
C_OPEN     = "#fde68a"
C_CURRENT  = "#1d6a44"
C_SOLUTION = "#3b82f6"
C_START    = "#1d6a44"
C_END      = "#f59e0b"
C_BG       = "#0f172a"
C_TEXT     = "#dcdcdc"
C_GRID     = "#1e3246"

MAZE = [
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,1,1,0,1,0,1,0,1,1,1,0,1,0,1],
    [1,0,0,0,1,0,0,0,1,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,0,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,1,0,0,0,1],
    [1,1,1,0,1,0,1,1,1,0,1,0,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,1,1,0,1,0,1,0,1,0,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,1,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
]

START = (0, 1)
END   = (14, 13)
DIRS  = [(-1,0),(1,0),(0,-1),(0,1)]


def reconstruct(parent, end):
    path, cur = [], end
    while cur is not None:
        path.append(cur)
        cur = parent.get(cur)
    path.reverse()
    return path

def bfs(maze, start, end):
    queue = deque([start])
    visited = {start: None}
    steps = []
    while queue:
        r, c = queue.popleft()
        steps.append(('current', r, c))
        if (r, c) == end:
            break
        for dr, dc in DIRS:
            nr, nc = r+dr, c+dc
            if 0<=nr<ROWS and 0<=nc<COLS and not maze[nr][nc] and (nr,nc) not in visited:
                visited[(nr,nc)] = (r,c)
                queue.append((nr,nc))
                steps.append(('open', nr, nc))
        steps.append(('visited', r, c))
    path = reconstruct(visited, end)
    for p in path: steps.append(('path', p[0], p[1]))
    return steps, path

def dfs(maze, start, end):
    stack = [start]
    visited = {start: None}
    steps = []
    while stack:
        r, c = stack.pop()
        steps.append(('current', r, c))
        if (r, c) == end:
            break
        for dr, dc in DIRS:
            nr, nc = r+dr, c+dc
            if 0<=nr<ROWS and 0<=nc<COLS and not maze[nr][nc] and (nr,nc) not in visited:
                visited[(nr,nc)] = (r,c)
                stack.append((nr,nc))
                steps.append(('open', nr, nc))
        steps.append(('visited', r, c))
    path = reconstruct(visited, end)
    for p in path: steps.append(('path', p[0], p[1]))
    return steps, path

def astar(maze, start, end):
    def h(r, c): return abs(r-end[0]) + abs(c-end[1])
    g_cost = {start: 0}
    parent = {start: None}
    heap = [(h(*start), 0, start)]
    closed = set()
    steps = []
    counter = 0
    while heap:
        f, g, (r, c) = heapq.heappop(heap)
        if (r,c) in closed: continue
        closed.add((r,c))
        steps.append(('current', r, c))
        if (r,c) == end: break
        for dr, dc in DIRS:
            nr, nc = r+dr, c+dc
            if 0<=nr<ROWS and 0<=nc<COLS and not maze[nr][nc] and (nr,nc) not in closed:
                ng = g+1
                if ng < g_cost.get((nr,nc), float('inf')):
                    g_cost[(nr,nc)] = ng
                    parent[(nr,nc)] = (r,c)
                    counter += 1
                    heapq.heappush(heap, (ng+h(nr,nc), counter, (nr,nc)))
                    steps.append(('open', nr, nc))
        steps.append(('visited', r, c))
    path = reconstruct(parent, end)
    for p in path: steps.append(('path', p[0], p[1]))
    return steps, path


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Pathfinding")
        self.root.configure(bg=C_BG)
        self.root.resizable(False, False)

        self.algos    = [("BFS", bfs), ("DFS", dfs), ("A*", astar)]
        self.algo_idx = 0
        self.speed    = 30

        # Inisialisasi semua variabel PERTAMA
        self.cell_state   = {}
        self.steps        = []
        self.step_idx     = 0
        self.path         = []
        self.running_anim = False
        self.done         = False
        self.explored     = 0

        # Canvas
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT,
                                bg=C_BG, highlightthickness=0)
        self.canvas.pack()

        # Panel info
        self.panel = tk.Frame(root, bg="#0a0f1e")
        self.panel.pack(fill=tk.X, padx=10, pady=6)

        row1 = tk.Frame(self.panel, bg="#0a0f1e")
        row1.pack(fill=tk.X)
        self.lbl_algo   = tk.Label(row1, text="", bg="#0a0f1e", fg="#a0c4ff", font=("Courier",11,"bold"))
        self.lbl_algo.pack(side=tk.LEFT, padx=(0,15))
        self.lbl_status = tk.Label(row1, text="", bg="#0a0f1e", fg=C_TEXT, font=("Courier",11))
        self.lbl_status.pack(side=tk.LEFT, padx=(0,15))
        self.lbl_stats  = tk.Label(row1, text="", bg="#0a0f1e", fg="#a8e6cf", font=("Courier",11))
        self.lbl_stats.pack(side=tk.LEFT)

        row2 = tk.Frame(self.panel, bg="#0a0f1e")
        row2.pack(fill=tk.X, pady=(2,0))
        tk.Label(row2, text="[SPACE] Mulai  [A] Ganti Algo  [R] Reset  [+/-] Speed  [Q] Keluar",
                 bg="#0a0f1e", fg="#555e6e", font=("Courier",10)).pack(side=tk.LEFT)

        row3 = tk.Frame(self.panel, bg="#0a0f1e")
        row3.pack(fill=tk.X, pady=(2,4))
        for color, label in [(C_VISITED,"dieksplorasi"),(C_OPEN,"open list"),
                              (C_CURRENT,"posisi kini"),(C_SOLUTION,"solusi")]:
            cv = tk.Canvas(row3, width=12, height=12, bg="#0a0f1e", highlightthickness=0)
            cv.pack(side=tk.LEFT, padx=(0,2))
            cv.create_rectangle(0,0,12,12, fill=color, outline="")
            tk.Label(row3, text=label, bg="#0a0f1e", fg=C_TEXT, font=("Courier",10)).pack(side=tk.LEFT, padx=(0,12))

        # Update label & gambar
        self.update_panel()
        self.draw_maze()

        # Keyboard
        self.root.bind("<space>", self.on_space)
        self.root.bind("<r>", self.on_reset)
        self.root.bind("<R>", self.on_reset)
        self.root.bind("<a>", self.on_algo)
        self.root.bind("<A>", self.on_algo)
        self.root.bind("<q>", lambda e: root.destroy())
        self.root.bind("<plus>",  lambda e: setattr(self,'speed',max(5,self.speed-10)))
        self.root.bind("<equal>", lambda e: setattr(self,'speed',max(5,self.speed-10)))
        self.root.bind("<minus>", lambda e: setattr(self,'speed',min(200,self.speed+10)))

    def update_panel(self):
        name   = self.algos[self.algo_idx][0]
        status = "Selesai!" if self.done else ("Berjalan..." if self.running_anim else "Siap")
        self.lbl_algo.config(text=f"Algoritma: {name}")
        self.lbl_status.config(text=f"Status: {status}")
        self.lbl_stats.config(text=f"Eksplorasi: {self.explored}  Panjang: {len(self.path)}")

    def get_state(self, r, c):
        return self.cell_state.get((r,c), set())

    def draw_cell(self, r, c):
        x, y = c*CELL_SIZE, r*CELL_SIZE
        state = self.get_state(r, c)
        if MAZE[r][c]:            color = C_WALL
        elif (r,c) == END:        color = C_END
        elif (r,c) == START:      color = C_START
        elif 'path'    in state:  color = C_SOLUTION
        elif 'current' in state:  color = C_CURRENT
        elif 'visited' in state:  color = C_VISITED
        elif 'open'    in state:  color = C_OPEN
        else:                     color = C_PATH

        self.canvas.create_rectangle(x+1, y+1, x+CELL_SIZE-1, y+CELL_SIZE-1,
                                     fill=color, outline=C_GRID)
        cx, cy = x+CELL_SIZE//2, y+CELL_SIZE//2
        if (r,c) == START:
            self.canvas.create_text(cx, cy, text="S", fill="white", font=("Courier",13,"bold"))
        elif (r,c) == END:
            self.canvas.create_text(cx, cy, text="E", fill="white", font=("Courier",13,"bold"))
        elif 'visited' in state:
            self.canvas.create_text(cx, cy, text="x", fill="#0a1a28", font=("Courier",10))
        elif 'open' in state:
            self.canvas.create_text(cx, cy, text="o", fill="#786010", font=("Courier",10))

    def draw_maze(self):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLS):
                self.draw_cell(r, c)

    def advance(self):
        if self.step_idx >= len(self.steps):
            self.running_anim = False
            self.done = True
            self.update_panel()
            return

        kind, r, c = self.steps[self.step_idx]
        self.step_idx += 1

        s = self.cell_state.setdefault((r,c), set())
        if kind == 'current':
            for v in self.cell_state.values(): v.discard('current')
            s.add('current')
        elif kind == 'open':
            if 'visited' not in s: s.add('open')
        elif kind == 'visited':
            s.add('visited'); s.discard('open'); s.discard('current')
            self.explored += 1
        elif kind == 'path':
            s.clear(); s.add('path')

        self.draw_cell(r, c)
        self.update_panel()
        if self.running_anim:
            self.root.after(self.speed, self.advance)

    def on_space(self, event):
        if not self.running_anim and not self.done:
            _, fn = self.algos[self.algo_idx]
            self.steps, self.path = fn(MAZE, START, END)
            self.running_anim = True
            self.advance()

    def on_reset(self, event=None):
        self.running_anim = False
        self.cell_state   = {}
        self.steps        = []
        self.step_idx     = 0
        self.path         = []
        self.done         = False
        self.explored     = 0
        self.draw_maze()
        self.update_panel()

    def on_algo(self, event):
        if not self.running_anim:
            self.algo_idx = (self.algo_idx + 1) % len(self.algos)
            self.on_reset()


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()