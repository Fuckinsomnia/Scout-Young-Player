"""
tests/test_fitur.py
Unit test untuk fitur cari nama (search_by_name), sorting manual,
dan filter gabungan (filter_combined).
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data import Player
from cari_nama import search_by_name
from filter_pemain import manual_sort, filter_combined


def create_dummy_players():
    p1 = Player({
        "Name": "Kylian Mbappé", "Age": "19", "Club": "Paris Saint-Germain",
        "Position": "RM", "Overall": "88", "Potential": "95",
        "Value": "€81M", "Wage": "€100K",
        "Vision": "82", "Reactions": "87", "Composure": "86"
    })
    p2 = Player({
        "Name": "Matthijs de Ligt", "Age": "18", "Club": "Ajax",
        "Position": "CB", "Overall": "82", "Potential": "91",
        "Value": "€27M", "Wage": "€11K",
        "Vision": "63", "Reactions": "79", "Composure": "82"
    })
    return [p1, p2]


# ==========================================
# Test Functions
# ==========================================

def test_manual_sort():
    nums = [3, 1, 4, 2]
    assert manual_sort(nums, lambda x: x, descending=False) == [1, 2, 3, 4]
    assert manual_sort(nums, lambda x: x, descending=True) == [4, 3, 2, 1]


def test_search_by_name():
    players = create_dummy_players()
    assert len(search_by_name(players, "mbappe")) == 1
    assert len(search_by_name(players, "de ligt")) == 1
    assert len(search_by_name(players, "bukan_pemain")) == 0
    assert len(search_by_name(players, "")) == 0


def test_filter_combined():
    players = create_dummy_players()
    # Tanpa kriteria: semua pemain lolos
    assert len(filter_combined(players)) == 2
    # Umur minimal 19: hanya Mbappé (19)
    assert len(filter_combined(players, min_age=19)) == 1
    # Budget gaji 20K: hanya De Ligt (€11K)
    assert len(filter_combined(players, max_wage=20_000.0)) == 1
    # Grup posisi DEF: hanya De Ligt (CB)
    assert len(filter_combined(players, position_query="DEF")) == 1
    # Potensi maksimal 90: tidak ada (95 dan 91)
    assert len(filter_combined(players, max_potential=90)) == 0


# ==========================================
# Unittest TestCase Wrapper
# ==========================================

class TestFitur(unittest.TestCase):
    def test_sort(self):
        test_manual_sort()

    def test_search_name(self):
        test_search_by_name()

    def test_filter_combined(self):
        test_filter_combined()


if __name__ == "__main__":
    print("Menjalankan pengujian assert untuk fitur...")
    test_manual_sort()
    test_search_by_name()
    test_filter_combined()
    print("-> Semua fungsi assert pada test_fitur.py BERHASIL 100%!")
