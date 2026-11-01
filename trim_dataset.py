import csv

INPUT_CSV = "data/fifa19.csv"
OUTPUT_CSV = "fifa19_young.csv"

# 13 kolom yang dipakai program scouting
TARGET_COLUMNS = [
    # Identitas
    "Name", "Age", "Club", "Position", "Preferred Foot",
    # Rating
    "Overall", "Potential",
    # Finansial
    "Value", "Wage", "Release Clause",
    # Atribut inti (profil lengkap pemain)
    "Vision", "Reactions", "Composure"
]

def trim_dataset(input_file: str, output_file: str):
    print(f"Membaca {input_file} (cp1252)...")
    
    total_raw = 0
    skipped_no_club = 0
    skipped_filter = 0
    qualified_rows = []

    with open(input_file, mode="r", encoding="cp1252", errors="replace") as infile:
        reader = csv.DictReader(infile)
        
        for row in reader:
            total_raw += 1
            club = row.get("Club", "").strip()
            
            # Lewati baris tanpa club
            if not club:
                skipped_no_club += 1
                continue
            
            # Cek umur dan potensi
            try:
                age = int(row.get("Age", 0))
                potential = int(row.get("Potential", 0))
            except ValueError:
                skipped_filter += 1
                continue
            
            # Filter pemain muda berbakat
            if age <= 21 and potential >= 75:
                # Simpan hanya kolom target
                filtered_row = {col: row.get(col, "").strip() for col in TARGET_COLUMNS}
                qualified_rows.append(filtered_row)
            else:
                skipped_filter += 1

    print(f"Total baris asli: {total_raw}")
    print(f"Dilewati (tanpa club): {skipped_no_club}")
    print(f"Dilewati (tidak memenuhi kriteria): {skipped_filter}")
    print(f"Baris terpilih (termasuk bad rows untuk demo loader): {len(qualified_rows)}")

    # Tulis ke fifa19_young.csv
    with open(output_file, mode="w", encoding="utf-8", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=TARGET_COLUMNS)
        writer.writeheader()
        writer.writerows(qualified_rows)

    print(f"Berhasil menyimpan {len(qualified_rows)} baris ke {output_file} (UTF-8).")

if __name__ == "__main__":
    trim_dataset(INPUT_CSV, OUTPUT_CSV)

