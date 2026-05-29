"""Service pour la gestion du matériel."""

from models.material_model import MaterialModel

class MaterielService:
    @staticmethod
    def obtenir_tous_materiels():
        """Récupère tous les matériels et formate les statuts et dates pour l'UI."""
        materiels_bruts = MaterialModel.get_all_materials()
        materiels_nettoyes = []

        for mat in materiels_bruts:
            mat_id, nom, num_serie, cat_nom, quantite, statut, date_achat = mat
            
            # Formatage de confort pour l'affichage (ex: 'EN_STOCK' -> 'En stock')
            statut_affichage = statut.replace('_', ' ').capitalize() if statut else "Inconnu"
            cat_affichage = cat_nom.capitalize() if cat_nom else "Sans catégorie"
            date_affichage = date_achat if date_achat else "Non renseignée"

            materiels_nettoyes.append((mat_id, nom, num_serie, cat_affichage, quantite, statut_affichage, date_affichage))

        return materiels_nettoyes
    
    @staticmethod
    def obtenir_categories_formulaire():
        """Récupère les catégories sous forme de dictionnaire {NomCapitalise: ID}."""
        categories_brutes = MaterialModel.get_all_categories_names_with_ids()
        return {cat_name.capitalize(): cat_id for cat_id, cat_name in categories_brutes}

    @staticmethod
    def ajouter_materiel(nom, num_serie, nom_categorie, quantite_str):
        """Valide les données de l'UI et crée le matériel sans exiger de date ni de statut."""
        nom_clean = nom.strip()
        num_serie_clean = num_serie.strip()

        if not nom_clean or not num_serie_clean or not nom_categorie:
            raise ValueError("Le nom, le numéro de série et la catégorie ne peuvent pas être vides.")

        try:
            quantite = int(quantite_str)
            if quantite < 0:
                raise ValueError()
        except ValueError:
            raise ValueError("La quantité doit être un nombre entier positif.")

        # Vérification de l'unicité du numéro de série
        if MaterielService.is_serial_number_exists(num_serie_clean):
            raise ValueError(f"Le numéro de série '{num_serie_clean}' est déjà utilisé.")

        # 1. Récupération de l'ID de la catégorie
        dict_cats = MaterielService.obtenir_categories_formulaire()
        cat_id = dict_cats.get(nom_categorie)
        if not cat_id:
            raise ValueError("La catégorie sélectionnée est invalide.")

        # 2. MODIFICATION ICI : On passe uniquement les 4 paramètres attendus par le modèle
        MaterialModel.create_material(nom_clean, num_serie_clean, cat_id, quantite)
        
    @staticmethod
    def modifier_materiel(material_id, nom, num_serie, nom_categorie, quantite_str, statut_affichage, date_achat):
        """Valide et met à jour un matériel existant."""
        nom_clean = nom.strip()
        num_serie_clean = num_serie.strip()
        date_clean = date_achat.strip()

        if not material_id:
            raise ValueError("Aucun matériel sélectionné.")
        if not nom_clean or not num_serie_clean or not nom_categorie:
            raise ValueError("Le nom, le numéro de série et la catégorie ne peuvent pas être vides.")

        try:
            quantite = int(quantite_str)
            if quantite < 0:
                raise ValueError()
        except ValueError:
            raise ValueError("La quantité doit être un nombre entier positif.")

        # Vérification du numéro de série en excluant le matériel en cours de modification
        if MaterialModel.is_serial_number_exists(num_serie_clean, exclude_id=material_id):
            raise ValueError(f"Le numéro de série '{num_serie_clean}' est déjà utilisé par un autre équipement.")

        dict_cats = MaterielService.obtenir_categories_formulaire()
        cat_id = dict_cats.get(nom_categorie)
        if not cat_id:
            raise ValueError("La catégorie sélectionnée est invalide.")

        statut_bdd = statut_affichage.strip().upper().replace(' ', '_')

        MaterialModel.update_material_full(material_id, nom_clean, num_serie_clean, cat_id, quantite, statut_bdd, date_clean)

    @staticmethod
    def supprimer_materiel(material_id):
        """Vérifie et transmet la demande de suppression définitive."""
        if not material_id:
            raise ValueError("Aucun matériel sélectionné pour la suppression.")
        MaterialModel.delete_material(material_id)