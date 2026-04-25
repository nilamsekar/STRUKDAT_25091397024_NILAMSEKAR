"""
Queue Visualizer — Python
Implementasi 5 Kasus Struktur Data Queue
=========================================
Kasus 1: Antrian Printer (FIFO)
Kasus 2: Permainan Hot Potato (Circular Queue)
Kasus 3: Antrian Rumah Sakit (Priority Queue)
Kasus 4: BFS Graph Traversal
Kasus 5: Simulasi Loket Bandara (Discrete-Event Simulation)
"""

from collections import deque
import heapq
import random
import time


# ═══════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════

def header(title: str, subtitle: str = ""):
    print("\n" + "═" * 60)
    print(f"  {title}")
    if subtitle:
        print(f"  {subtitle}")
    print("═" * 60)

def log(msg: str, kind: str = "info"):
    icons = {"ok": "✅", "out": "🔴", "info": "ℹ️ ", "warn": "⚠️ "}
    print(f"  {icons.get(kind,'ℹ️ ')} {msg}")

def separator():
    print("  " + "─" * 56)


# ═══════════════════════════════════════════════════════════════
#  KASUS 1 — ANTRIAN PRINTER (FIFO)
# ═══════════════════════════════════════════════════════════════

DOCS = [
    {"name": "laporan.pdf",     "ext": "pdf"},
    {"name": "tugas.docx",      "ext": "docx"},
    {"name": "foto.jpg",        "ext": "jpg"},
    {"name": "data.xlsx",       "ext": "xlsx"},
    {"name": "slide.pptx",      "ext": "pptx"},
    {"name": "resume.pdf",      "ext": "pdf"},
    {"name": "laporan2.docx",   "ext": "docx"},
]


class PrinterQueue:
    """Antrian printer FIFO — dokumen dicetak sesuai urutan kedatangan."""

    MAX_SIZE = 6

    def __init__(self):
        self.queue: deque = deque()
        self.doc_index = 0

    def enqueue(self) -> None:
        if len(self.queue) >= self.MAX_SIZE:
            log("Queue penuh (max 6)!", "out")
            return
        doc = DOCS[self.doc_index % len(DOCS)]
        self.doc_index += 1
        self.queue.append(doc.copy())
        log(f'enqueue("{doc["name"]}") → tambah ke belakang', "ok")

    def dequeue(self) -> None:
        if not self.queue:
            log("Queue kosong — tidak ada dokumen!", "out")
            return
        doc = self.queue.popleft()
        log(f'dequeue() → 🖨  Mencetak: {doc["name"]}', "out")

    def display(self) -> None:
        if not self.queue:
            print("    [antrian kosong]")
            return
        items = list(self.queue)
        parts = []
        for i, doc in enumerate(items):
            tag = ""
            if i == 0 and i == len(items) - 1:
                tag = "(front=rear)"
            elif i == 0:
                tag = "(front)"
            elif i == i == len(items) - 1:
                tag = "(rear)"
            parts.append(f'[{doc["ext"].upper()}:{doc["name"]}{" "+tag if tag else ""}]')
        print("    front → " + " → ".join(parts) + " ← rear")

    def run_demo(self, steps: int = 8) -> None:
        header("KASUS 1 — Antrian Printer Bersama",
               "Dokumen dicetak sesuai urutan kedatangan — FIFO murni")
        for step in range(1, steps + 1):
            separator()
            print(f"  Langkah {step}:")
            # Randomly enqueue or dequeue
            if len(self.queue) < 3 or (len(self.queue) < 5 and random.random() > 0.4):
                self.enqueue()
            if self.queue and random.random() > 0.3:
                self.dequeue()
            self.display()
        separator()
        log(f"Sisa dokumen di queue: {len(self.queue)}", "info")


# ═══════════════════════════════════════════════════════════════
#  KASUS 2 — HOT POTATO (CIRCULAR QUEUE)
# ═══════════════════════════════════════════════════════════════

