# Przygotowanie zadań z Analizy Matematycznej II

## Główne źródło

Jedynym głównym źródłem zadań jest połączony dokument:

`Analiza Matematyczna II – ćwiczenia`

Plik znajduje się w:

`content/courses/uw-matematyka-am2/materialy/analiza-matematyczna-ii-cwiczenia/Analiza_Matematyczna_II.pdf`

Dokument ma 29 rozdziałów. Mapa rozdziałów do działów strony znajduje się w:

`content/courses/uw-matematyka-am2/mapa_rozdzialow.yaml`

## Dozwolone działy

Jedynym źródłem prawdy dla identyfikatorów `topics` jest:

`content/courses/uw-matematyka-am2/dozwolone_dzialy.yaml`

Te same identyfikatory znajdują się w `course.yaml`. Nie należy tworzyć nowych wariantów nazw działów w plikach zadań.

## Numerowanie plików

Wszystkie zadania trafiają kolejno do:

`content/courses/uw-matematyka-am2/zadania/`

Nazwy: `0001.md`, `0002.md`, ...

## Metadane źródła

Dla nowych plików używaj:

- `collection: Analiza Matematyczna II`
- `chapter`: numer rozdziału w połączonym PDF-ie
- `original_problem_number`: numer zadania w danym rozdziale
- `pages`: strony w połączonym PDF-ie

Nie używaj już oznaczeń `Analiza Matematyczna II.1`, `Analiza Matematyczna II.2` ani pola `exercise_set`.

## Budowanie

Po dodaniu plików uruchom:

`python3 build.py`

Generator sprawdzi m.in., czy wszystkie `topics` istnieją w `course.yaml`.
