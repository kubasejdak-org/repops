# repops requirements

## Functional requirements

1. App should allow creating pull requests (PR) on the following platforms:
    1. GitHub,
    2. Azure DevOps,
    3. GitLab.
2. App should be independent from any programming language wherever possible, but should provide modules for creating a
   language-specific behavior.

## Non-functional requirements

1. Project should be written in Python.
2. Project should use `uv` workflow for managing build system and dependencies.
3. Project should use `ruff` for checking for formatting and linting issues.
















3. Aplikacja powinna mieć architekturę modułową, opartą o pluginy lub zestaw komend (akcji) które można w prosty sposób rozszerzać.
4. Procesy modyfikowacji repozytorów powinny być oddzielone od procesu tworzeniach PR ze zmianami.
5. Powinna być możliwość zdefiniowania kolejki operacji na danym repozytium lub ich liście, włączając operację tworzenia PR.
6. W przypadku gdy jest kilka operacji modyfikacji po sobie, oznacza to że każda z tych operacji jest osobnym commitem w repozytorium, ale są częścią tego samego potencjalnego PR.
7. Aplikacja powinna ładować plik YAML (domyślnie `repos.yml`) z listą repozytoriów do zarządzania.
8. Aplikacja powinna mieć interfejs CLI do modyfikowania pliku z listą repozytoriów:
    1. dodawanie i usuwanie repozytorium
    2. aktualizacja ścieżki na dysku, URL lub nazwy gałęzi głównej
9. Aplikacja powinna wspierać następujące operacje:
    1. Ogólne
        1. git
            1. klonowanie repozytorium
            2. pullowanie zmian
            3. tworzenie pull requestów (PR)
            4. tworzenie, usuwanie i zmiana gałęzi
            5. tworzenie tagów
            6. pobranie i zapisanie aktualnych rewizji wszystkich zarządzanych repozytoriów
        2. files
            1. kopiowanie wskazanego pliku do wybranego repozytorium (jako referencja może być użyte inne repozytorium)
            2. aplikowanie wskazanego patcha do wybranego repozytorium
            3. wykonanie operacji „find”
            4. wykonanie operacji „find and replace”
        3. script
            1. wykonanie wskazanego skryptu lub wyrażenia powłoki na danym repozytorium
    2. C++:
        1. cmake
            1. listowanie zależności na podstawie plików `Find*.cmake`
            2. tworzenie grafu zależności pomiędzy repozytoriami (w celu ustalenia kolejności aplikowania zmian)
            3. update zależności do wersji HEAD wg grafu zależności

### WYMAGANIA NIEFUNKCJONALNE

---

4. Project powinien mieć zrobione testy jednostkowe przy pomocy `pytest` oraz liczone code coverage.