class HotPotato:
    """
    Permainan Hot Potato menggunakan circular queue.
    Pemain yang memegang kentang saat hitungan habis, gugur.
    """

    NAMES = ["Ayu", "Budi", "Citra", "Dian", "Eka", "Fajar"]

    def __init__(self, passes_per_round: int = 4):
        self.passes_per_round = passes_per_round
        self.queue: deque = deque(self.NAMES)
        self.eliminated: list = []
        self.round = 0
        self.total_passes = 0

    def display(self) -> None:
        alive = list(self.queue)
        elim  = self.eliminated
        print(f"    Pemain aktif  : {' → '.join(alive)}")
        if elim:
            print(f"    Gugur         : {', '.join(elim)}")

    def step(self) -> str | None:
        """Jalankan satu ronde. Kembalikan nama yang gugur, atau None jika selesai."""
        if len(self.queue) <= 1:
            return None
        # Oper kentang sebanyak passes_per_round kali
        for _ in range(self.passes_per_round):
            self.queue.append(self.queue.popleft())
            self.total_passes += 1
        # Pemain di depan memegang kentang → gugur
        holder = self.queue.popleft()
        self.eliminated.append(holder)
        self.round += 1
        return holder

    def run_demo(self) -> None:
        header("KASUS 2 — Permainan Hot Potato 🥔",
               "Circular queue — pemain yang memegang kentang saat hitungan habis, gugur")
        print(f"  Oper per ronde : {self.passes_per_round}")
        separator()
        self.display()

        while len(self.queue) > 1:
            separator()
            elim = self.step()
            log(f"Ronde {self.round}: 🥔 {elim} memegang kentang → GUGUR!", "out")
            log(f"Total oper: {self.total_passes} | Tersisa: {len(self.queue)} pemain", "info")
            self.display()

        separator()
        winner = self.queue[0]
        log(f"🏆 Pemenang: {winner}!", "ok")


# ═══════════════════════════════════════════════════════════════
#  KASUS 3 — ANTRIAN RUMAH SAKIT (PRIORITY QUEUE)
# ═══════════════════════════════════════════════════════════════

PRIORITY_LABELS = {
    0: ("KRITIS",   "🔴"),
    1: ("DARURAT",  "🟠"),
    2: ("MENENGAH", "🟡"),
    3: ("RINGAN",   "🟢"),
}

PATIENT_POOL = [
    ("Ani",   0), ("Budi",  1), ("Citra", 2), ("Dedi",  3),
    ("Eko",   0), ("Fira",  1), ("Gita",  2), ("Hadi",  3),
    ("Indah", 1), ("Joko",  0), ("Kiki",  2), ("Luki",  3),
]


class HospitalQueue:
    """
    Priority queue rumah sakit.
    Pasien darurat didahulukan; prioritas sama → FIFO.
    """

    def __init__(self):
        # heap: (priority, arrival_order, name)
        self._heap: list = []
        self._counter = 0        # tie-breaker untuk FIFO
        self.served: list = []

    def enqueue(self, name: str, priority: int) -> None:
        heapq.heappush(self._heap, (priority, self._counter, name))
        self._counter += 1
        label, icon = PRIORITY_LABELS[priority]
        log(f'enqueue("{name}") → prioritas {icon} {label} (P{priority})', "ok")

    def dequeue(self) -> None:
        if not self._heap:
            log("Queue kosong — tidak ada pasien!", "out")
            return
        priority, _, name = heapq.heappop(self._heap)
        label, icon = PRIORITY_LABELS[priority]
        log(f'dequeue() → 🏥 Melayani: {name} [{icon} {label}]', "out")
        self.served.append((name, priority))

    def display(self) -> None:
        if not self._heap:
            print("    [antrian kosong]")
            return
        # Group by priority
        groups: dict[int, list] = {0: [], 1: [], 2: [], 3: []}
        for prio, _, name in sorted(self._heap):
            groups[prio].append(name)
        for prio in range(4):
            label, icon = PRIORITY_LABELS[prio]
            patients = groups[prio]
            status = " → ".join(patients) if patients else "—"
            print(f"    {icon} P{prio} {label:9s}: {status}")

    def run_demo(self) -> None:
        header("KASUS 3 — Antrian Rumah Sakit",
               "Priority Queue — pasien darurat didahulukan; sama prioritas → FIFO")

        # Fill with random patients
        log("Mengisi antrian dengan pasien acak...", "info")
        separator()
        sample = random.sample(PATIENT_POOL, 8)
        for name, prio in sample:
            self.enqueue(name, prio)

        separator()
        print("  Status antrian awal:")
        self.display()

        separator()
        log("Mulai melayani pasien...", "info")
        separator()
        while self._heap:
            self.dequeue()

        separator()
        log(f"Semua {len(self.served)} pasien telah dilayani.", "ok")
        print("  Urutan pelayanan:")
        for i, (name, prio) in enumerate(self.served, 1):
            label, icon = PRIORITY_LABELS[prio]
            print(f"    {i:2d}. {icon} {name} [{label}]")


