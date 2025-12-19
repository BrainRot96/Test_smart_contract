"""
🎯 CHALLENGE 5 : XOR CIPHER

Objectif : Décrypte le message XOR avec la clé secrète !

Difficulté : 🔴 Difficile
Points : 30

Indice : XOR est réversible avec la même clé.
"""

def xor_encrypt(texte, cle):
    """Chiffre/déchiffre avec XOR"""
    resultat = ""
    for i in range(len(texte)):
        char_texte = texte[i]
        char_cle = cle[i % len(cle)]
        xor_result = ord(char_texte) ^ ord(char_cle)
        resultat += chr(xor_result)
    return resultat

def main():
    print("🎯 CHALLENGE 5 : XOR CIPHER")
    print("="*50)
    print()
    
    # Message CORRECTEMENT chiffré avec la clé "ctf"
    message_original = "flag{x0r_c1ph3r_1s_r3v3rs1bl3}"
    cle_secrete = "ctf"
    message_chiffre = xor_encrypt(message_original, cle_secrete)
    
    print("📜 MESSAGE CHIFFRÉ (illisible) :")
    print(repr(message_chiffre))
    print()
    
    print("💡 INDICE 1 : Le message a été chiffré avec XOR")
    print("💡 INDICE 2 : La clé est un mot de 3 lettres")
    print("💡 INDICE 3 : Le message déchiffré commence par 'flag{'")
    print("💡 INDICE 4 : Pense au nom de ce type de challenge...")
    print()
    
    choix = input("➤ Méthode (1=Manuel, 2=Bruteforce, 3=Aide) : ")
    
    if choix == "1":
        cle = input("➤ Entre la clé : ")
        dechiffre = xor_encrypt(message_chiffre, cle)
        
        print()
        print(f"Message déchiffré : {dechiffre}")
        
        if dechiffre == message_original:
            print()
            print("✅ BRAVO ! Tu as trouvé la bonne clé !")
            print(f"🔑 Clé : {cle}")
            print(f"🚩 Flag : {dechiffre}")
        else:
            print()
            print("❌ Mauvaise clé... Le message n'est pas lisible.")
    
    elif choix == "2":
        print()
        print("🔍 Bruteforce avec clés courantes...")
        print()
        
        cles_courantes = [
            "key", "ctf", "hack", "xor", "code", 
            "flag", "pass", "secret", "pwn", "bin"
        ]
        
        input("➤ Appuie sur Entrée pour lancer...")
        print()
        
        for cle in cles_courantes:
            dechiffre = xor_encrypt(message_chiffre, cle)
            
            # Vérifier si c'est lisible (commence par 'flag{')
            if dechiffre.startswith("flag{"):
                print(f"✅ Clé '{cle}' : {dechiffre}")
                print()
                print("🎉 CLÉ TROUVÉE !")
                print(f"🔑 Clé secrète : {cle}")
                print(f"🚩 Flag : {dechiffre}")
                break
            else:
                print(f"❌ Clé '{cle}' : {dechiffre[:20]}... (illisible)")
    
    elif choix == "3":
        print()
        print("📚 COMPRENDRE XOR :")
        print()
        print("XOR (eXclusive OR) - Opération binaire :")
        print()
        print("  0 XOR 0 = 0")
        print("  0 XOR 1 = 1")
        print("  1 XOR 0 = 1")
        print("  1 XOR 1 = 0")
        print()
        print("✨ PROPRIÉTÉ MAGIQUE : A XOR B XOR B = A")
        print()
        print("Exemple concret :")
        print()
        print("  Message : 'H' (code ASCII 72)")
        print("  Clé : 'K' (code ASCII 75)")
        print()
        print("  CHIFFREMENT :")
        print("  72 XOR 75 = 3 → Caractère chiffré")
        print()
        print("  DÉCHIFFREMENT :")
        print("  3 XOR 75 = 72 → 'H' (message original !)")
        print()
        print("→ La même clé chiffre ET déchiffre !")
        print()
        print("🎯 Pour ce challenge :")
        print("  - Essaie des mots de 3 lettres")
        print("  - Le message commence par 'flag{'")
        print("  - Indice : C'est le nom de ce type de challenge...")
        print()
        
        input("➤ Appuie sur Entrée pour revenir...")
        main()

if __name__ == "__main__":
    main()