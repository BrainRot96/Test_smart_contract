
class Plante:

    """Représente une plante du jardin """

    def __init__(self, nom, espece):
        """Initialise une plante"""
        self.nom = nom
        self.espece = espece
        self.arrosee = False

    def arroser(self):
        """Arroser la plante"""
        self.arrosee = True
        print(f"💧 {self.nom} arrosée !")

    def afficher(self):
        """Affiche info plante"""
        statut = "💧" if self.arrosee else "🏜️"
        print(f"{statut} {self.nom} ({self.espece})")



# Test
print("=== Test Classe Plante ===\n")

# Créer 3 plantes
rose = Plante("Rosa", "Rose")
tulipe = Plante("Tulipa", "Tulipe")
orchidee = Plante("Orchis", "Orchidée")

# Afficher toutes
print("État initial :")
rose.afficher()
tulipe.afficher()
orchidee.afficher()

print("\nArrosage de la rose et l'orchidée :")
rose.arroser()
orchidee.arroser()

print("\nÉtat final :")
rose.afficher()
tulipe.afficher()
orchidee.afficher()