from data import Player
from clean_text import ask_int


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


def remove_from_slot(slot_compare: list[Player]):
    # Menghapus satu pemain dari slot komparasi.
    if not slot_compare:
        print("\n  [!] Slot komparasi masih kosong.")
        return

    print("\n--- HAPUS PEMAIN DARI SLOT KOMPARASI ---")
    for i, p in enumerate(slot_compare, start=1):
        print(f"  {i}. {p.name} ({p.club} | Pos: {p.position} | OVR: {p.overall} | POT: {p.potential})")

    idx = ask_int(f"Pilih nomor pemain yang ingin dihapus (1-{len(slot_compare)}, 0=batal): ", 0, len(slot_compare))
    if idx > 0:
        removed = slot_compare.pop(idx - 1)
        print(f"  [OK] '{removed.name}' dihapus dari slot komparasi. Sisa: {len(slot_compare)} pemain.")
