# Gestion de Stock Informatique Desktop
## Technologies
* Python
* Tkinter
* SQLite

## Lancement
### Création de la base de données
Il y a déjà une base de données dans ce dépôt, mais s'il y a besoin de la regénérer :
```
sqlite3 database/stock.db < schema.sql
sqlite3 database/stock.db < seed.sql
```

### Lancement
```
python main.py
```

### Tests
```
python -m unittest discover tests
```
