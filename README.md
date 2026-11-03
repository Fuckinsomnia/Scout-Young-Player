# FIFA 19 Scout Player

Program CLI (Command Line Interface) Python untuk membantu scout sepak bola mencari **pemain muda berbakat** dari dataset FIFA 19. Dibuat sebagai proyek Final Exam mata kuliah *Intro to Computer Programming*.

Program hanya menggunakan **standard library Python** (tidak ada pandas/numpy), dan semua sorting ditulis dengan **loop Selection Sort manual** tanpa `sorted()` / `.sort()`.

---

## 1. Dataset

- **Sumber:** [FIFA 19 Complete Player Dataset (javagarm)](https://www.kaggle.com/datasets/javagarm/fifa-19-complete-player-dataset) dari Kaggle
- **Alasan dipilih:** datanya lengkap (18.207 pemain, 89 kolom), menggabungkan data identitas, atribut teknis, dan finansial dalam satu file — cocok untuk fitur scouting yang membutuhkan filter umur, rating, posisi, dan gaji sekaligus.
- **File asli:** `data/fifa19.csv` (18.207 baris, encoding cp1252)

### Proses penyiapan dataset (`trim_dataset.py`)

Batas soal adalah 200–2.000 baris, jadi dataset dipotong dengan filter:

- Umur **≤ 21 tahun** (pemain muda)
- Potential **≥ 75** (berbakat)
- Baris **tanpa Club** dikeluarkan (penanganan sel kosong)
- Baris dengan Age/Potential yang bukan angka dilewati dengan `try/except`

Hasilnya disimpan ke **`fifa19_young.csv`** (1.988 baris, UTF-8, sefolder dengan `main.py`) dengan hanya 13 kolom yang dipakai program:

| Kelompok | Kolom |
|---|---|
| Identitas | `Name`, `Age`, `Club`, `Position`, `Preferred Foot` |
| Rating | `Overall`, `Potential` |
| Finansial | `Value`, `Wage`, `Release Clause` |
| Atribut inti | `Vision`, `Reactions`, `Composure` |

Kolom lain dari dataset asli (Foto, Nationality, atribut teknis/fisik lain, dll.) tidak dipakai dan dibuang saat trim agar file kecil dan mudah dibaca.

### Validasi saat loading (`pythonapp/data.py`)

Saat program berjalan, `load_dataset()` memvalidasi setiap baris lewat `is_valid_row()`:

- Kolom wajib (`Name`, `Age`, `Club`, `Position`, `Overall`, `Potential`) harus terisi
- `Age`, `Overall`, `Potential` harus angka yang valid

Baris yang rusak **dilewati tanpa membuat program crash** dan jumlahnya dihitung, lalu dilaporkan saat program mulai: **1.983 pemain berhasil dimuat, 5 baris dilewati**.

### Penanganan kolom dengan sel kosong

Kolom `Release Clause` kosong pada 270 baris yang tetap dimuat — pemain seperti itu ditampilkan dengan nilai `€0` (default di `data.py`). Kolom lain yang kosong (Position, Vision, Reactions, Preferred Foot) hanya ada di 5 baris rusak yang memang di-skip loader. Kolom `Value`, `Wage`, `Name`, `Age`, `Club`, `Overall`, `Potential` terisi lengkap di semua baris.

---

## 2. Struktur Proyek

```text
Scout Player/
├── main.py                  # Entry point: menu utama CLI
├── fifa19_young.csv         # Dataset hasil trim (UTF-8, 13 kolom)
├── test_project.py          # Runner seluruh unit test
├── trim_dataset.py          # Script pemotong dataset (dijalankan sekali)
├── data/
│   └── fifa19.csv           # Dataset asli dari Kaggle (cp1252, sumber trim)
└── pythonapp/
    ├── clean_text.py        # Util teks: normalisasi nama, parse/format uang, input angka
    ├── data.py              # Class Player, ScoutDatabase, loader CSV + validasi baris
    ├── cari_nama.py         # Fitur 1: cari nama, tabel hasil, profil lengkap, pemilihan pemain
    ├── filter_pemain.py     # Fitur 2: filter gabungan + sorting manual (Selection Sort)
    ├── komparasi.py         # Fitur 3: komparasi pemain di slot berdampingan
    └── tests/
        ├── test_clean_text.py
        ├── test_data.py
        └── test_fitur.py
```

---

## 3. Cara Menjalankan

Jalankan dari folder root proyek (`Scout Player/`):

```powershell
# Menjalankan program utama
python main.py

# Menjalankan seluruh unit test (19 test) — dua cara sama-sama bisa
python test_project.py
python -m unittest

# (Sekali saja) memotong dataset asli menjadi fifa19_young.csv
python trim_dataset.py
```

---

## 4. Fitur Program

### Menu Utama

```text
MENU UTAMA:
  Slot Komparasi (0 pemain)
  1. Cari Berdasarkan Nama
  2. Filter Pemain (Umur, Rating, Posisi, Gaji)
  3. Komparasi pemain yg di pilih
  4. Hapus Pemain dari Slot Komparasi
  0. Keluar
```

**1. Cari Berdasarkan Nama** — pencarian nama pemain yang tidak sensitif huruf besar/kecil dan mengabaikan aksen (contoh: mengetik `mbappe` tetap menemukan "K. Mbappé", `joao felix` menemukan "João Félix").

**2. Filter Pemain** — menyaring pemain dengan **semua kriteria sekaligus**: umur (15–21), overall minimal, potensi maksimal, posisi (kode `ST`/`CB`/`GK` atau grup `FWD`/`MID`/`DEF`/`GK`), dan budget gaji mingguan (€1K–€155K, sesuai gaji pemain termurah–termahal di data). Ketik **0 atau Enter** pada kriteria mana pun untuk melewatinya. Hasil diurutkan dari potensi tertinggi dengan Selection Sort manual.

**3. Komparasi Pemain Terpilih** — menampilkan tabel semua pemain yang sudah di-select di slot komparasi secara berdampingan (Usia, Posisi, Overall, Potensi, Gaji, Value). Slot bisa menampung berapa saja pemain, minimal 2 untuk bisa dibandingkan.

**4. Hapus Pemain dari Slot Komparasi** — mengeluarkan satu pemain dari slot komparasi (misalnya yang tidak jadi dibandingkan), lengkap dengan konfirmasi nomor dan batal (0).

### Menu Pemain Terpilih (muncul setelah memilih nomor pemain dari hasil pencarian/filter)

```text
>> Pemain Terpilih: K. Mbappé (Paris Saint-Germain | Pos: RM | OVR: 88 | POT: 95)
Pilihan Menu:
  1. Select pemain ini untuk komparasi
  2. Lihat profil lengkap
  3. Cari pemain lain (kembali ke menu)
```

- **Select untuk komparasi** — menyimpan pemain ke slot komparasi (nama yang sama tidak bisa dimasukkan dua kali)
- **Lihat profil lengkap** — identitas, rating, dua nilai turunan (pertumbuhan `Potential − Overall` dan gaji tahunan `Wage × 52`), nilai finansial, dan 3 atribut inti dalam format list

Semua input angka divalidasi dengan loop (input salah akan diminta ulang, program tidak pernah crash).

---

## 5. Pemetaan 8 Konsep Inti

| Konsep | File | Fungsi / Lokasi |
|---|---|---|
| 1. Variables & Constants | `pythonapp/clean_text.py` | `CURRENCY_SYMBOL`, `MILLION_MULTIPLIER`, `THOUSAND_MULTIPLIER`; `DEFAULT_CSV_FILE`, `REQUIRED_FIELDS`, `POSITION_GROUPS` di `data.py` |
| 2. Data Types | `pythonapp/data.py` | `Player.__init__` — konversi `str → int` (Age, Overall) dan `str → float` (`parse_currency`) |
| 3. Operators | `pythonapp/data.py`, `pythonapp/filter_pemain.py` | Dua nilai turunan: `growth = potential - overall` dan `yearly_wage = wage_num * 52`; operator perbandingan dan logika `and` di `filter_combined` |
| 4. Conditional Statements | `pythonapp/clean_text.py` | `parse_currency` (if/elif/else untuk suffix K/M); `is_valid_row` di `data.py` |
| 5. Loops | `pythonapp/filter_pemain.py`, `pythonapp/data.py` | `manual_sort` (nested `for`, Selection Sort); loop `while` menu utama di `main.py`; `for` pembaca CSV |
| 6. Functions | semua modul | parameter opsional dengan nilai default, mis. `filter_combined(players, min_age=None, ...)` |
| 7. OOP | `pythonapp/data.py` | `Player` (record class dengan `__str__`) dan `ScoutDatabase` (collection class dengan `add_player`, `get_all`, `__len__`, `__getitem__`) |
| 8. Lists & Dictionaries | `pythonapp/data.py`, `pythonapp/cari_nama.py` | `stats` (dict atribut), `POSITION_GROUPS` (dict), `slot_compare` (list), baris CSV dari `csv.DictReader` (list of dict) |

Konsep **string manipulation** juga terpakai di `clean_text` (`.strip()`, `.lower()`, `.replace()`, `.translate()`, `.split()`, `.join()`) dan **file I/O** di `data.py` / `trim_dataset.py` (`csv.DictReader` / `csv.DictWriter`).

---

## 6. Unit Test

19 test berjalan otomatis lewat `unittest`:

| File | Yang diuji |
|---|---|
| `test_clean_text.py` | `clean_text`, `parse_currency`, `format_currency` (input normal, edge case, bad input) |
| `test_data.py` | `Player` (atribut, growth, pengelompokan posisi, `__str__`), `ScoutDatabase`, `is_valid_row`, `load_dataset` |
| `test_fitur.py` | `search_by_name`, `manual_sort`, `filter_combined` |

---

## 7. Keterbatasan

- Dataset dipotong hanya ke pemain muda (umur ≤ 21, Potential ≥ 75), jadi tidak bisa mencari pemain senior.
- Filter hanya mendukung 13 kolom yang disimpan; atribut teknis lain (Finishing, Dribbling, dll.) tidak tersedia.
- Angka batas filter (umur 15–21, OVR 40–90, POT 75–95, gaji €1K–€155K) diambil dari rentang data aktual; memasukkan angka di luar rentang itu akan ditolak.
- Tabel komparasi memotong nama pemain 16 karakter agar tetap muat di layar terminal.

---

## 8. Video Penjelasan

Link video: https://youtu.be/wYBaJNNYZEg?si=J02qngd4KmsNHU8T
