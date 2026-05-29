from models.breakdown_model import BreakdownModel
from models.material_model import MaterialModel

class BreakdownService:

    @staticmethod
    def obtenir_tous_materiels_combobox():
        """Retourne la liste complète des matériels sous forme de dict pour le menu déroulant."""
        mats = MaterialModel.get_all_materials()
        return {f"{m[1]} (S/N: {m[2]})": m[0] for m in mats}

    @staticmethod
    def obtenir_pannes_formatees():
        """Formate les pannes pour un affichage propre dans le Treeview."""
        pannes = BreakdownModel.get_all_breakdowns()
        liste_formatee = []
        for p in pannes:
            p_id, mat_nom, serial, desc, statut, date_p, mat_id = p
            statut_aff = statut.replace('_', ' ').capitalize()
            liste_formatee.append((p_id, f"{mat_nom} ({serial})", desc, statut_aff, date_p, mat_id))
        return liste_formatee

    @staticmethod
    def déclarer_panne(nom_affichage_mat, description):
        if not nom_affichage_mat or not description.strip():
            raise ValueError("Veuillez sélectionner un matériel et décrire le problème.")
            
        dict_mats = BreakdownService.obtenir_tous_materiels_combobox()
        mat_id = dict_mats.get(nom_affichage_mat)
        if not mat_id:
            raise ValueError("Matériel invalide.")
            
        BreakdownModel.declare_breakdown(mat_id, description.strip())

    @staticmethod
    def changer_statut_panne(breakdown_id, material_id, statut_affichage):
        mapping = {
            "En cours de réparation": "EN_COURS",
            "Réparé (Retour au stock)": "REPARE",
            "Mis hors service": "MIS_HORS_SERVICE"
        }
        statut_bdd = mapping.get(statut_affichage)
        if not statut_bdd:
            raise ValueError("Statut sélectionné invalide.")
            
        BreakdownModel.update_breakdown_status(breakdown_id, material_id, statut_bdd)