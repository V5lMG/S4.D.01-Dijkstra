import importation
import exportation
from parcours import a_star
from plateau import Plateau


class Application:
    def __init__(self):
        """Initialise l'application."""
        self.plateau = None  # Stocke le plateau généré ou importé

    def afficher_menu(self):
        """Affiche le menu principal et gère les choix de l'utilisateur."""
        choix = ""
        while choix != "Q":
            print("""
                Bienvenue sur notre application d'analyse des algorithmes A* et Dijkstra !
                Veuillez choisir une action :
                    G - Générer un plateau de jeu
                    I - Importer un plateau de jeu existant (.txt)
                    Q - Quitter l'application
            """)
            choix = input("Votre choix : ").strip().upper()

            if choix == "G":
                self.generer_plateau()
            elif choix == "I":
                self.importer_plateau()
            elif choix != "Q":
                print("❌ Choix invalide. Veuillez entrer G, I ou Q.")

    def generer_plateau(self):
        """Génère un plateau de jeu selon les paramètres de l'utilisateur."""
        largeur = self.saisir_valeur("la largeur du plateau (>= 3)", min_val=3)
        longueur = self.saisir_valeur("la longueur du plateau (>= 3)", min_val=3)
        taux = self.saisir_valeur("le taux de cases interdites (0-100)", min_val=0, max_val=100) / 100
        placement_aleatoire = self.saisir_oui_non("Placer départ/arrivée aléatoirement ? (O/N)")

        # Création du plateau
        self.plateau = Plateau(largeur, longueur, taux, placement_aleatoire)
        print("\nPlateau généré :")
        self.plateau.afficher_plateau()

        # Choix de l'algorithme
        self.lancer_algorithme()

    def importer_plateau(self):
        """Importe un plateau à partir d'un fichier texte."""
        chemin_fichier = input("Entrez le chemin du fichier .txt : ").strip()
        while not chemin_fichier.endswith(".txt"):
            print("❌ Erreur : le fichier doit être au format .txt.")
            chemin_fichier = input("Entrez un chemin valide : ").strip()

        importateur = importation.Importateur(chemin_fichier)
        self.plateau = importateur.importer_plateau()

        if self.plateau:
            self.plateau.afficher_plateau()
            self.lancer_algorithme()

    def lancer_algorithme(self):
        """Demande à l'utilisateur quel algorithme utiliser et exécute le chemin optimal."""
        choix_algo = ""
        while choix_algo not in ["A", "D"]:
            choix_algo = input("Choisissez un algorithme : A (A*) ou D (Dijkstra) : ").strip().upper()
            if choix_algo not in ["A", "D"]:
                print("❌ Réponse invalide. Entrez 'A' pour A* ou 'D' pour Dijkstra.")

        use_a_star = (choix_algo == "A")
        algo = a_star(self.plateau, use_a_star=use_a_star)
        algo.executer()
        plateau_avec_chemin = algo.afficher_resultat()

        # Exportation du plateau
        nom_fichier = input("Entrez un nom de fichier pour exporter le plateau : ").strip()
        exportateur = exportation.Exportateur(self.plateau, plateau_avec_chemin, nom_fichier)
        exportateur.exporter_vers_txt()

    def saisir_valeur(self, message, min_val=None, max_val=None):
        """Demande une valeur numérique valide à l'utilisateur."""
        while True:
            try:
                valeur = int(input(f"Veuillez entrer {message} : ").strip())
                if (min_val is not None and valeur < min_val) or (max_val is not None and valeur > max_val):
                    raise ValueError
                return valeur
            except ValueError:
                print(f"❌ Erreur : La valeur doit être un entier entre {min_val} et {max_val}.")

    def saisir_oui_non(self, message):
        """Demande une réponse Oui/Non et retourne un booléen."""
        reponse = ""
        while reponse not in ["O", "N"]:
            reponse = input(f"{message} ").strip().upper()
            if reponse not in ["O", "N"]:
                print("❌ Réponse invalide. Entrez 'O' pour Oui ou 'N' pour Non.")
        return reponse == "O"


# Lancement de l'application
if __name__ == "__main__":
    app = Application()
    app.afficher_menu()
