# semantive-project

Zbudowanie projektu:

```
docker-compose build
```

Uruchomienie projektu:
```
docker-compose up -d
```
Przykładowe zapytanie:
```
curl --header "Content-Type: application/json;only=both" --request POST --data '{"url": "https://www.python.org/", "name": "test"}' http://localhost:5000/extractor/
```


  
---

# Podsumowanie

Aplikacja napisana we Flasku. Wykorzystane zostały SQLAlchemy, Celery oraz Redis. Postanowiłem stworzyć API w oparciu o Content-Type. Zabieg moim zdaniem uprościł endpointy w aplikacji. Oprócz adresu url użytkownik powinien podawać name, aby od strony cms rozpoznawać obiekty po nazwie (w założeniu że api służyłoby w cms, który będzie miał wylistowane obiekty). Napisałem dwa adaptery obsługujące pobieranie obrazków - docelowo użyłbym clouda do ich przechowywania. Starałem się wszystko pisać w TDD.

Do zmiany:
- sporo logiki znajduje się w handlerach - należałoby wydzielić kod do klas 
- refactor testów - trzymanie jednej metodyki (When-Given-Then)
- wydzielenie settingsów oraz zmiennych globalnych do jednego pliku np. yml i pobieranie wszystkiego ze zmiennych systemowych
- jeśli miałby zostać lokalny adapter należałoby dodać dodatkowy volume

Co poszło nie po mojej myśli:
- inicjalizacja obiektu celery + sposób przekazywania do niego konfiguracji 
- zapisywanie plików lokalnie zamiast w chmurze
- brak skryptu tworzącego bazę danych z migracji 
- brak skryptu do uruchamiania aplikacji np. make start
