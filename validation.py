# validation.py

import os

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {'.pdf'}

def validate_pdf_file(filename, file_content):
    """
    Przeprowadza walidację na podstawie nazwy pliku i jego wczytanej zawartości (bajtów).
    """
    # Extension validation
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Niedozwolone rozszerzenie pliku: '{ext}'. Akceptowane są tylko pliki .pdf."

    # Check size of the file
    file_length = len(file_content)
    if file_length == 0:
        return False, "Plik jest pusty."
    if file_length > MAX_FILE_SIZE:
        max_size_mb = MAX_FILE_SIZE / (1024 * 1024)
        return False, f"Plik jest za duży. Maksymalny rozmiar to {max_size_mb:.1f} MB."

    # File format validation
    header = file_content[:5]
    if header != b'%PDF-':
        return False, "Zawartość pliku nie wskazuje na format PDF."

    return True, "Plik jest poprawny."