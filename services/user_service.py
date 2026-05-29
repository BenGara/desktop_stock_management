"""Service pour la gestion des utilisateurs."""

from models.user_model import UserModel
from services.auth_service import AuthService

class UserService:
    
    @staticmethod
    def obtenir_tous_utilisateurs():
        """Récupère tous les utilisateurs avec le nom de leur rôle nettoyé."""
        utilisateurs_bruts = UserModel.get_all_users()
        utilisateurs_nettoyes = []

        for user in utilisateurs_bruts:
            user_id, prenom, nom, email, role_nom = user
            utilisateurs_nettoyes.append((user_id, prenom, nom, email, role_nom))

        return utilisateurs_nettoyes
        
    @staticmethod
    def obtenir_noms_roles():
        """Récupère les rôles disponibles en BDD et les rend propres pour le menu déroulant."""
        roles_bruts = UserModel.get_all_role_names()
        return [role.capitalize() for role in roles_bruts]

    # Ajouter un nouvel utilisateur avec un formulaire complet dans un popup.
    @staticmethod
    def inscrire_utilisateur(prenom, nom, email, mdp, role_texte):
        """Valide la saisie, applique les règles métier et enregistre en BDD."""
        prenom_clean = prenom.strip()
        nom_clean = nom.strip()
        email_clean = email.strip()
        mdp_clean = mdp.strip()

        if not prenom_clean or not nom_clean or not email_clean or not mdp_clean:
            raise ValueError("Tous les champs doivent être remplis.")

        role_bdd = role_texte.upper()
        if role_bdd == "ADMIN":
            role_id = 1
        elif role_bdd == "MANAGER" or role_bdd == "GESTIONNAIRE DE STOCK":
            role_id = 2
        else:
            role_id = 3  # 'EMPLOYEE'

        mdp_hache = AuthService.hash_password(mdp_clean)
        UserModel.create_user(prenom_clean, nom_clean, email_clean, mdp_hache, role_id)

    # Modifier un utilisateur existant avec un formulaire pré-rempli dans un popup.
    @staticmethod
    def modifier_utilisateur(user_id, prenom, nom, email, role_texte):
        """Valide les modifications et met à jour l'utilisateur en BDD."""
        prenom_clean = prenom.strip()
        nom_clean = nom.strip()
        email_clean = email.strip()

        if not user_id:
            raise ValueError("Aucun utilisateur sélectionné.")
        if not prenom_clean or not nom_clean or not email_clean:
            raise ValueError("Le prénom, le nom et l'email ne peuvent pas être vides.")

        role_id = UserService._convertir_role_en_id(role_texte)
        UserModel.update_user(user_id, prenom_clean, nom_clean, email_clean, role_id)

    # Supprimer un utilisateur existant après confirmation.
    @staticmethod
    def supprimer_utilisateur(user_id):
        """Demande la suppression d'un utilisateur au modèle."""
        if not user_id:
            raise ValueError("Aucun utilisateur sélectionné pour la suppression.")
        UserModel.delete_user(user_id)

    # Méthode utilitaire pour convertir le texte du rôle en ID de rôle pour la BDD.
    @staticmethod
    def _convertir_role_en_id(role_texte):
        """Méthode utilitaire interne pour faire la correspondance Rôle -> ID."""
        role_bdd = role_texte.upper()
        if role_bdd == "ADMIN":
            return 1
        elif role_bdd == "MANAGER" or role_bdd == "GESTIONNAIRE DE STOCK":
            return 2
        else:
            return 3  # 'EMPLOYEE'