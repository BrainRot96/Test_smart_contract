import json
import os
from datetime import datetime

# ==== Fichier pour sauvegarder les données ====

FICHIER_DONNEES = "plantes.json"

# ==== Liste pour stocker les plantes ====

plantes = []

def afficher_menu():
    """Affiche le menu principal"""
    print("\n" + "="*50)
    print("🌱 JOURNAL BOTANIQUE 🌱")
    print("="*50)
    print("1. Ajouter plante")
    print("2. Voir toutes les plantes")
    print("3. Rechercher une plante")
    print("4. quitter")
    print("="*50)

# ==== Ajouter une plante ====

def ajouter_plante():
    """Ajoute une nouvelle plante au journal"""
    print("\n" + "="*50)
    print("🌱 AJOUTER UNE PLANTE")
    print("="*50)

    #Demander les infos :

    nom = input("Nom de la plante :")
    espece = input("Espèce (ex: Rosa, Ficus...)")
    lieu = input("Lieu (jardin, balcon, intérieur...)")
    notes = input("Notes (optionnel) :")

    #Créer le dictionnaire de plantes :

    plante = {
        "nom": nom,
        "espece": espece,
        "lieu": lieu,
        "date_ajout": datetime.now().strftime("%Y-%m-%d"),
        "notes": notes,
    }

    #Ajouter la liste : 

    plantes.append(plante)

    print(f"\n✅ {nom} ajouté(e) au journal !")
    sauvegarder_donnees()


# ==== Afficher toutes les plantes ====

def afficher_plantes():
    """Afficher toutes les plantes du journal"""
    print("\n" + "="*50)
    print("🌿 MES PLANTES")
    print("="*50)

    if len(plantes) == 0:
        print("\n📭 Aucune plante dans le journal pour le moment.")
        print("Commence par ajouter une plante !")
    else:
        for i, plante in enumerate(plantes, 1):
            print(f"\n{i}. 🌱 {plante['nom']}")
            print(f"   Espèce : {plante['espece']}")
            print(f"   Lieu : {plante['lieu']}")
            print(f"   Ajouté le : {plante['date_ajout']}")
            if plante['notes']:
                print(f"   Notes : {plante['notes']}")

        print(f"\n📊 Total : {len(plantes)} plante(s)")


# === Defis : Rechercher plante / Modification du menu

def rechercher_plantes():
    """Rechercher des plantes par critère"""
    print("\n" + "="*50)
    print("🔍 RECHERCHER DES PLANTES")
    print("="*50)

    if len(plantes) == 0:
        print("\n📭 Aucune plante dans le journal.")
        return
    
    print("\nRechercher par :")
    print("1. Nom")
    print("2. Lieu")
    print("3. Espece")

    choix = input("\nTon choix : ")

    if choix == "1":
        critere = "nom"
    elif choix == "2":
        critere = "lieu"
    elif choix == "3":
        critere = "espece"
    else: 
        print("❌ Choix invalide")
        return

    # Ces lignes doivent être INDENTÉES (au même niveau que le if)
    recherche = input(f"\nRecherche ({critere}) : ").lower()

    resultats = [p for p in plantes if recherche in p.get(critere, "").lower()]

    if len(resultats) == 0:
        print(f"\n❌ Aucune plante trouvée avec '{recherche}'")
    else:
        print(f"\n✅ {len(resultats)} plante(s) trouvée(s) :\n")
        for i, plante in enumerate(resultats, 1):
            print(f"{i}. 🌱 {plante['nom']}")
            for cle, valeur in plante.items():
                if cle != "nom" and valeur:
                    print(f"   {cle} : {valeur}")
            print()

# ==== Sauvegarder les données ====

def sauvegarder_donnees():
    """Sauvegarde les plantes dans un fichier JSON"""
    with open(FICHIER_DONNEES, 'w', encoding='utf-8') as f:
        json.dump(plantes, f, ensure_ascii=False, indent=2)
    print("💾 Données sauvegardées !")


# ==== Charge les données du JSON ====

def charger_donnees():
    """Charge les plantes depuis le fichier JSON"""
    global plantes 
    if os.path.exists(FICHIER_DONNEES):
        with open(FICHIER_DONNEES, 'r', encoding='utf-8') as f:
            plantes = json.load(f)
        print(f"✅ {len(plantes)} plante(s) chargée(s) !")
    else:
        print("📁 Nouveau journal créé !")



# ==== Programme principal ====

print("Bienvenue dans ton journal botanique")
charger_donnees()

while True:
    afficher_menu()
    choix = input("\nTon choix :")

    if choix == "1":
        ajouter_plante()
    elif choix == "2":
        afficher_plantes()
    elif choix == "3":
        rechercher_plantes()      
    elif choix == "4":
        sauvegarder_donnees() 
        print("\nA bientôt")
        break
    else:
          print("\n❌ Choix invalide !")
     

