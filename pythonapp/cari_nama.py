from clean_text import clean_text, ask_int
from data import Player


def search_by_name(players: list[Player], query: str) -> list[Player]:
    # Mencari pemain berdasarkan nama (case-insensitive & pembersihan ketikan).
    q = clean_text(query)
    if not q:
        return []
    return [p for p in players if q in clean_text(p.name)]


def print_table(players: list[Player], title: str, limit: int):
    # Menampilkan tabel pemain.
    sub = players[:limit]
    print(f"\n--- {title} (Menampilkan {len(sub)} dari {len(players)}) ---")
    print(f"{'No':<3} | {'Nama':<20} | {'Usia':<4} | {'Klub':<18} | {'Pos':<4} | {'OVR':<3} | {'POT':<3} | {'Gaji':<7} | {'Nilai':<7}")
    print("-" * 78)
    for i, p in enumerate(sub, start=1):
        print(f"{i:<3} | {p.name[:20]:<20} | {p.age:<4} | {p.club[:18]:<18} | {p.position:<4} | {p.overall:<3} | {p.potential:<3} | {p.wage_str:<7} | {p.value_str:<7}")
    print("-" * 78)


def print_detail_card(p: Player):
    # Menampilkan profil lengkap satu pemain.
    print(f"\n=== PROFIL LENGKAP: {p.name.upper()} ===")
    print(f"  Klub           : {p.club}")
    print(f"  Posisi         : {p.position} ({p.position_group})")
    print(f"  Usia           : {p.age} thn")
    print(f"  Kaki           : {p.preferred_foot}")
    print(f"  Overall        : {p.overall}")
    print(f"  Potensi        : {p.potential} (Pertumbuhan: +{p.growth})")
    print(f"  Value          : {p.value_str}")
    print(f"  Gaji           : {p.wage_str}/minggu")
    print(f"  Release Clause : {p.release_clause_str}")
    print("  Atribut Inti:")
    for k, v in p.stats.items():
        print(f"    - {k:<10}: {v}")


def handle_selected_player(player: Player, slot_compare: list[Player]):
    # Menu setelah seorang pemain dipilih.
    while True:
        print(f"\n>> Pemain Terpilih: {player.name} ({player.club} | Pos: {player.position} | OVR: {player.overall} | POT: {player.potential})")
        print("Pilihan Menu:")
        print("  1. Select pemain ini untuk komparasi")
        print("  2. Lihat profil lengkap")
        print("  3. Cari pemain lain (kembali ke menu)")

        act = ask_int("Pilih menu (1-3): ", 1, 3)

        if act == 1:
            if any(p.name == player.name for p in slot_compare):
                print(f"  [!] {player.name} sudah ada di dalam slot komparasi.")
            else:
                slot_compare.append(player)
                print(f"  [OK] '{player.name}' berhasil di-select untuk komparasi! (total {len(slot_compare)} pemain)")
            break

        elif act == 2:
            print_detail_card(player)

        elif act == 3:
            break


def select_from_results(results: list[Player], slot_compare: list[Player]):
    # Menampilkan hasil pencarian lalu meminta pemain yang ingin di-select.
    if not results:
        print("  [!] Tidak ada pemain yang cocok dengan kriteria.")
        return

    limit = min(len(results), 15)
    print_table(results, "HASIL FILTER", limit)
    idx = ask_int(f"Pilih nomor pemain untuk di-select (1-{limit}, 0=batal): ", 0, limit)
    if idx > 0:
        handle_selected_player(results[idx - 1], slot_compare)
