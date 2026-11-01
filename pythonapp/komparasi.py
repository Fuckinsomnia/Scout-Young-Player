from data import Player


def run_comparison_feature(slot_compare: list[Player]):
    # Menampilkan tabel komparasi semua pemain di slot berdampingan.
    print("\n--- KOMPARASI PEMAIN TERPILIH ---")
    if len(slot_compare) < 2:
        print("  [!] Slot komparasi perlu minimal 2 pemain. Cari pemain lewat menu 1-2 dulu!")
        return

    col_w = 16
    header = f"{'Statistik':<16} | " + " | ".join(f"{p.name[:col_w]:<{col_w}}" for p in slot_compare)
    print(f"\n{header}")
    print("-" * len(header))

    rows = [
        ("Usia", [str(p.age) for p in slot_compare]),
        ("Posisi", [p.position for p in slot_compare]),
        ("Overall", [str(p.overall) for p in slot_compare]),
        ("Potensi", [str(p.potential) for p in slot_compare]),
        ("Gaji", [p.wage_str for p in slot_compare]),
        ("Value", [p.value_str for p in slot_compare]),
    ]
    for label, vals in rows:
        print(f"{label:<16} | " + " | ".join(f"{str(v)[:col_w]:<{col_w}}" for v in vals))
    print("-" * len(header) + "\n")
