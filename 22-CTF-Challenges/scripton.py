code_chiffre = "fweh_2028"

code_original = ""
for caractere in code_chiffre:
    code_original += chr(ord(caractere) - 3)

print(f"Code chiffré : {code_chiffre}")
print(f"Code original : {code_original}")