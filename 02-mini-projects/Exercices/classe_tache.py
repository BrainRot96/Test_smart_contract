# Classe Tache - POO
# Tom - Session 15

class Tache:

    """Représente une tâche a faire"""

    def __init__(self, nom, priorite="Moyenne"):
        """
        Initialise une tâche

        Args : nom (str): Nom de la tâche
        priorite (str) : Haute, Moyenne ou Basse
        """

        self.nom = nom
        self.priorite = priorite
        self.terminee = False

    def marquer_terminee(self):
            """Marque la tâche comme terminée"""
            self.terminee = True 
            print(f"✅ {self.nom} terminée ")

    def afficher(self):
            """Afficher la tâche """
            statut = "✅" if self.terminee else "⏳"
            print("f{statut} {self.nom} - Priorité {self.priorite}")

    def __str__(self):
            """Representation en string (pour print direct)"""
            statut = "✅" if self.terminee else "⏳"
            return f"{statut} {self.nom} ({self.priorite})"

# === TESTS ===
print("=== Test Classe Tache ===\n")

# Créer quelques tâches
tache1 = Tache("Faire les courses", "Haute")
tache2 = Tache("Faire le ménage", "Basse")
tache3 = Tache("Arroser plantes")  # Priorité par défaut = Moyenne

# Liste de tâches
mes_taches = [tache1, tache2, tache3]

# Afficher toutes
print("État initial :")
for tache in mes_taches:
    tache.afficher()

# Marquer certaines terminées
print("\nMarquage terminée :")
tache1.marquer_terminee()
tache3.marquer_terminee()

# Afficher à nouveau
print("\nÉtat final :")
for tache in mes_taches:
    tache.afficher()

# Bonus : utiliser __str__
print("\nAvec print direct :")
for tache in mes_taches:
    print(tache)  # Appelle automatiquement __str__