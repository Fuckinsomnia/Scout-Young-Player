CURRENCY_SYMBOL = "€"
MILLION_MULTIPLIER = 1_000_000.0
THOUSAND_MULTIPLIER = 1_000.0

# Tabel penggantian karakter beraksen (contoh: é -> e)
ACCENT_TABLE = str.maketrans(
    "éèêëáàâãäíìîïóòôõöúùûüñçćšžø",
    "eeeeeaaaaaiiiiooooouuuuncszo"
)


def ask_int(prompt: str, min_val: int, max_val: int) -> int:
    # Membaca integer dari user dengan validasi.
    while True:
        try:
            val = int(input(prompt).strip())
            if min_val <= val <= max_val:
                return val
            print(f"  [!] Masukkan angka antara {min_val} dan {max_val}.")
        except ValueError:
            print("  [!] Input harus berupa angka bulat.")


def ask_optional_int(prompt: str, min_val: int, max_val: int):
    # Sama seperti ask_int, tetapi Enter atau 0 berarti kriteria dilewati.
    while True:
        raw = input(prompt).strip()
        if not raw:
            return None
        try:
            val = int(raw)
            if val == 0:
                return None
            if min_val <= val <= max_val:
                return val
            print(f"  [!] Masukkan angka antara {min_val} dan {max_val}, 0 atau Enter untuk lewati.")
        except ValueError:
            print("  [!] Input harus berupa angka bulat, 0 atau Enter untuk lewati.")


def clean_text(text: str) -> str:
    # Membersihkan teks untuk pencarian yang fleksibel (case-insensitive & accent-insensitive).
    if not isinstance(text, str):
        return ""
    cleaned = text.strip().lower().translate(ACCENT_TABLE).replace("-", " ")
    return " ".join(cleaned.split())


def parse_currency(value_str: str) -> float:
    # Mengonversi string nilai transfer/gaji pemain ke angka numerik (float). Contoh: '€110.5M' -> 110500000.0, '€565K' -> 565000.0, '€0' -> 0.0
    if not value_str or not isinstance(value_str, str):
        return 0.0

    raw = value_str.strip().replace(CURRENCY_SYMBOL, "").replace(" ", "").upper()
    if not raw:
        return 0.0

    try:
        # Percabangan minimal 3 kondisi (Core Concept: Conditional Statements)
        if raw.endswith("M"):
            return float(raw[:-1]) * MILLION_MULTIPLIER
        elif raw.endswith("K"):
            return float(raw[:-1]) * THOUSAND_MULTIPLIER
        else:
            return float(raw)
    except ValueError:
        return 0.0


def format_currency(amount: float) -> str:
    # Mengubah nilai numerik kembali ke bentuk teks mata uang ringkas. Contoh: 110500000.0 -> '€110.5M', 565000.0 -> '€565K', 0 -> '€0'
    if not isinstance(amount, (int, float)) or amount <= 0:
        return f"{CURRENCY_SYMBOL}0"

    if amount >= MILLION_MULTIPLIER:
        return f"{CURRENCY_SYMBOL}{amount / MILLION_MULTIPLIER:.1f}M"
    elif amount >= THOUSAND_MULTIPLIER:
        return f"{CURRENCY_SYMBOL}{amount / THOUSAND_MULTIPLIER:.0f}K"
    else:
        return f"{CURRENCY_SYMBOL}{amount:.0f}"
