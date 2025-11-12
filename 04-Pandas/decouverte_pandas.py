"""
Découverte Pandas
Victor - Session 18 - Data Analysis
"""

import pandas as pd 

print("=== BIENVENUE DANS PANDAS ! ===\n")

# 1. Premier DataFrame
print("1️⃣ Premier DataFrame\n")

personnes = pd.DataFrame({
    'nom' : ['Tom', 'Alice', 'Bob', 'Charlie'],
    'age' : [33, 28, 35, 42],
    'ville': ['Paris', 'Lyon', 'Paris', 'Merseille'],
    'metier': ['jardinier', 'deve', 'designer', 'prof'],
})

print(personnes)
print()

# 2. Informations de base
print("2️⃣ Informations DataFrame\n")

print(f"Shape (dimensions) : {personnes.shape}")    #(Ligne, colonnes)
print(f"Colonnes : {list(personnes.columns)}")
print(f"Types : \n{personnes.dtypes}")
print()

# 3. Premières lignes
print("3️⃣ Premières lignes (head)\n")
print(personnes.head(2))
print()

# 4. Statistiques
print("4️⃣ Statistiques\n")
print(personnes.describe())   # Stats colonnes numériques
print()

# 5. Sélection colonne
print("5️⃣ Sélection colonne 'nom'\n")
print(personnes['nom'])
print()

# 6. Filtrage
print("6️⃣ Filtrage : Personnes à Paris\n")
parisiens = personnes[personnes['ville'] == 'Paris']
print(parisiens)
print()

# 7. Age moyen
print("7️⃣ Age moyen\n")
age_moyen = personnes['age'].mean()
print(f"Age moyen : {age_moyen} ans")