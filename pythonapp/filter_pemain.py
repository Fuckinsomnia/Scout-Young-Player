from clean_text import parse_currency, format_currency, ask_optional_int
from cari_nama import select_from_results
from data import Player, POSITION_GROUPS

# Semua input posisi yang valid: gabungan kode grup + kode posisi spesifik
VALID_POSITIONS = set(POSITION_GROUPS) | {p for positions in POSITION_GROUPS.values() for p in positions}


def ask_position():
    # Meminta posisi dengan validasi: kode posisi (ST, CB, GK), grup (FWD, MID, DEF, GK), ALL, atau 0/Enter untuk skip.
    while True:
        raw = input("Posisi (ST/CB/GK atau grup FWD/MID/DEF/GK, ALL = semua, 0 = skip): ").strip()
        if not raw or raw == "0" or raw.upper() == "ALL":
            return None
        if raw.upper() in VALID_POSITIONS:
            return raw.upper()
        print("  [!] Posisi tidak dikenali. Gunakan kode posisi (ST, CB, GK), grup (FWD, MID, DEF, GK), atau ALL/0 untuk semua.")


def ask_budget():
    # Meminta budget gaji mingguan dengan validasi rentang data (0/Enter = skip).
    while True:
        raw = input("Budget gaji per minggu Anda (€1K - €155K, 0 = skip): ").strip()
        if not raw or raw == "0":
            return None
        val = parse_currency(raw)
        if 1000 <= val <= 155000:
            return val
        print("  [!] Budget harus di antara €1K (pemain termurah) dan €155K (pemain termahal), contoh: 50K atau 50000.")


# 1. Algoritma Sorting Manual (Selection Sort)
def manual_sort(items: list, key_func, descending: bool = True) -> list:
    # Mengurutkan list menggunakan loop manual tanpa memodifikasi data asli.
    result = list(items)
    n = len(result)
    for i in range(n):
        target_idx = i
        for j in range(i + 1, n):
            val_j = key_func(result[j])
            val_target = key_func(result[target_idx])
            if descending:
                if val_j > val_target:
                    target_idx = j
            else:
                if val_j < val_target:
                    target_idx = j
        if target_idx != i:
            result[i], result[target_idx] = result[target_idx], result[i]
    return result


# 2. Filter Kombinasi (Umur + Rating + Posisi + Gaji sekaligus)
def filter_combined(players: list[Player],
                    min_age: int = None, max_age: int = None,
                    min_overall: int = None, max_potential: int = None,
                    position_query: str = None,
                    max_wage: float = None) -> list[Player]:
    # Menyaring pemain dengan kombinasi semua kriteria secara bersamaan. Setiap kriteria bersifat opsional (None = tidak difilter).
    results = []
    for p in players:
        if min_age is not None and p.age < min_age:
            continue
        if max_age is not None and p.age > max_age:
            continue
        if min_overall is not None and p.overall < min_overall:
            continue
        if max_potential is not None and p.potential > max_potential:
            continue
        if position_query:
            pos = position_query.strip().upper()
            if pos not in ("", "ALL"):
                if p.position.upper() != pos and p.position_group != pos:
                    continue
        if max_wage is not None and p.wage_num > max_wage:
            continue
        results.append(p)
    return results


def menu_filter_combined(db) -> list[Player]:
    # Menu filter interaktif: 0 atau Enter = lewati kriteria.
    print("\n--- FILTER PEMAIN GABUNGAN ---")

    min_age = ask_optional_int("Umur minimal (15-21) (0 = untuk skip): ", 15, 21)
    max_age = ask_optional_int("Umur maksimal (15-21) (0 = untuk skip): ", 15, 21)
    if min_age is not None and max_age is not None and min_age > max_age:
        print("  [!] Umur minimal lebih besar dari umur maksimal, keduanya ditukar.")
        min_age, max_age = max_age, min_age

    min_overall = ask_optional_int("Overall rating minimal (40-90) (0 = untuk skip): ", 40, 90)
    max_potential = ask_optional_int("Potensi rating maksimal (75-95) (0 = untuk skip): ", 75, 95)

    position_query = ask_position()
    max_wage = ask_budget()

    kriteria = []
    if min_age is not None or max_age is not None:
        kriteria.append(f"umur {min_age or 15}-{max_age or 21}")
    if min_overall is not None:
        kriteria.append(f"OVR >= {min_overall}")
    if max_potential is not None:
        kriteria.append(f"POT <= {max_potential}")
    if position_query:
        kriteria.append(f"posisi {position_query.upper()}")
    if max_wage is not None:
        kriteria.append(f"budget <= {format_currency(max_wage)}")
    print(f"\nKriteria aktif: {', '.join(kriteria) if kriteria else '(tidak ada, semua pemain)'}")

    results = filter_combined(
        db.get_all(),
        min_age=min_age, max_age=max_age,
        min_overall=min_overall, max_potential=max_potential,
        position_query=position_query,
        max_wage=max_wage,
    )
    return manual_sort(results, key_func=lambda p: (p.potential, p.overall), descending=True)


def run_filter_feature(db, slot_compare: list[Player]):
    # Entry point fitur filter: jalankan menu lalu tampilkan hasilnya.
    results = menu_filter_combined(db)
    select_from_results(results, slot_compare)