# ═══════════════════════════════════════════════════════════════
#  KASUS 4 — BFS GRAPH TRAVERSAL
# ═══════════════════════════════════════════════════════════════

BFS_GRAPH: dict[str, list[str]] = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "F"],
    "F": ["C", "E", "G"],
    "G": ["F"],
}


class BFSTraversal:
    """BFS menggunakan queue untuk menelusuri graf."""

    def __init__(self, graph: dict[str, list[str]], start: str = "A"):
        self.graph = graph
        self.start = start

    def run(self) -> list[str]:
        """Jalankan BFS dan kembalikan urutan kunjungan."""
        visited: set[str] = set()
        queue: deque[str] = deque([self.start])
        order: list[str] = []
        log(f"BFS dimulai dari '{self.start}' → enqueue('{self.start}')", "ok")

        while queue:
            node = queue.popleft()
            if node in visited:
                continue
            visited.add(node)
            order.append(node)
            log(f"dequeue() → proses [{node}] | urutan: {' → '.join(order)}", "out")

            new_neighbors = [
                nb for nb in self.graph[node]
                if nb not in visited and nb not in queue
            ]
            for nb in new_neighbors:
                queue.append(nb)
            if new_neighbors:
                log(f"enqueue tetangga: [{', '.join(new_neighbors)}] | queue: {list(queue)}", "ok")

        return order

    def run_demo(self) -> None:
        header("KASUS 4 — BFS Graph Traversal",
               "Breadth-First Search menggunakan queue untuk menjelajahi graf")
        print("  Graf adjacency list:")
        for node, neighbors in self.graph.items():
            print(f"    {node} → {', '.join(neighbors)}")
        separator()
        order = self.run()
        separator()
        log(f"✅ BFS selesai. Urutan kunjungan: {' → '.join(order)}", "ok")


# ═══════════════════════════════════════════════════════════════
#  KASUS 5 — SIMULASI LOKET BANDARA
# ═══════════════════════════════════════════════════════════════

class Passenger:
    def __init__(self, pid: int, arrival_time: int):
        self.id = pid
        self.arrival_time = arrival_time
        self.name = f"P{pid}"


class Agent:
    def __init__(self, agent_id: int):
        self.id = agent_id
        self.busy = False
        self.end_time = 0
        self.serving: Passenger | None = None
        self.start_time = 0


