import json
import os 

print("🛡️ ANALYSEUR DE MOTS DE PASSE 🛡️\n")

def analyser_mot_de_passe(password):
    """Analyse de la force des mots de passes"""
    score = 0
    problemes = []

    # Critère 1 : Longueur (TON DÉFI)
    
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        problemes.append("❌ Trop court (minimum 8 caractères)")

    # Critère 2 : Contient des chiffres (TON DÉFI)
    # Vérifie si le mot de passe contient au moins un chiffre

    if any(c.isdigit() for c in password):
        score += 1
    else:
        problemes.append("❌ Aucun chiffre")

    # Critère 3 : Contient des majuscules
    # TON CODE ICI - Comme pour les chiffres mais avec .isupper()

    if any(c.isupper() for c in password):
        score += 1
    else:
        problemes.append("❌ Aucune majuscule")

    # Critère 4 : Contient des caractères spéciaux
    caracteres_speciaux = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    if any(c in caracteres_speciaux for c in password):
        score += 1
    else:
        problemes.append("❌ Aucun caractère spécial")
    
    return score, problemes

def verifier_mot_de_passe_compromis(password):
    """Vérifie si le mot de passe est dans une liste de mot de passe compromis"""

# Liste des mots de passe les plus utilisés (et donc compromis)
    mots_de_passe_compromis = [
        "password", "123456", "123456789", "12345678", "12345",
        "password123", "qwerty", "abc123", "111111", "123123",
        "admin", "letmein", "welcome", "monkey", "dragon",
        "master", "sunshine", "princess", "football", "iloveyou"
    ]

    # Vérifier si le password (en minuscules) est dans la liste

    if password.lower() in mots_de_passe_compromis:
        return True
    
    # Vérifier aussi des variations communes

    variations = [
        password.lower(),
        password.lower() + "123",
        password.lower() + "!",
        "123" + password.lower(),
        password.lower().replace("123", ""),
        password.lower().replace("!", "")
    ]

    for variation in variations:
        if variation in mots_de_passe_compromis:
            return True
    
    return False



# ====================================================================


# Programme principal
def afficher_menu():
    """Affiche le menu"""
    print("\n" + "="*50)
    print("🛡️  ANALYSEUR DE MOTS DE PASSE")
    print("="*50)
    print("1. Analyser un mot de passe")
    print("2. Voir l'historique des analyses")
    print("3. Quitter")
    print("="*50)

def sauvegarder_analyse(password, score, problemes, compromis):
    """Sauvegarde l'analyse dans un fichier JSON"""
    from datetime import datetime
    
    # Charger l'historique existant
    fichier = "historique_analyses.json"
    if os.path.exists(fichier):
        with open(fichier, 'r', encoding='utf-8') as f:
            historique = json.load(f)
    else:
        historique = []
    
    # Ajouter la nouvelle analyse (masquer le mot de passe pour la sécurité !)
    analyse = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "longueur": len(password),
        "score": score,
        "compromis": compromis,
        "problemes": problemes
    }
    
    historique.append(analyse)
    
    # Sauvegarder
    with open(fichier, 'w', encoding='utf-8') as f:
        json.dump(historique, f, ensure_ascii=False, indent=2)

def afficher_historique():
    """Affiche l'historique des analyses"""
    fichier = "historique_analyses.json"
    
    if not os.path.exists(fichier):
        print("\n📭 Aucune analyse dans l'historique.")
        return
    
    with open(fichier, 'r', encoding='utf-8') as f:
        historique = json.load(f)
    
    print(f"\n📊 HISTORIQUE ({len(historique)} analyses)")
    print("="*50)
    
    for i, analyse in enumerate(historique, 1):
        print(f"\n{i}. {analyse['date']}")
        print(f"   Longueur : {analyse['longueur']} caractères")
        print(f"   Score : {analyse['score']}/5")
        print(f"   Compromis : {'🚨 OUI' if analyse['compromis'] else '✅ NON'}")
        if analyse['problemes']:
            print(f"   Problèmes : {len(analyse['problemes'])}")

# Boucle principale
while True:
    afficher_menu()
    choix = input("\nTon choix : ")
    
    if choix == "1":
        password = input("\nEntre un mot de passe à analyser : ")
        
        # Vérifier si compromis
        compromis = verifier_mot_de_passe_compromis(password)
        
        if compromis:
            print("\n🚨 ALERTE DE SÉCURITÉ ! 🚨")
            print("Ce mot de passe est COMPROMIS")
            sauvegarder_analyse(password, 0, ["Mot de passe compromis"], True)
        else:
            score, problemes = analyser_mot_de_passe(password)
            
            print(f"\n📊 Score de sécurité : {score}/5")
            
            if score >= 4:
                print("🟢 Niveau : FORT")
            elif score >= 2:
                print("🟡 Niveau : MOYEN")
            else:
                print("🔴 Niveau : FAIBLE")
            
            if problemes:
                print("\n⚠️  Problèmes détectés :")
                for probleme in problemes:
                    print(f"  {probleme}")
            
            sauvegarder_analyse(password, score, problemes, False)
            print("\n💾 Analyse sauvegardée")
    
    elif choix == "2":
        afficher_historique()
    
    elif choix == "3":
        print("\n👋 À bientôt !")
        break
    
    else:
        print("\n❌ Choix invalide")