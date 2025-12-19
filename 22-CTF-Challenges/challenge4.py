"""
🎯 CHALLENGE 4 : BASE64 DECODING

Objectif : Décode le message encodé en Base64 !

Difficulté : 🟡 Moyen
Points : 25

Indice : Base64 est un encodage, pas du chiffrement.
"""

import base64

def main():
    print("🎯 CHALLENGE 4 : BASE64 DECODING")
    print("="*50)
    print()
    
    # Messages encodés
    message1 = "Qm9uam91ciBUb20gIQ=="
    message2 = "VHUgZXMgdW4gaGFja2VyICE="
    message3 = "VGUgdm9pbGEgbGUgZmxhZyA6IGZsYWd7YjRzMzY0X2lzX24wdF9zM2N1cjN9"
    
    print("📋 MESSAGES ENCODÉS EN BASE64 :")
    print()
    print(f"Message 1 : {message1}")
    print(f"Message 2 : {message2}")
    print(f"Message 3 : {message3}")
    print()
    
    print("💡 INDICE : Base64 est un encodage standard")
    print("💡 Tu peux décoder avec Python ou un site en ligne")
    print()
    
    choix = input("➤ Méthode (1=Manuel, 2=Automatique) : ")
    
    if choix == "1":
        # Mode manuel
        print()
        print("📖 POUR DÉCODER EN PYTHON :")
        print()
        print("import base64")
        print("message = 'Qm9uam91ciBUb20gIQ=='")
        print("decoded = base64.b64decode(message).decode('utf-8')")
        print("print(decoded)")
        print()
        
        tentative = input("➤ Entre le flag décodé : ")
        
        if "flag{b4s364_is_n0t_s3cur3}" in tentative:
            print()
            print("✅ BRAVO ! Tu as réussi !")
        else:
            print()
            print("❌ Pas tout à fait... Essaie de décoder le message 3 !")
    
    elif choix == "2":
        # Mode automatique
        print()
        print("🔓 DÉCODAGE AUTOMATIQUE :")
        print()
        
        input("➤ Appuie sur Entrée pour décoder...")
        
        # Décoder les messages
        decoded1 = base64.b64decode(message1).decode('utf-8')
        decoded2 = base64.b64decode(message2).decode('utf-8')
        decoded3 = base64.b64decode(message3).decode('utf-8')
        
        print()
        print(f"Message 1 : {decoded1}")
        print(f"Message 2 : {decoded2}")
        print(f"Message 3 : {decoded3}")
        print()
        print("🚩 FLAG TROUVÉ !")

if __name__ == "__main__":
    main()