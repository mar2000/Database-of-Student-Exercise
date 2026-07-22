# Architektura projektu

## Cel

Projekt generuje statyczną stronę z bazą zadań studenckich. Użytkownik przechodzi ścieżką:

`strona główna → kierunek → przedmiot → zadania / materiały dydaktyczne`.

Strona nie wymaga logowania, panelu administracyjnego ani działającego backendu na serwerze docelowym.

## Przepływ danych

1. Dane źródłowe znajdują się w `content/`.
2. `build.py` uruchamia generator z `generator/builder.py`.
3. Generator waliduje konfigurację kursów, zadania i materiały.
4. Pliki z `site/` są kopiowane do katalogu wynikowego.
5. Powstaje katalog `build/` zawierający gotową stronę statyczną.

## Struktura katalogów

```text
.
├── build.py
├── requirements.txt
├── content/
│   ├── fields/
│   └── courses/
├── generator/
├── site/
├── tests/
├── docs/
└── build/
```

### `content/fields/`

Każdy plik YAML opisuje kierunek studiów, np. `matematyka.yaml`.

### `content/courses/`

Każdy kurs ma własny katalog o unikalnym identyfikatorze, np.:

```text
content/courses/uw-matematyka-am2/
content/courses/uw-matematyka-rp1/
```

Typowy katalog kursu zawiera:

```text
course.yaml
zadania/
materialy/
```

Może też zawierać pomocnicze pliki konfiguracyjne, np. `dozwolone_dzialy.yaml` lub mapy rozdziałów.

### `zadania/`

Każde zadanie jest osobnym numerowanym plikiem `.md` z metadanymi YAML i sekcjami treści. Numeracja jest ciągła w obrębie danego przedmiotu.

### `materialy/`

Każdy materiał dydaktyczny ma osobny podkatalog zawierający `material.yaml` oraz właściwy plik, najczęściej PDF.

### `generator/`

Zawiera kod odpowiedzialny za:

- odczyt konfiguracji YAML i plików `.md`;
- walidację identyfikatorów `topics`;
- budowanie katalogu danych;
- generowanie stron HTML;
- kopiowanie zasobów i materiałów.

### `site/`

Zawiera wspólne zasoby interfejsu:

- CSS;
- JavaScript listy zadań i filtrów;
- obsługę zestawu zadań;
- paginację;
- eksport wybranych zadań do PDF.

### `build/`

Katalog wynikowy. Może zostać usunięty i odtworzony przez `python3 build.py`. To jego zawartość publikuje się na serwerze.

## Model kursu

`course.yaml` określa m.in.:

- identyfikator i nazwę przedmiotu;
- kierunek;
- listę dozwolonych działów (`topics`);
- kolejność i widoczność kursu.

Identyfikatory działów są technicznymi kluczami. Wartość wpisana w `topics` zadania musi dokładnie odpowiadać `id` działu z `course.yaml`.

## Model zadania

Zadanie składa się z front matter YAML i czterech sekcji:

```text
## Treść
## Wskazówka
## Odpowiedź
## Rozwiązanie
```

Generator wykorzystuje metadane do filtrowania według działu, trudności i pochodzenia.

## Model materiału

Materiał dydaktyczny jest definiowany przez `material.yaml`. Metadane wskazują tytuł, typ, przypisane działy, plik i widoczność.

## Charakter statyczny

Po zbudowaniu strona działa jako zestaw statycznych plików HTML/CSS/JS/JSON/PDF. Dzięki temu na serwerze nie ma kont administratorów ani aplikacyjnej bazy danych, którą trzeba utrzymywać.