class AirportSimulation:
    """
    Discrete-event simulation loket tiket bandara.
    Pengaruh jumlah agen terhadap rata-rata waktu tunggu.
    """

    SERVICE_TIME = 5    # menit per penumpang
    SIM_DURATION = 120  # total durasi simulasi (menit)

    def __init__(self, num_agents: int = 2, arrival_interval: int = 4):
        self.num_agents = num_agents
        self.arrival_interval = arrival_interval
        self.queue: deque[Passenger] = deque()
        self.agents = [Agent(i + 1) for i in range(num_agents)]
        self.time = 0
        self.pax_id = 0
        self.total_wait = 0
        self.num_served = 0
        self.max_queue = 0
        self.log_entries: list[str] = []

    def _log(self, msg: str) -> None:
        self.log_entries.append(f"t={self.time:3d}: {msg}")

    def tick(self) -> None:
        self.time += 1

        # Kedatangan penumpang (probabilistik)
        if random.random() < 1 / self.arrival_interval:
            self.pax_id += 1
            pax = Passenger(self.pax_id, self.time)
            self.queue.append(pax)
            if len(self.queue) > self.max_queue:
                self.max_queue = len(self.queue)
            self._log(f"Penumpang {pax.name} tiba → antrian[{len(self.queue)}]")

        # Tugaskan penumpang ke agen kosong
        for agent in self.agents:
            if not agent.busy and self.queue:
                pax = self.queue.popleft()
                wait = self.time - pax.arrival_time
                self.total_wait += wait
                self.num_served += 1
                agent.busy = True
                agent.serving = pax
                agent.end_time = self.time + self.SERVICE_TIME
                agent.start_time = self.time
                self._log(f"Loket {agent.id} melayani {pax.name} (tunggu {wait} mnt)")

        # Selesaikan pelayanan
        for agent in self.agents:
            if agent.busy and self.time >= agent.end_time:
                self._log(f"Loket {agent.id} selesai melayani {agent.serving.name}")
                agent.busy = False
                agent.serving = None

    def run(self) -> dict:
        """Jalankan simulasi penuh dan kembalikan statistik."""
        random.seed(42)
        for _ in range(self.SIM_DURATION):
            self.tick()

        avg_wait = round(self.total_wait / self.num_served, 2) if self.num_served else 0
        return {
            "total_served":  self.num_served,
            "avg_wait":      avg_wait,
            "max_queue":     self.max_queue,
            "remaining":     len(self.queue),
            "log":           self.log_entries,
        }

    def run_demo(self) -> None:
        header("KASUS 5 — Simulasi Loket Tiket Bandara",
               "Discrete-event simulation — pengaruh jumlah agen terhadap rata-rata tunggu")

        configs = [(1, 4), (2, 4), (3, 4)]
        results = {}

        for agents, interval in configs:
            sim = AirportSimulation(num_agents=agents, arrival_interval=interval)
            stats = sim.run()
            results[agents] = stats

            separator()
            print(f"  Konfigurasi: {agents} agen | interval tiba ~{interval} menit")
            # Print last 10 log entries as sample
            print(f"  Sample log (10 entri terakhir dari {len(stats['log'])}):")
            for entry in stats["log"][-10:]:
                print(f"    {entry}")

        separator()
        print("\n  RINGKASAN PERBANDINGAN")
        print(f"  {'Agen':>6} | {'Dilayani':>10} | {'Rata-rata Tunggu':>18} | {'Maks Antrian':>13}")
        print("  " + "-" * 56)
        for agents, stats in results.items():
            print(
                f"  {agents:>6} | {stats['total_served']:>10} | "
                f"{stats['avg_wait']:>16.2f}m | {stats['max_queue']:>13}"
            )
        separator()
        log("Simulasi selesai (120 menit per konfigurasi).", "ok")


# ═══════════════════════════════════════════════════════════════
#  MAIN — Jalankan semua kasus
# ═══════════════════════════════════════════════════════════════

def main():
    random.seed(99)

    print("\n" + "╔" + "═" * 58 + "╗")
    print("║  QUEUE — Visualisasi 5 Kasus Implementasi" + " " * 15 + "║")
    print("║  Struktur Data & Algoritma (Python)" + " " * 21 + "║")
    print("╚" + "═" * 58 + "╝")

    # Kasus 1
    PrinterQueue().run_demo(steps=6)

    # Kasus 2
    HotPotato(passes_per_round=4).run_demo()

    # Kasus 3
    HospitalQueue().run_demo()

    # Kasus 4
    BFSTraversal(BFS_GRAPH, start="A").run_demo()

    # Kasus 5
    AirportSimulation().run_demo()

    print("\n" + "═" * 60)
    print("  Selesai. Semua 5 kasus queue berhasil didemonstrasikan.")
    print("═" * 60 + "\n")


if __name__ == "__main__":
    main()