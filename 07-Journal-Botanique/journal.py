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
    print("4. Supprimer une plante")
    print("5. Modifier une plante")
    print("6. Statistiques")
    print("7. Quitter")
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

def supprimer_plante():
    """Supprime une plante du journal"""
    print("\n" + "="*50)
    print("🗑️  SUPPRIMER UNE PLANTE")
    print("="*50)
    
    if len(plantes) == 0:
        print("\n📭 Aucune plante dans le journal.")
        return
    
    # Afficher toutes les plantes avec numéros
    print("\nPlantes disponibles :")
    for i, plante in enumerate(plantes, 1):
        print(f"{i}. {plante['nom']} ({plante['lieu']})")
    
    # Demander quelle plante supprimer
    try:
        choix = int(input("\nNuméro de la plante à supprimer (0 pour annuler) : "))
        
        if choix == 0:
            print("❌ Suppression annulée")
            return
        
        if 1 <= choix <= len(plantes):
            plante_supprimee = plantes[choix - 1]
            
            # Confirmation
            confirm = input(f"\n⚠️  Confirmer la suppression de '{plante_supprimee['nom']}' ? (oui/non) : ")
            
            if confirm.lower() in ['oui', 'o', 'yes', 'y']:
                plantes.pop(choix - 1)
                sauvegarder_donnees()
                print(f"\n✅ {plante_supprimee['nom']} supprimé(e) du journal")
            else:
                print("❌ Suppression annulée")
        else:
            print("❌ Numéro invalide")
    
    except ValueError:
        print("❌ Entrée invalide")

def modifier_plante():
    """Modifie une plante existante"""
    print("\n" + "="*50)
    print("✏️  MODIFIER UNE PLANTE")
    print("="*50)

    if len(plantes) == 0:
        print("\n📭 Aucune plante dans le journal.")
        return
    
    # Afficher toutes les plantes :
    print("\nPlantes disponibles :")
    for i, plante in enumerate(plantes, 1):
        print(f"{i}. {plante['nom']} ({plante['lieu']})")

    # Demander quel plante modifier :
    try:
        choix = int(input("\nNuméro de la plante a modifier (0 pour annuler) : "))

        if choix == 0:
            print("❌ Modification annulée")
            return
        
        if 1 <= choix <= len(plantes):
            plante = plantes[choix - 1]

            print(f"\n📝 Modification de : {plante['nom']}")
            print("\nLaisse vide pour conserver la valeur actuelle")
            print("="*50)

            # Modifier chaque champ
            nouveau_nom = input(f"Nom [{plante['nom']}] : ")
            if nouveau_nom.strip():
                plante['nom'] = nouveau_nom
            
            nouvelle_espece = input(f"Espèce [{plante['espece']}] : ")
            if nouvelle_espece.strip():
                plante['espece'] = nouvelle_espece
            
            nouveau_lieu = input(f"Lieu [{plante['lieu']}] : ")
            if nouveau_lieu.strip():
                plante['lieu'] = nouveau_lieu
            
            nouvelles_notes = input(f"Notes [{plante.get('notes', '')}] : ")
            if nouvelles_notes.strip():
                plante['notes'] = nouvelles_notes
            
            # Sauvegarder
            sauvegarder_donnees()
            print(f"\n✅ {plante['nom']} modifié(e) avec succès !")
        else:
            print("❌ Numéro invalide")
    
    except ValueError:
        print("❌ Entrée invalide")

def afficher_statistiques():
    """Affiche des statistiques sur le journal"""
    print("\n" + "="*50)
    print("📊 STATISTIQUES DU JOURNAL")
    print("="*50)
    
    if len(plantes) == 0:
        print("\n📭 Aucune plante dans le journal.")
        return
    
    # Nombre total
    print(f"\n🌱 Total de plantes : {len(plantes)}")
    
    # Plantes par lieu
    lieux = {}
    for plante in plantes:
        lieu = plante['lieu']
        lieux[lieu] = lieux.get(lieu, 0) + 1
    
    print("\n📍 Plantes par lieu :")
    for lieu, count in sorted(lieux.items(), key=lambda x: x[1], reverse=True):
        print(f"   - {lieu} : {count} plante(s)")
    
    # Plantes par espèce
    especes = {}
    for plante in plantes:
        espece = plante['espece']
        especes[espece] = especes.get(espece, 0) + 1
    
    print("\n🌿 Plantes par espèce :")
    for espece, count in sorted(especes.items(), key=lambda x: x[1], reverse=True):
        print(f"   - {espece} : {count} plante(s)")
    
    # Plante la plus récente
    plantes_triees = sorted(plantes, key=lambda x: x['date_ajout'], reverse=True)
    plus_recente = plantes_triees[0]
    print(f"\n🆕 Plante la plus récente : {plus_recente['nom']} ({plus_recente['date_ajout']})")
    
    # Plante la plus ancienne
    plus_ancienne = plantes_triees[-1]
    print(f"📅 Plante la plus ancienne : {plus_ancienne['nom']} ({plus_ancienne['date_ajout']})")



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
        supprimer_plante()
    elif choix == "5":
        modifier_plante()
    elif choix == "6":
        afficher_statistiques()
    elif choix == "7":    
        sauvegarder_donnees() 
        print("\nA bientôt")
        break
    else:
          print("\n❌ Choix invalide !")
     

