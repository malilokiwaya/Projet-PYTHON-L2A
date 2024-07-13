1
import json
import csv
from datetime import datetime

class Utilisateur:
    def __init__(self, nom, email):
        self.nom = nom
        self.email = email
        self.livres_empruntes = []
        self.historique_emprunts = []

    def __str__(self):
        return f"{self.nom} ({self.email})"

    def to_dict(self):
        return {
            "nom": self.nom,
            "email": self.email,
            "livres_empruntes": self.livres_empruntes,
            "historique_emprunts": self.historique_emprunts
        }

    @classmethod
    def from_dict(cls, data):
        utilisateur = cls(data["nom"], data["email"])
        utilisateur.livres_empruntes = data["livres_empruntes"]
        utilisateur.historique_emprunts = data["historique_emprunts"]
        return utilisateur

class GestionUtilisateurs:
    def __init__(self, fichier_json):
        self.fichier_json = fichier_json
        self.utilisateurs = self.charger_utilisateurs()

    def ajouter_utilisateur(self):
        nom = input("Entrez le nom de l'utilisateur : ")
        email = input("Entrez l'email de l'utilisateur : ")
        self.utilisateurs.append(Utilisateur(nom, email))
        self.sauvegarder_utilisateurs()
        print(f"Utilisateur {nom} ajouté avec succès.")

    def supprimer_utilisateur(self):
        email = input("Entrez l'email de l'utilisateur à supprimer : ")
        self.utilisateurs = [u for u in self.utilisateurs if u.email != email]
        self.sauvegarder_utilisateurs()
        print(f"Utilisateur avec l'email {email} supprimé avec succès.")

    def lister_utilisateurs(self):
        for utilisateur in self.utilisateurs:
            print(utilisateur)

    def modifier_utilisateur(self):
        email = input("Entrez l'email de l'utilisateur à modifier : ")
        for utilisateur in self.utilisateurs:
            if utilisateur.email == email:
                nouveau_nom = input("Entrez le nouveau nom (laissez vide pour ne pas changer) : ")
                nouveau_email = input("Entrez le nouvel email (laissez vide pour ne pas changer) : ")
                if nouveau_nom:
                    utilisateur.nom = nouveau_nom
                if nouveau_email:
                    utilisateur.email = nouveau_email
                self.sauvegarder_utilisateurs()
                print(f"Informations de l'utilisateur {email} modifiées avec succès.")
                return
        print(f"Utilisateur avec l'email {email} non trouvé.")

    def afficher_livres_empruntes(self):
        email = input("Entrez l'email de l'utilisateur : ")
        for utilisateur in self.utilisateurs:
            if utilisateur.email == email:
                print(f"Livres empruntés par {utilisateur.nom}: {utilisateur.livres_empruntes}")
                return
        print(f"Utilisateur avec l'email {email} non trouvé.")

    def afficher_historique(self):
        email = input("Entrez l'email de l'utilisateur : ")
        for utilisateur in self.utilisateurs:
            if utilisateur.email == email:
                print(f"Historique des emprunts de {utilisateur.nom}: {utilisateur.historique_emprunts}")
                return
        print(f"Utilisateur avec l'email {email} non trouvé.")

    def trier_utilisateurs(self):
        critere = input("Entrez le critère de tri (nom ou email) : ")
        self.utilisateurs.sort(key=lambda u: getattr(u, critere))
        self.sauvegarder_utilisateurs()
        print(f"Utilisateurs triés par {critere}.")

    def recherche_utilisateurs(self):
        critere = input("Entrez le critère de recherche (nom ou email) : ")
        valeur = input(f"Entrez la valeur pour {critere} : ")
        resultats = [u for u in self.utilisateurs if getattr(u, critere) == valeur]
        for utilisateur in resultats:
            print(utilisateur)

    def importer_donnees(self):
        fichier_csv = input("Entrez le nom du fichier CSV à importer : ")
        with open(fichier_csv, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.ajouter_utilisateur(row['nom'], row['email'])
        self.sauvegarder_utilisateurs()
        print("Données importées avec succès.")

    def afficher_utilisateurs_en_retard(self):
        date_actuelle = datetime.now().date()
        for utilisateur in self.utilisateurs:
            retards = [livre for livre in utilisateur.livres_empruntes if livre['date_retour'] < date_actuelle]
            if retards:
                print(f"Utilisateur {utilisateur.nom} a des retards: {retards}")

    def sauvegarder_utilisateurs(self):
        with open(self.fichier_json, 'w', encoding='utf-8') as file:
            json.dump([u.to_dict() for u in self.utilisateurs], file, ensure_ascii=False, indent=4)

    def charger_utilisateurs(self):
        try:
            with open(self.fichier_json, 'r', encoding='utf-8') as file:
                utilisateurs_dict = json.load(file)
                return [Utilisateur.from_dict(u) for u in utilisateurs_dict]
        except FileNotFoundError:
            return []

def menu_principal():
    gestion = GestionUtilisateurs('utilisateurs.json')
    options = {
        "1": gestion.ajouter_utilisateur,
        "2": gestion.supprimer_utilisateur,
        "3": gestion.lister_utilisateurs,
        "4": gestion.modifier_utilisateur,
        "5": gestion.afficher_livres_empruntes,
        "6": gestion.afficher_historique,
        "7": gestion.trier_utilisateurs,
        "8": gestion.recherche_utilisateurs,
        "9": gestion.importer_donnees,
        "10": gestion.afficher_utilisateurs_en_retard,
        "0": exit
    }

    while True:
        print("\nMenu:")
        print("1. Ajouter un utilisateur")
        print("2. Supprimer un utilisateur")
        print("3. Lister les utilisateurs")
        print("4. Modifier un utilisateur")
        print("5. Afficher les livres empruntés par un utilisateur")
        print("6. Afficher l'historique d'un utilisateur")
        print("7. Trier les utilisateurs")
        print("8. Recherche avancée d’utilisateurs")
        print("9. Importer les données à partir d'un fichier CSV")
        print("10. Afficher les utilisateurs ayant des retards")
        print("0. Quitter")
        choix = input("Entrez votre choix : ")

        if choix in options:
            options[choix]()
        else:
            print("Choix invalide, veuillez réessayer.")

# Démarrer le menu principal
if __name__ == "__main__":
    menu_principal()
