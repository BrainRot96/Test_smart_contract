"""
🎯 CHALLENGE 3 : PASSWORD CRACKING

Objectif : Craque le mot de passe hashé !

Difficulté : 🟡 Moyen
Points : 20

Indice : Le mot de passe est dans une liste courante.
"""

import hashlib

def hash_password(password):
    """Hash un mot de passe avec SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def main():
    print("🎯 CHALLENGE 3 : PASSWORD CRACKING")
    print("="*50)
    print()
    
    # Hash du mot de passe secret
    password_hash = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
    
    print(f"Hash du mot de passe : {password_hash}")
    print()
    print("💡 Indice : C'est un mot de passe très courant...")
    print()
    
    # Liste de mots de passe courants
    common_passwords = [
        "123456",
        "password",
        "12345678",
        "qwerty",
        "abc123",
        "monkey",
        "letmein",
        "dragon",
        "111111",
        "baseball",
        "iloveyou",
        "trustno1",
        "1234567",
        "sunshine",
        "master",
        "welcome",
        "shadow",
        "ashley",
        "football",
        "jesus",
        "michael",
        "ninja",
        "mustang",
        "password1"
    ]
    
    print("🔍 Essaie de cracker le hash avec la liste de mots de passe courants...")
    print()
    
    tentative = input("➤ Méthode (1=Manuel, 2=Bruteforce) : ")
    
    if tentative == "1":
        # Mode manuel
        mdp = input("➤ Entre le mot de passe : ")
        if hash_password(mdp) == password_hash:
            print()
            print("✅ BRAVO ! Le flag est : flag{h4sh1ng_1s_n0t_3ncrypt10n}")
        else:
            print()
            print("❌ Mauvais mot de passe !")
    
    elif tentative == "2":
        # Mode bruteforce guidé
        print()
        print("💡 Code pour bruteforce :")
        print()
        print("for mdp in common_passwords:")
        print("    if hash_password(mdp) == password_hash:")
        print("        print(f'✅ Trouvé : {mdp}')")
        print()
        input("➤ Appuie sur Entrée pour exécuter...")
        
        found = False
        for mdp in common_passwords:
            hash_test = hash_password(mdp)
            if hash_test == password_hash:
                print(f"✅ MOT DE PASSE TROUVÉ : {mdp}")
                print()
                print("🚩 FLAG : flag{h4sh1ng_1s_n0t_3ncrypt10n}")
                found = True
                break
        
        if not found:
            print("❌ Mot de passe non trouvé dans la liste !")

if __name__ == "__main__":
    main()