import os
import re
import PyPDF2
from colorama import init, Fore, Style

# Inicjalizacja colorama
init(autoreset=True)


def extract_start_date_from_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            first_page = pdf_reader.pages[0]
            text = first_page.extract_text()
            match = re.search(r'początek:\s*(\d{2})\s*[-–—]\s*(\d{2})\s*[-–—]\s*(\d{4})', text)
            if match:
                day, month, year = match.groups()
                return f"{year}/data_{month.zfill(2)}.pdf"
            else:
                print(f"{Fore.RED}✗ Nie znaleziono daty rozpoczęcia w pliku: {pdf_path}")
                return None
    except Exception as e:
        print(f"{Fore.RED}✗ Błąd podczas przetwarzania pliku {pdf_path}: {e}")
        return None


def verify_data_structure(base_directory):
    # Definiowanie oczekiwanych lat i liczby plików na rok
    expected_years = [str(year) for year in range(2018, 2025)]
    expected_files = {
        "2018": 12,
        "2019": 12,
        "2020": 12,
        "2021": 12,
        "2022": 12,
        "2023": 12,
        "2024": 4
    }

    exceptions = {
        "17stycznia/2023": Fore.YELLOW + "⚠ Brak danych wejściowych w 17stycznia/2023",
        "kossutha/2019": Fore.YELLOW + "⚠ Brak danych wejściowych w kossutha/2019"
    }

    # Przechodzenie przez wszystkie katalogi w bazowym katalogu
    for parent_folder in os.listdir(base_directory):
        parent_path = os.path.join(base_directory, parent_folder)
        if os.path.isdir(parent_path):
            print(f"{Style.BRIGHT}Sprawdzanie katalogu: {parent_path}")
            # Sprawdzanie obecności wymaganych lat
            for year in expected_years:
                year_path = os.path.join(parent_path, year)
                if os.path.exists(year_path):
                    # Sprawdzanie liczby plików PDF w każdym roku
                    files = [f for f in os.listdir(year_path) if f.endswith('.pdf')]
                    if len(files) != expected_files[year]:
                        exception_key = f"{parent_folder}/{year}"
                        if exception_key in exceptions:
                            print(exceptions[exception_key])
                        else:
                            print(
                                f"{Fore.RED}✗ Błąd: {parent_path}/{year} ma {len(files)} plików zamiast {expected_files[year]}")
                    else:
                        # Weryfikacja nazw plików i dat w plikach PDF
                        all_correct = True
                        for file in files:
                            if file == '.DS_Store':
                                continue
                            file_path = os.path.join(year_path, file)
                            expected_path = extract_start_date_from_pdf(file_path)
                            if expected_path and expected_path != f"{year}/{file}":
                                all_correct = False
                                print(
                                    f"{Fore.RED}✗ Błąd: plik {file} w {year_path} ma nieprawidłową datę rozpoczęcia pomiaru. Oczekiwano {expected_path}")
                        if all_correct:
                            print(f"{Fore.GREEN}✔ Poprawnie zweryfikowano {parent_path}/{year}")
                else:
                    print(f"{Fore.RED}✗ Błąd: brak folderu {parent_path}/{year}")
        else:
            print(f"{Fore.RED}✗ Błąd: {parent_path} nie jest katalogiem")


# Podaj ścieżkę do bazowego katalogu
base_directory = 'content'
verify_data_structure(base_directory)
