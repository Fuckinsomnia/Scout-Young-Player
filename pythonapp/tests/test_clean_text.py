import sys
import os
import unittest

# Menambahkan direktori root agar modul clean_text dapat di-import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from clean_text import clean_text, parse_currency, format_currency


# ==========================================
# 1. Test Functions (Assert-based)
# ==========================================

def test_clean_text_normal():
    """Menguji pembersihan teks standar."""
    result = clean_text("Erling Haaland")
    assert result == "erling haaland", f"Expected 'erling haaland', got '{result}'"


def test_clean_text_accents_and_spaces():
    """Menguji normalisasi karakter beraksen dan spasi berlebih."""
    assert clean_text("  K. Mbappé  ") == "k. mbappe"
    assert clean_text("João-Félix") == "joao felix"
    assert clean_text("   Ousmane    Dembélé   ") == "ousmane dembele"


def test_clean_text_edge_and_bad_input():
    """Menguji kasus ekstrem (string kosong) dan tipe data salah (None, int)."""
    assert clean_text("") == ""
    assert clean_text("     ") == ""
    assert clean_text(None) == ""
    assert clean_text(12345) == ""


def test_parse_currency_normal():
    """Menguji parsing format mata uang Millions (M) dan Thousands (K)."""
    assert parse_currency("€110.5M") == 110500000.0
    assert parse_currency("€565K") == 565000.0
    assert parse_currency("€500") == 500.0


def test_parse_currency_edge_and_bad_input():
    """Menguji kasus batas (0, kosong) dan input tidak valid (teks acak, None)."""
    assert parse_currency("€0") == 0.0
    assert parse_currency("") == 0.0
    assert parse_currency(None) == 0.0
    assert parse_currency("bukan_angka") == 0.0


def test_format_currency_all_ranges():
    """Menguji konversi angka ke string ringkas (€M, €K, nominal kecil, dan 0)."""
    assert format_currency(110500000.0) == "€110.5M"
    assert format_currency(565000.0) == "€565K"
    assert format_currency(500.0) == "€500"
    assert format_currency(0) == "€0"
    assert format_currency(-100) == "€0"


# ==========================================
# 2. Unittest TestCase Wrapper
# ==========================================

class TestCleanText(unittest.TestCase):
    def test_clean_text_normal(self):
        test_clean_text_normal()

    def test_clean_text_accents(self):
        test_clean_text_accents_and_spaces()

    def test_clean_text_bad_input(self):
        test_clean_text_edge_and_bad_input()

    def test_parse_currency(self):
        test_parse_currency_normal()
        test_parse_currency_edge_and_bad_input()

    def test_format_currency(self):
        test_format_currency_all_ranges()


# ==========================================
# 3. Direct Script Runner
# ==========================================

if __name__ == "__main__":
    print("Menjalankan pengujian assert untuk clean_text.py...")
    test_clean_text_normal()
    test_clean_text_accents_and_spaces()
    test_clean_text_edge_and_bad_input()
    test_parse_currency_normal()
    test_parse_currency_edge_and_bad_input()
    test_format_currency_all_ranges()
    print("-> Semua fungsi assert pada test_clean_text.py BERHASIL 100%!")

