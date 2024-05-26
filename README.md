# Projekt 5: Watchlist

## Opis projektu:
Aplikacja do zarządzania kolekcją filmów umożliwi użytkownikom organizację, przeglądanie i śledzenie ich kolekcji filmów. Użytkownicy będą mogli dodawać, edytować, oceniać oraz wyszukiwać filmy.

### Funkcje aplikacji:
- Dodawanie nowych filmów do swojej kolekcji poprzez wprowadzenie tytułu, reżysera, roku produkcji, gatunku, statusu, oceny oraz innych szczegółowych informacji.
- Edytowanie informacje o filmie, takie jak tytuł, reżyser, gatunek, ocena, opis
- Ocenianie filmów oraz komentowanie.
- Dodaj funkcję wyszukiwania filmów w kolekcji na podstawie różnych kryteriów, takich jak tytuł, gatunek, reżyser, rok produkcji itp.
- Przeglądanie swojej kolekcji filmów.
- Dodaj możliwość eksportu danych o kolekcji filmów do pliku tekstowego.
- Dodaj funkcję, która będzie przechowywać historię obejrzanych filmów, aby użytkownicy mogli śledzić, które filmy już widzieli i kiedy je oglądali.
- Wprowadź funkcję generowania statystyk dotyczących kolekcji filmów, takich jak liczba filmów w poszczególnych gatunkach, średnia ocena filmów, najczęściej oceniane filmy itp.
- Uwzględnij obsługę błędów, jak usuwanie nieistniejącej pozycji lub dodawanie wyniku po za skale.
- Dodaj prosty interface.

## Struktura projektu:
Klasa Film: Reprezentuje pojedynczy film w kolekcji. Zawiera atrybuty takie jak tytuł, reżyser, gatunek, status, ocena oraz metody do zarządzania danymi filmu.

Klasa CollectionManager: Zarządza kolekcją filmów. Zawiera metody do dodawania, usuwania, edytowania, oceniania filmów oraz wyszukiwania filmów w kolekcji.

Klasy wyjątków: Odpowiadają za obsługę sytuacji błędnych, np. ScaleError, MovieNotFoundError
