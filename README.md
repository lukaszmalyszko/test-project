

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


  
--
