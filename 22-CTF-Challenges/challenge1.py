"""
🎯 CHALLENGE 1 : CODE ANALYSIS

Objectif : Trouve le flag caché dans ce code !

Difficulté : 🟢 Facile
Points : 10

Indice : Lis attentivement le code et exécute-le.
"""

def verifier_mot_de_passe(tentative):
    """Fonction mystérieuse"""
    mot_de_passe_secret = "cyber_2025"
    
    if tentative == mot_de_passe_secret:
        return True
    return False

def afficher_message():
    """Affiche un message"""
    print("Bienvenue dans le CTF Challenge 1 !")
    print("Trouve le mot de passe pour obtenir le flag.")
    print()

def reveler_flag(mdp):
    """Révèle le flag si le mot de passe est correct"""
    if verifier_mot_de_passe(mdp):
        flag = "flag{b1env3nue_dans_le_ctf}"
        print(f"✅ BRAVO ! Voici ton flag : {flag}")
        return flag
    else:
        print("❌ Mauvais mot de passe !")
        return None

# Programme principal
if __name__ == "__main__":
    afficher_message()
    
    # Demander le mot de passe
    tentative = input("➤ Entre le mot de passe : ")
    reveler_flag(tentative)