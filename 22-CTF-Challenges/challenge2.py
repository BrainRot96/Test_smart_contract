"""
🎯 CHALLENGE 2 : REVERSE ENGINEERING

Objectif : Comprends la logique et trouve le flag !

Difficulté : 🟢 Facile
Points : 15

Indice : Analyse la fonction de vérification.
"""

def fonction_mysterieuse(n):
    """Fonction qui fait quelque chose..."""
    resultat = ""
    for i in range(len(n)):
        resultat += chr(ord(n[i]) + 3)
    return resultat

def verifier_code(code):
    """Vérifie si le code est correct"""
    code_chiffre = "fweh_2028"
    
    if fonction_mysterieuse(code) == code_chiffre:
        return True
    return False

def main():
    print("🎯 CHALLENGE 2 : REVERSE ENGINEERING")
    print("="*50)
    print()
    print("Trouve le code secret pour obtenir le flag !")
    print()
    
    tentative = input("➤ Entre le code secret : ")
    
    if verifier_code(tentative):
        print()
        print("✅ EXCELLENT ! Le flag est : flag{r3v3rs3_3ng1n33r1ng}")
    else:
        print()
        print("❌ Code incorrect ! Continue à chercher...")
        print("💡 Indice : Regarde ce que fait fonction_mysterieuse()")

if __name__ == "__main__":
    main()