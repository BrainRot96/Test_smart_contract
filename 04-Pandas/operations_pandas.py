"""
Opérations Pandas avancées
Victor - Session 18 - Manipulation données
"""
import pandas as pd

print("=== OPÉRATIONS PANDAS AVANCÉES ===\n")

# ========================================
# 1️⃣ CHARGER CSV
# ========================================

print("1️⃣ CHARGEMENT CSV\n")

plantes = pd.read_csv('plantes_idf.csv')
print("✅ Fichier chargé !")
print(f"📊 {len(plantes)} plantes chargées\n")

# ========================================
# 2️⃣ EXPLORER DONNÉES
# ========================================
print("2️⃣ EXPLORATION\n")

# Premières lignes
print("📋 Premières lignes :")
print(plantes.head(3))
print()

# Informations générales
print("ℹ️ Informations générales :")
print(plantes.info())
print()

# Statistiques colonnes numériques
print("📊 Statistiques :")
print(plantes.describe())
print()

# ========================================
# 3️⃣ SÉLECTION COLONNES
# ========================================
print("3️⃣ SÉLECTION COLONNES\n")

# Une colonne (Series)
noms = plantes['nom']
print("Noms plantes :")
print(noms)
print()

# Plusieurs colonnes (DataFrame)
plantes_info = plantes[['nom', 'espece', 'prix_euros']]
print("Nom + Espece + Prix :")
print(plantes_info)
print()

# ========================================
# 4️⃣ FILTRAGE SIMPLE
# ========================================
print("4️⃣ FILTRAGE SIMPLE\n")

# Plantes à Paris
plantes_paris = plantes[plantes['zone'] == 'Paris']
print(f"🏙️ Plantes Paris : {len(plantes_paris)}")
print(plantes_paris[['nom', 'espece', 'zone']])
print()

# Plantes < 10€
plantes_pas_cher = plantes[plantes['prix_euros'] < 10]
print(f"💰 Plantes < 10€ : {len(plantes_pas_cher)}")
print(plantes_pas_cher[['nom', 'prix_euros']])
print()

# ========================================
# 5️⃣ FILTRAGE MULTIPLE (ET / OU)
# ========================================
print("5️⃣ FILTRAGE MULTIPLE\n")

# ET (& ) : Paris ET arrosage faible
filtre_et = plantes[
    (plantes['zone'] == 'Paris') &
    (plantes['arrosage'] == 'Faible')
    
]
print("🌱 Paris + Arrosage faible :")
print(filtre_et[['nom', 'zone', 'arrosage']])
print()

# OU (|) : Prix < 8 OU hauteur > 100
filtre_ou = plantes[
    (plantes['prix_euros'] < 8) | 
    (plantes['hauteur_cm'] > 100)
]
print("💰 Prix < 8€ OU Hauteur > 100cm :")
print(filtre_ou[['nom', 'prix_euros', 'hauteur_cm']])
print()

# ========================================
# 6️⃣ TRIER DONNÉES
# ========================================
print("6️⃣ TRI\n")

# Trier par prix (croissant)
tri_prix = plantes.sort_values('prix_euros')
print("Tri par prix (↗️) :")
print(tri_prix[['nom', 'prix_euros']].head())
print()

# Trier par hauteur (décroissant)
tri_hauteur = plantes.sort_values('hauteur_cm', ascending=False)
print("Tri par hauteur (↘️) :")
print(tri_hauteur[['nom', 'hauteur_cm']].head())
print()

# ========================================
# 7️⃣ GROUPER ET AGRÉGER (groupby)
# ========================================
print("7️⃣ GROUPBY (agrégation)\n")

# Prix moyen par zone
# Prix moyen par zone
prix_par_zone = plantes.groupby('zone')['prix_euros'].mean()
print("💰 Prix moyen par zone :")
print(prix_par_zone)
print()

# Nombre plantes par type arrosage
count_arrosage = plantes.groupby('arrosage').size()
print("💧 Nombre plantes par arrosage :")
print(count_arrosage)
print()

# Statistiques multiples par zone
stats_zone = plantes.groupby('zone').agg({
    'prix_euros': ['mean', 'min', 'max'],
    'hauteur_cm': 'mean'
})
print("📊 Stats complètes par zone :")
print(stats_zone)
print()

# ========================================
# 8️⃣ AJOUTER COLONNE CALCULÉE
# ========================================
print("8️⃣ COLONNE CALCULÉE\n")

# Prix par cm de hauteur
plantes['prix_par_cm'] = plantes['prix_euros'] / plantes['hauteur_cm']
print("Ajout colonne 'prix_par_cm' :")
print(plantes[['nom', 'prix_euros', 'hauteur_cm', 'prix_par_cm']].head())
print()

# Catégorie prix
def categoriser_prix(prix):
    if prix < 10:
        return 'Bon marché'
    elif prix < 15:
        return 'Moyen'
    else:
        return 'Cher'

plantes['categorie_prix'] = plantes['prix_euros'].apply(categoriser_prix)
print("Ajout colonne 'categorie_prix' :")
print(plantes[['nom', 'prix_euros', 'categorie_prix']].head())
print()

# ========================================
# 9️⃣ RÉSUMÉ FINAL
# ========================================
print("9️⃣ RÉSUMÉ ANALYSE\n")

print(f"📊 Total plantes : {len(plantes)}")
print(f"🏙️ Plantes Paris : {len(plantes[plantes['zone'] == 'Paris'])}")
print(f"💰 Prix moyen : {plantes['prix_euros'].mean():.2f}€")
print(f"📏 Hauteur moyenne : {plantes['hauteur_cm'].mean():.0f}cm")
print(f"💧 Arrosage le plus commun : {plantes['arrosage'].mode()[0]}")
print()

print("✅ Opérations Pandas maîtrisées !")