# Aplikacja do Podsumowywania Plików PDF z AI

## 1. Opis Projektu 

Aplikacja jest rozwiązaniem typu **full-stack**, które umożliwia użytkownikom przesyłanie dokumentów w formacie PDF w celu wygenerowania ich automatycznego podsumowania za pomocą modelu sztucznej inteligencji **Google Gemini**. Projekt został zrealizowany jako demonstracja umiejętności integracji technologii frontendowych, backendowych oraz zewnętrznych usług API.

### Główne Funkcjonalności:
* Interfejs użytkownika do przesyłania plików z obsługą "przeciągnij i upuść" (Drag & Drop).
* Walidacja po stronie klienta (przycisk jest nieaktywny do momentu załączenia pliku).
* Skuteczna walidacja typu, rozmiaru i zawartości pliku po stronie serwera.
* Komunikacja z modelem AI w celu wygenerowania podsumowania.
* Dynamiczne wyświetlenie wyniku wraz z opcją kopiowania i czyszczenia.

---

## 2. Stos Technologiczny 

* **Frontend:**
    * **Języki:** HTML, CSS, JavaScript 
    * **Frameworki:** Brak. Aplikacja została napisana w czystym **Vanilla JS**, aby zapewnić lekkość i pełną kontrolę nad kodem.
    * **Narzędzia:** Google Fonts (dla czcionki Poppins i ikon Material Symbols).

* **Backend:**
    * **Język:** Python 
    * **Framework:** Flask
    * **Kluczowe Pakiety:**
        * `Flask`: Rdzeń aplikacji serwerowej i obsługa API.
        * `requests`: Do wysyłania zapytań HTTP do zewnętrznego API Gemini.
        * `pypdf`: Do odczytywania i ekstrakcji tekstu z plików PDF.
        * `python-dotenv`: Do zarządzania zmiennymi środowiskowymi (bezpieczne przechowywanie klucza API).
        * `flask-cors`: Do obsługi zapytań Cross-Origin Resource Sharing.

* **Model AI:**
    * **Usługa:** Google Gemini (model `gemini-2.5-flash`)
    * **Interfejs:** REST API


## 3. Architektura i Komunikacja 

Aplikacja została zbudowana w architekturze **klient-serwer** z wyraźnym podziałem na warstwę frontendową (przeglądarka) i backendową (serwer Flask).

Komunikacja odbywa się za pośrednictwem **asynchronicznych zapytań HTTP** do punktu końcowego API (`/api/summarize`). Proces ten przebiega następująco:

1.  **Akcja Użytkownika:** Użytkownik przesyła plik PDF.
2.  **Wysłanie Danych:** Frontend, używając **Fetch API**, wysyła żądanie `POST` z plikiem spakowanym w `FormData`.
3.  **Walidacja i Przetwarzanie:** Serwer Flask odbiera żądanie, waliduje plik, a następnie ekstrahuje z niego tekst.
4.  **Komunikacja z AI:** Backend wysyła zapytanie **REST API** do serwerów Google, przesyłając tekst z instrukcją (promptem).
5.  **Odpowiedź:** Serwer Flask odbiera wygenerowane podsumowanie, formatuje je jako obiekt **JSON** i odsyła do frontendu.
6.  **Prezentacja Wyniku:** Frontend odbiera odpowiedź JSON i dynamicznie renderuje podsumowanie na stronie.

---

## 4. Instrukcja Uruchomienia Lokalnego 

### Wymagania Wstępne
* **Python** (wersja 3.8 lub nowsza)
* **Git**
* **VS Code** z rozszerzeniem **Live Server** (rekomendowane).

### Krok 1: Konfiguracja Backendu
1.  Sklonuj repozytorium:
    ```bash
    git clone https://github.com/Julekoski/Serty-Zadanie.git
    cd Serty-Zadanie
    ```
2.  Stwórz i aktywuj wirtualne środowisko:
    ```bash
    # Stworzenie środowiska
    python -m venv venv

    Jeśli środowisko się nie uruchamia: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

    # Aktywacja na Windows
    .\venv\Scripts\activate

    # Aktywacja na macOS/Linux
    source venv/bin/activate
    ```
3.  Zainstaluj wszystkie zależności z pliku `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
4.  Skonfiguruj klucz API:
    * Stwórz plik o nazwie `.env` w głównym folderze.
    * Dodaj do niego swój klucz API w formacie: `GEMINI_API_KEY="TWOJ_KLUCZ_API"`
5.  Uruchom serwer:
    ```bash
    python app.py
    ```
    Serwer będzie działał pod adresem `http://127.0.0.1:5000`.

### Krok 2: Uruchomienie Frontendu
1.  Otwórz folder projektu w VS Code.
2.  Kliknij prawym przyciskiem myszy na plik `index.html`.
3.  Wybierz opcję **"Open with Live Server"**.


Aplikacja otworzy się w przeglądarce i będzie w pełni funkcjonalna.
