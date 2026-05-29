from models.material_model import MaterialModel
from models.user_model import UserModel
from models.assignment_model import AssignmentModel

class AssignmentService:
    
    @staticmethod
    def obtenir_materiels_disponibles():
        """Renvoie un dictionnaire { 'Nom (S/N: 123) [Dispo: 5]': id } pour les matériels en stock."""
        materiels_bruts = MaterialModel.get_all_materials()
        # On filtre pour ne garder que ceux qui ont une quantité supérieure à 0
        return {
            f"{mat[1]} (S/N: {mat[2]}) [Dispo: {mat[4]}]": mat[0]
            for mat in materiels_bruts if mat[4] > 0
        }

    @staticmethod
    def obtenir_employes_actifs():
        """
        Renvoie un dictionnaire { 'Nom Prénom': id } des employés.
        Ajuste selon la structure de ton user_model.py.
        """
        # Supposons que user_model possède une méthode get_all_users() 
        # qui renvoie des tuples (id, nom, prenom, ...)
        users_bruts = UserModel.get_all_users()
        return {
            f"{user[1].upper()} {user[2].capitalize()}": user[0]
            for user in users_bruts
        }

    @staticmethod
    def affecter_materiel(nom_affichage_mat, nom_affichage_emp):
        """Valide les sélections et applique l'affectation."""
        if not nom_affichage_mat or not nom_affichage_emp:
            raise ValueError("Veuillez sélectionner un matériel et un employé.")

        # Récupération des IDs via les dictionnaires de correspondance
        dict_mats = AssignmentService.obtenir_materiels_disponibles()
        dict_emps = AssignmentService.obtenir_employes_actifs()

        mat_id = dict_mats.get(nom_affichage_mat)
        user_id = dict_emps.get(nom_affichage_emp)

        if not mat_id:
            raise ValueError("Le matériel sélectionné est invalide ou épuisé.")
        if not user_id:
            raise ValueError("L'employé sélectionné est invalide.")

        # Lancement de l'affectation en BDD
        AssignmentModel.create_assignment(mat_id, user_id)