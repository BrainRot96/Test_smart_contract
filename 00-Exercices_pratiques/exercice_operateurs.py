# EXERCICE : Système de connexion avec tentatives

# Variables globales

tentatives_restantes = 3 
utilisateur_connecte = False 

def verifier_connexion(username, password):
    """Vérifier si les identifiants sont correctes"""
    global tentatives_restantes, utilisateur_connecte

     # Identifiants corrects
    bon_username = "Tom"
    bon_password = "Python_2025"

    # Vérifier avec AND :
    if username == bon_username and password == bon_password:
        print("Connexion réussie")
        utilisateur_connecte = True
        return True
    
    else:
        tentatives_restantes -= 1
        print(f"❌ Échec ! Il te reste {tentatives_restantes} tentative(s)")
        return False 
    
def est_admin_ou_premium(statut):
    """Vérifie si l'utilisateur a des privilèges avec OR"""

    # Un utilisateur a accès s'il est admin OU premium

    if statut == "admin" or statut == "premium":
        return True
    else:
        return False 
    
# Programme principal : 

print("=== SYSTÈME DE CONNEXION ===\n")

# Boucle de connexion
while tentatives_restantes > 0 and not utilisateur_connecte:
    print(f"Tentatives restantes : {tentatives_restantes}")

    user = input("Username :")
    pwd = input("password :")

    verifier_connexion(user, pwd)
    print()

# On vérifie le résultat 

if utilisateur_connecte:
    print("Tu es maintenant connceté \n")

# Test des privilèges avec OR

    statut_user = input("Quel est ton statut ? (normal/premium/admin) : ")

    if est_admin_ou_premium(statut_user):
        print("🌟 Tu as accès aux fonctionnalités avancées !")

    else: 
        print("Accès noraml uniquement")

else: 
    print("🚫 Compte bloqué ! Trop de tentatives échouées.")

print(f"\nTentatives restantes finales : {tentatives_restantes}")
print(f"Connecté : {utilisateur_connecte}")





    
        
