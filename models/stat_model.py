"""Modèle de gestion de la récupération des données pour les statistiques du stock."""

import database
from multiprocessing import connection

class StatModel:
    """Fournit des méthodes pour récupérer les données statistiques du stock."""

    @staticmethod
    def get_stock_stats():
        """Renvoie les statistiques globales du stock."""
        connection = database.get_connection()
        connection.row_factory = None 
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) AS total_materials, SUM(quantity) AS total_quantity FROM materials")
        stats = cursor.fetchone()
            
        return stats
    
    @staticmethod
    def get_materiel_affecte_stats():
        """Renvoie les statistiques du matériels affectés."""
        connection = database.get_connection()
        connection.row_factory = None 
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(id) AS material_affecte_count FROM assignments WHERE active = 1")
        stats = cursor.fetchone()

        return stats
    
    @staticmethod
    def get_materiel_panne_stats():
        """Renvoie les statistiques du matériels en panne."""
        connection = database.get_connection()
        connection.row_factory = None 
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) AS material_panne_count FROM breakdowns")
        stats = cursor.fetchone()

        return stats
    
    
