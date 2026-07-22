# Baza zadań studenckich

Statyczna baza zadań i materiałów dydaktycznych dla studentów. Strona jest generowana lokalnie z plików źródłowych, a na serwer publikuje się wyłącznie gotową zawartość katalogu `build/`.

## Szybki start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 build.py
cd build
python3 -m http.server 8001
```

Następnie otwórz `http://127.0.0.1:8001/`.

## Najważniejsze katalogi

- `content/` — dane źródłowe: kierunki, przedmioty, zadania i materiały PDF;
- `generator/` — generator statycznej strony;
- `site/` — wspólne pliki CSS i JavaScript kopiowane do wyniku;
- `tests/` — testy generatora i interfejsu;
- `docs/` — dokumentacja i szablony pomocnicze;
- `build/` — wynik generowania, gotowy do publikacji.

## Publikacja

Po zmianie treści uruchom:

```bash
python3 build.py
```

Na serwer studencki przesyłaj **zawartość katalogu `build/`**, a nie cały projekt.

## Dokumentacja

- [Architektura projektu](docs/ARCHITEKTURA.md)
- [Dodawanie zadań i materiałów](docs/DODAWANIE_TRESCI.md)
- [Budowanie, testowanie i publikacja](docs/PUBLIKACJA.md)
- [Szablony plików](docs/templates/)

W katalogu głównym pozostawiono tylko ten `README.md`; pozostałe pomocnicze pliki Markdown zostały przeniesione do `docs/`, ponieważ nie są potrzebne do kompilacji strony.
