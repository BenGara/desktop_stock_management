"""Service pour gérer la logique métier des catégories de matériel."""

from models.categorie_model import CategorieModel

class CategorieService:

    @staticmethod
    def obtenir_toutes_categories():
        """Récupère toutes les catégories et formate les textes pour l'UI."""
        categories_brutes = CategorieModel.get_all_categories()
        categories_nettoyees = []

        for cat in categories_brutes:
            cat_id, nom, desc = cat
            nom_affichage = nom.capitalize() if nom else ""
            desc_propre = desc if desc is not None else ""
            
            categories_nettoyees.append((cat_id, nom_affichage, desc_propre))

        return categories_nettoyees

    @staticmethod
    def ajouter_categorie(nom, description):
        """Valide les saisies et demande la création d'une catégorie."""
        nom_clean = nom.strip()
        desc_clean = description.strip()

        # 1. Validation du champ obligatoire
        if not nom_clean:
            raise ValueError("Le nom de la catégorie est obligatoire.")

        # 2. Règle de gestion : Unicité du nom de la catégorie
        if CategorieModel.is_category_name_exists(nom_clean):
            raise ValueError(f"La catégorie '{nom_clean}' existe déjà.")

        CategorieModel.create_category(nom_clean, desc_clean)

    @staticmethod
    def modifier_categorie(category_id, nom, description):
        """Valide les modifications et demande la mise à jour d'une catégorie."""
        nom_clean = nom.strip()
        desc_clean = description.strip()

        if not category_id:
            raise ValueError("Aucune catégorie sélectionnée pour la modification.")
        if not nom_clean:
            raise ValueError("Le nom de la catégorie ne peut pas être vide.")

        # Vérification du doublon en excluant la catégorie en cours de modification
        if CategorieModel.is_category_name_exists(nom_clean, exclude_id=category_id):
            raise ValueError(f"Une autre catégorie porte déjà le nom '{nom_clean}'.")

        CategorieModel.update_category(category_id, nom_clean, desc_clean)

    @staticmethod
    def supprimer_categorie(category_id):
        """Demande la suppression définitive d'une catégorie au modèle."""
        if not category_id:
            raise ValueError("Aucune catégorie sélectionnée pour la suppression.")
        CategorieModel.delete_category(category_id)