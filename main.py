import os
import sys

# Menambahkan folder pythonapp ke path agar modul bisa di-import
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "pythonapp"))

# Konfigurasi console Windows untuk UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

from data import load_dataset, DEFAULT_CSV_FILE
from clean_text import ask_int
from cari_nama import search_by_name, select_from_results
from filter_pemain import run_filter_feature
from komparasi import run_comparison_feature, remove_from_slot


def main():
    print("=== FIFA 19 SCOUT PLAYER ===")
    db, skipped = load_dataset(DEFAULT_CSV_FILE)
    print(f"Data Berhasil Dimuat: {len(db)} pemain | Baris Dilewati: {skipped}")

    slot_compare = []

    while True:
        print("\nMENU UTAMA:")
        print(f"  Slot Komparasi ({len(slot_compare)} pemain)")
        print("  1. Cari Berdasarkan Nama")
        print("  2. Filter Pemain (Umur, Rating, Posisi, Gaji)")
        print("  3. Komparasi pemain yg di pilih")
        print("  4. Hapus Pemain dari Slot Komparasi")
        print("  0. Keluar")

        opt = ask_int("Pilih menu (0-4): ", 0, 4)

        if opt == 1:
            q = input("\nMasukkan nama pemain: ").strip()
            results = search_by_name(db.get_all(), q)
            select_from_results(results, slot_compare)

        elif opt == 2:
            run_filter_feature(db, slot_compare)

        elif opt == 3:
            run_comparison_feature(slot_compare)

        elif opt == 4:
            remove_from_slot(slot_compare)

        elif opt == 0:
            print("\nTerima kasih telah menggunakan Scout Player. Sampai jumpa!")
            break


if __name__ == "__main__":
    main()
