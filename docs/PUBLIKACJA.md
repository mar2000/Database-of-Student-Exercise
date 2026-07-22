# Budowanie, testowanie i publikacja

## Instalacja zależności

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Budowanie strony

```bash
python3 build.py
```

Generator tworzy lub aktualizuje katalog `build/`.

## Lokalny podgląd

```bash
cd build
python3 -m http.server 8001
```

Otwórz:

```text
http://127.0.0.1:8001/
```

Po zmianach w JavaScript lub CSS warto wykonać twarde odświeżenie przeglądarki (`Ctrl+Shift+R`).

## Testy

Z katalogu głównego projektu:

```bash
pytest -q
```

Testy sprawdzają m.in. poprawność budowania, paginację i wybrane reguły renderowania.

## Publikacja na serwerze studenckim

Na serwer przesyłaj wyłącznie zawartość `build/`.

Przykład docelowej struktury:

```text
public_html/
├── index.html
├── assets/
├── data/
├── kierunki/
├── przedmioty/
└── zestaw/
```

Nie publikuj katalogów źródłowych takich jak `content/`, `generator/`, `tests/` ani pliku `build.py`.

## Co jest źródłem, a co wynikiem

Źródła projektu:

- `content/`
- `generator/`
- `site/`
- `tests/`
- `build.py`
- `requirements.txt`

Pliki pomocnicze:

- `docs/`

Wynik generowania:

- `build/`

`build/` można zawsze odtworzyć z plików źródłowych.
