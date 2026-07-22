# Dodawanie treści

## Dodawanie zadania

1. Wejdź do katalogu danego kursu, np.:

```text
content/courses/uw-matematyka-rp1/zadania/
```

2. Dodaj kolejny numerowany plik, np. `0001.md`, `0002.md`, itd.
3. Zachowaj schemat metadanych i sekcji.
4. Używaj wyłącznie `topics` zdefiniowanych w `course.yaml` danego kursu.
5. Uruchom `python3 build.py`.

Szablony znajdują się w `docs/templates/`.

### Minimalna struktura zadania

```yaml
---
id: uw-matematyka-rp1-0001
number: 1
title: Tytuł zadania

topics:
  - model-klasyczny-kombinatoryka

difficulty: latwe

source:
  type: Ćwiczenia
  name: ...
  collection: ...
  chapter: ...
  original_problem_number: ...
  pages: "..."

tags: []
published: true
verified: false
---
```

Następnie:

```text
## Treść
## Wskazówka
## Odpowiedź
## Rozwiązanie
```

### Zasady formatowania

- zwykłe akapity treści zapisuj jako `<p>...</p>`;
- wzory liniowe zapisuj jako `\( ... \)`;
- wzory blokowe zapisuj jako `\[ ... \]`;
- polecenia LaTeX muszą zawierać literalne pojedyncze backslashe, np. `\frac`, `\binom`, `\sum`;
- nie używaj znaków sterujących w miejscu poleceń LaTeX.

### `verified`

- `true` — gdy istnieje pełne i poprawne rozwiązanie lub odpowiedź źródłowa;
- `false` — gdy jest tylko polecenie, rozwiązanie jest niepełne/błędne albo zostało samodzielnie dopisane lub istotnie poprawione.

W zadaniach typu „wykaż”, „udowodnij”, „uzasadnij” sekcja `## Odpowiedź` powinna pozostać pusta, jeśli nie istnieje niezależna, jednoznaczna odpowiedź końcowa.

## Dodawanie materiału dydaktycznego

Dla kursu utwórz katalog:

```text
content/courses/<id-kursu>/materialy/<id-materialu>/
```

W nim umieść:

```text
material.yaml
plik.pdf
```

Przykład:

```yaml
id: uw-matematyka-rp1-wzory
title: Wzory z Rachunku Prawdopodobieństwa I
type: inne
description: >
  Zestaw najważniejszych wzorów.
author: Marysia Nazarczuk
topics:
  - prawdopodobienstwo-warunkowe-bayes
file: wzory.pdf
published: true
featured: false
order: 10
```

Nazwa w polu `file` musi dokładnie odpowiadać nazwie rzeczywistego pliku.

## Dodawanie nowego kursu

1. Utwórz katalog `content/courses/<id-kursu>/`.
2. Dodaj `course.yaml`.
3. Utwórz `zadania/` i opcjonalnie `materialy/`.
4. Upewnij się, że `field` odpowiada istniejącemu kierunkowi z `content/fields/`.
5. Zbuduj projekt i uruchom testy.
