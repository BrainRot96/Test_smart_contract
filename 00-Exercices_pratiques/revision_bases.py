# EXERCICE : Analyseur de notes

# 1. Demander une note

note_texte = input("Entre une note entre 0 et 100 :")
note = int(note_texte) #Convertir le texte en nombre 

# 2. Compter combien de chiffre dans la note (il faut utiliser len)

nombre_chiffres = len(note_texte)
print(f"Ta note a {nombre_chiffres} chiffre(s)")

# 3. Déterminer la lettre (il faut utiliser if/elif/else)

if note >= 90:
    lettre = "A"
elif note >= 80:
    lettre = "B"
elif note >= 70:
    lettre = "C"
elif note >= 60:
    lettre = "D"
else :
    lettre = "F"

print(f"Ta note de {note} correspond a : {lettre}")

compteur = 0 
print("\nComptons jusqu'à ta note :")

while compteur <= note:
    print(compteur, end=" ")
    compteur += 10 #On compte par 10

print(f"\n\nValeur finale du compteur : {compteur}")


