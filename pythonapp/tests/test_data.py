import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data import Player, ScoutDatabase, is_valid_row, load_dataset, DEFAULT_CSV_FILE


def create_sample_player_data():
    """Helper untuk membuat data dummy pemain muda valid."""
    return {
        "Name": "K. Mbappé",
        "Age": "19",
        "Nationality": "France",
        "Club": "Paris Saint-Germain",
        "Position": "RM",
        "Overall": "88",
        "Potential": "95",
        "Value": "€81M",
        "Wage": "€100K",
        "Vision": "82",
        "Reactions": "87",
        "Composure": "86"
    }


# ==========================================
# 1. Test Class Player
# ==========================================

def test_player_initialization_and_types():
    data = create_sample_player_data()
    player = Player(data)

    assert player.name == "K. Mbappé"
    assert player.age == 19
    assert isinstance(player.age, int)
    assert player.overall == 88
    assert player.potential == 95
    assert player.value_num == 81_000_000.0
    assert player.wage_num == 100_000.0


def test_player_derived_growth():
    """Menguji perhitungan turunan: growth = potential - overall."""
    data = create_sample_player_data()
    player = Player(data)
    assert player.growth == 7  # 95 - 88 = 7

    # Edge case: pemain yang sudah mencapai potensi maksimal (growth == 0)
    data["Overall"] = "90"
    data["Potential"] = "90"
    player_max = Player(data)
    assert player_max.growth == 0


def test_player_position_grouping():
    """Menguji pengelompokan posisi (FWD, MID, DEF, GK, OTHER)."""
    data = create_sample_player_data()

    # RM -> MID
    player = Player(data)
    assert player.position_group == "MID"

    # ST -> FWD
    data["Position"] = "ST"
    assert Player(data).position_group == "FWD"

    # CB -> DEF
    data["Position"] = "CB"
    assert Player(data).position_group == "DEF"

    # Posisi tidak dikenal -> OTHER
    data["Position"] = "UNKNOWN"
    assert Player(data).position_group == "OTHER"


def test_player_str_representation():
    """Menguji method __str__ pada Player menghasilkan teks yang rapi."""
    data = create_sample_player_data()
    player = Player(data)
    str_output = str(player)

    assert "Mbappé" in str_output
    assert "Paris Saint-Germain" in str_output
    assert "OVR: 88" in str_output
    assert "POT: 95" in str_output
    assert "(+7)" in str_output


# ==========================================
# 2. Test Class ScoutDatabase
# ==========================================

def test_scout_database_operations():
    """Menguji class koleksi ScoutDatabase: add_player, len, indexing, get_all."""
    db = ScoutDatabase()
    assert len(db) == 0

    p1 = Player(create_sample_player_data())
    db.add_player(p1)

    assert len(db) == 1
    assert db[0].name == "K. Mbappé"
    assert len(db.get_all()) == 1

    # Uji coba penambahan pemain non-Player (bad input)
    db.add_player("Bukan objek Player")
    assert len(db) == 1  # Tidak bertambah karena divalidasi


# ==========================================
# 3. Test Loader CSV (is_valid_row & load_dataset)
# ==========================================

def test_is_valid_row_success():
    """Menguji baris dengan data lengkap dan valid."""
    row = {
        "Name": "Pedri",
        "Age": "18",
        "Club": "FC Barcelona",
        "Position": "CM",
        "Overall": "81",
        "Potential": "91"
    }
    assert is_valid_row(row) is True


def test_is_valid_row_missing_fields():
    """Menguji baris dengan kolom penting yang kosong."""
    row_no_club = {
        "Name": "Pedri",
        "Age": "18",
        "Club": "",
        "Position": "CM",
        "Overall": "81",
        "Potential": "91"
    }
    assert is_valid_row(row_no_club) is False

    row_no_pos = {
        "Name": "Pedri",
        "Age": "18",
        "Club": "FC Barcelona",
        "Position": "   ",
        "Overall": "81",
        "Potential": "91"
    }
    assert is_valid_row(row_no_pos) is False


def test_is_valid_row_invalid_numbers():
    """Menguji baris dengan format angka yang rusak."""
    row_bad_age = {
        "Name": "Pedri",
        "Age": "dua_puluh",
        "Club": "FC Barcelona",
        "Position": "CM",
        "Overall": "81",
        "Potential": "91"
    }
    assert is_valid_row(row_bad_age) is False


def test_is_valid_row_non_dict_input():
    """Menguji edge case input bukan dictionary."""
    assert is_valid_row(None) is False
    assert is_valid_row("string") is False
    assert is_valid_row([1, 2, 3]) is False


def test_load_dataset_from_csv():
    """Menguji pembacaan dataset fifa19_young.csv."""
    db, skipped = load_dataset(DEFAULT_CSV_FILE)

    assert isinstance(db, ScoutDatabase)
    assert len(db) == 1983, f"Expected 1983 loaded players, got {len(db)}"
    assert skipped == 5, f"Expected 5 skipped rows, got {skipped}"
    assert db[0].name != ""


def test_load_dataset_file_not_found():
    """Menguji penanganan jika file CSV tidak ditemukan (tidak boleh crash)."""
    db, skipped = load_dataset("file_tidak_ada.csv")
    assert isinstance(db, ScoutDatabase)
    assert len(db) == 0
    assert skipped == 0


# ==========================================
# 4. Unittest TestCase Wrapper
# ==========================================

class TestData(unittest.TestCase):
    def test_player_initialization(self):
        test_player_initialization_and_types()

    def test_growth(self):
        test_player_derived_growth()

    def test_position_group(self):
        test_player_position_grouping()

    def test_str(self):
        test_player_str_representation()

    def test_database(self):
        test_scout_database_operations()

    def test_valid_row(self):
        test_is_valid_row_success()

    def test_missing_fields(self):
        test_is_valid_row_missing_fields()

    def test_invalid_numbers(self):
        test_is_valid_row_invalid_numbers()

    def test_non_dict(self):
        test_is_valid_row_non_dict_input()

    def test_load_csv(self):
        test_load_dataset_from_csv()

    def test_missing_file(self):
        test_load_dataset_file_not_found()


if __name__ == "__main__":
    print("Menjalankan pengujian assert untuk data.py...")
    test_player_initialization_and_types()
    test_player_derived_growth()
    test_player_position_grouping()
    test_player_str_representation()
    test_scout_database_operations()
    test_is_valid_row_success()
    test_is_valid_row_missing_fields()
    test_is_valid_row_invalid_numbers()
    test_is_valid_row_non_dict_input()
    test_load_dataset_from_csv()
    test_load_dataset_file_not_found()
    print("-> Semua fungsi assert pada test_data.py BERHASIL 100%!")
