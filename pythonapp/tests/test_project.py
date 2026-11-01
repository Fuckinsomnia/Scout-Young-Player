"""
tests/test_project.py
File runner utama unit test (sesuai spesifikasi lembar soal ujian).
Mengumpulkan seluruh TestCase dari folder tests/.

Dapat dijalankan dari folder root proyek dengan:
    python pythonapp/tests/test_project.py
"""

import unittest
from test_clean_text import TestCleanText
from test_data import TestData
from test_fitur import TestFitur


if __name__ == "__main__":
    print("Menjalankan seluruh unit test proyek Scout Player...\n")
    unittest.main(verbosity=2)
