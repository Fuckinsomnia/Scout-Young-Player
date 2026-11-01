import os
import csv

from clean_text import parse_currency

# Konstanta dalam huruf kapital (Core Concept: Variables & Constants)
DEFAULT_UNKNOWN_VALUE = "N/A"
DEFAULT_ENCODING = "utf-8"

# Lokasi dataset dihitung dari lokasi file ini: <root>/data/fifa19_young.csv
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DEFAULT_CSV_FILE = os.path.join(DATA_DIR, "fifa19_young.csv")

# Kolom wajib yang tidak boleh kosong atau salah format
REQUIRED_FIELDS = ["Name", "Age", "Club", "Position", "Overall", "Potential"]

# Pengelompokan posisi sepak bola
POSITION_GROUPS = {
    "FWD": ["ST", "CF", "LW", "RW"],
    "MID": ["CAM", "CM", "CDM", "LM", "RM"],
    "DEF": ["CB", "LB", "RB", "LWB", "RWB"],
    "GK": ["GK"]
}

# 3 atribut inti yang ditampilkan di profil lengkap pemain
STAT_KEYS = ["Vision", "Reactions", "Composure"]


class Player:
    # Record Class untuk menyimpan data satu pemain muda FIFA 19. Menyimpan atribut identitas, teknis, potensi, dan nilai finansial.
    def __init__(self, data: dict):
        # Identitas dasar (str & int)
        self.name: str = data.get("Name", DEFAULT_UNKNOWN_VALUE)
        self.age: int = int(data.get("Age", 0))
        self.club: str = data.get("Club", DEFAULT_UNKNOWN_VALUE)
        self.position: str = data.get("Position", DEFAULT_UNKNOWN_VALUE)
        self.preferred_foot: str = data.get("Preferred Foot", DEFAULT_UNKNOWN_VALUE)

        # Rating & Pengembangan
        self.overall: int = int(data.get("Overall", 0))
        self.potential: int = int(data.get("Potential", 0))

        # Nilai Finansial (Teks asli & Angka numerik float)
        self.value_str: str = data.get("Value", "€0")
        self.wage_str: str = data.get("Wage", "€0")
        self.release_clause_str: str = data.get("Release Clause", "€0")

        self.value_num: float = parse_currency(self.value_str)
        self.wage_num: float = parse_currency(self.wage_str)

        # Kemampuan / Atribut (dictionary berisi integer)
        self.stats: dict[str, int] = {}
        for key in STAT_KEYS:
            try:
                self.stats[key] = int(data.get(key, 0))
            except (ValueError, TypeError):
                self.stats[key] = 0

        # Nilai Turunan: Growth dihitung dengan operator pengurangan '-'
        self.growth: int = self.potential - self.overall

        # Pengelompokan posisi dihitung saat objek dibuat
        self.position_group: str = "OTHER"
        pos_upper = self.position.upper()
        for group, positions in POSITION_GROUPS.items():
            if pos_upper in positions:
                self.position_group = group
                break

    def __str__(self) -> str:
        # Representasi string rapi saat objek pemain di-print. (OOP __str__)
        return (
            f"{self.name} ({self.age} thn) - {self.club} | "
            f"Pos: {self.position} | OVR: {self.overall} -> POT: {self.potential} (+{self.growth}) | "
            f"Val: {self.value_str}"
        )


class ScoutDatabase:
    # """ Collection Class yang menampung kumpulan objek Player dalam sebuah list. (OOP Collection Class & Lists) """
    def __init__(self):
        self.players: list[Player] = []

    def add_player(self, player: Player) -> None:
        # Menambahkan objek Player ke dalam list database.
        if isinstance(player, Player):
            self.players.append(player)

    def get_all(self) -> list[Player]:
        # Mengembalikan list seluruh pemain.
        return self.players

    def __len__(self) -> int:
        # Mengembalikan total jumlah pemain dalam koleksi.
        return len(self.players)

    def __getitem__(self, index):
        # Mendukung pengindeksan dan slicing langsung (contoh: db[0] atau db[:10]).
        return self.players[index]


def is_valid_row(row: dict) -> bool:
    # Memeriksa kelayakan satu baris data pemain:- Seluruh kolom wajib ada dan tidak kosong - Age, Overall, dan Potential bertipe angka valid
    if not isinstance(row, dict):
        return False

    for field in REQUIRED_FIELDS:
        if not str(row.get(field, "")).strip():
            return False

    try:
        if int(row["Age"]) <= 0 or int(row["Overall"]) <= 0 or int(row["Potential"]) <= 0:
            return False
    except (ValueError, TypeError):
        return False

    return True


def load_dataset(filepath: str = DEFAULT_CSV_FILE) -> tuple[ScoutDatabase, int]:
    # Membaca file CSV pemain muda, melewati baris rusak, dan mengembalikan tuple (ScoutDatabase, jumlah baris yang dilewati).
    database = ScoutDatabase()
    skipped_count = 0

    if not os.path.exists(filepath):
        print(f"[Peringatan] File dataset '{filepath}' tidak ditemukan!")
        return database, skipped_count

    with open(filepath, mode="r", encoding=DEFAULT_ENCODING, errors="replace") as file:
        for row in csv.DictReader(file):
            if is_valid_row(row):
                database.add_player(Player(row))
            else:
                skipped_count += 1

    return database, skipped_count
