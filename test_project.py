"""
test_project.py
Runner utama unit test (sesuai spesifikasi lembar soal ujian).

Dapat dijalankan dari folder root proyek dengan:
    python test_project.py
atau
    python -m unittest
"""

import os
import sys
import unittest

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "pythonapp"))
sys.path.insert(0, os.path.join(ROOT, "pythonapp", "tests"))

from test_clean_text import TestCleanText
from test_data import TestData
from test_fitur import TestFitur


if __name__ == "__main__":
    print("Menjalankan seluruh unit test proyek Scout Player...\n")
    unittest.main(verbosity=2)
