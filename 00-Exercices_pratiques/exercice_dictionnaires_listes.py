# EXERCICE 1 : Accès sécurisé avec .get()

plante = {
    "nom": "Basilic",
    "espece": "Ocimum Basilicum",
    "lieu": "balcon"
    
}

prix = plante.get("prix", "non défini")
notes = plante.get("notes", "aucune note")
arrosage = plante.get("arrosage", "quotidien")

print(f"Prix : {prix}")
print(f"Notes : {notes}")
print(f"Arrosage : {arrosage}")

print("\n" + "="*50)
print("EXERCICE 2 : append() vs extend()")
print("="*50)

# Liste de départ

plante_balcon = ["basilic", "menthe"]

# Méthode 1 : append() - ajoute UN élément (même si c'est une liste)

plante_balcon_v1 = plante_balcon.copy()
plante_balcon_v1.append(["Thym", "Romarain"])

print(f"\nAvec append() : {plante_balcon_v1}")
print(f"Nombre d'éléments : {len(plante_balcon_v1)}")

# Méthode 2 : extend() - ajoute CHAQUE élément

plante_balcon_v2 = plante_balcon.copy()
plante_balcon_v2.extend(["Thym", "Romarain"])

print(f"\nAvec extend() : {plante_balcon_v2}")
print(f"Nombre d'éléments : {len(plante_balcon_v2)}")

# Défis :

mes_plantes = ["Basilic"]
mes_plantes.extend(["Coriandre", "Persil"])

print(mes_plantes)

print("\n" + "="*50)
print("EXERCICE 3 : List Comprehension (filtrage)")
print("="*50)

plantes = [
    {"nom": "Basilic", "lieu": "Balcon", "arrosage": "Quotidien"},
    {"nom": "Cactus", "lieu": "Interieur", "arrosage": "hebdomadaire"},
    {"nom": "Menthe", "lieu": "Balcon", "arrosage": "Quotidien"},
    {"nom": "Ficus", "lieu": "Interieur", "arrosage": "hebdomadaire"},
]

# Méthode classique (longue)
plantes_balcon_classique = []
for plante in plantes:
    if plante["lieu"] == "Balcon":
        plantes_balcon_classique.append(plante["nom"])

print(f"\nMéthode classique : {plantes_balcon_classique}")

# Méthode avec list comprehension (courte et élégante !)
plantes_balcon_comprehension = [p["nom"] for p in plantes if p["lieu"] == "Balcon"]

print(f"Avec comprehension : {plantes_balcon_comprehension}")

# Défis :
plantes_quotidien = [p["nom"] for p in plantes if p["arrosage"] == "Quotidien"]

print(f"\nPlantes a arrosage quotidien {plantes_quotidien}")

print("\n" + "="*50)
print("EXERCICE 4 : Boucler sur un dictionnaire")
print("="*50)


plante = {
    "nom": "Basilic",
    "espece": "Ocimum basilicum",
    "lieu": "Balcon",
    "arrosage": "Quotidien"
}

# Méthode 1 : Boucle sur les CLÉS (par défaut)
print("\n📋 Les clés :")

for cle in plante:
    print(f"  - {cle}")

# Méthode 2 : Boucle sur les VALEURS
print("\n📝 Les valeurs :")

for valeur in plante.values():
    print(f"  - {valeur}")

# Méthode 3 : Boucle sur CLÉS ET VALEURS (le plus utile !)
print("\n📊 Clés + Valeurs :")

for cle, valeur in plante.items():
    print(f"  {cle} : {valeur}")

# TON DÉFI : Affiche toutes les infos de cette plante avec .items()

ma_plante = {
    "nom": "Cactus",
    "type": "Succulent",
    "age_ans": 3
}

print("\n🌵 Infos de ma plante :")

for cle, valeur in ma_plante.items():
    print(f"  {cle} : {valeur}")