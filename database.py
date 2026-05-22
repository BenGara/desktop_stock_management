"""Database connection module for the Stock Management application."""

import sqlite3

DATABASE_NAME = "database/stock.db"


def get_connection():
    """Create and return a new SQLite connection with row factory enabled."""
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection
