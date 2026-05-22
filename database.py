"""Module de connexion à la base de données."""

import sqlite3

DATABASE_NAME = "database/stock.db"


def get_connection():
    """Crée et renvoye une nouvelle connexion SQLite avec la fonction
    "row factory"" activée.
    """
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection
