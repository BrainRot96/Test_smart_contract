import requests 
from bs4 import BeautifulSoup
import csv 

print("=== SCRAPER DE LIVRES ===\n")

url = "http://books.toscrape.com/"
responses = requests.get(url)

if responses.status_code == 200:
    print("✅ Connecté au site de livres !\n")
    soup = BeautifulSoup(responses.text, 'html.parser')
else:
   print("❌ Erreur de connexion")
   exit()

livres = soup.find_all('article', class_='product_pod')

print(f"Trouvé {len(livres)} livres\n")

liste_livres = []
for livre in livres[:10]:
    titre_tag = livre.find('h3').find('a')
    titre = titre_tag['title']

    prix = livre.find('p', class_='price_color').text

    note_tag = livre.find('p', class_='star-rating')
    note = note_tag['class'][1]

    print(f"📚 {titre}")
    print(f"   💰 Prix : {prix}")
    print(f"   ⭐ Note : {note}")
    print()

    liste_livres.append({
        'titre': titre,
        'prix': prix,
        'note': note
    })

print(f"✅ {len(liste_livres)} livres extraits !")

nom_fichier = "livres.csv"

with open(nom_fichier, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['titre', 'prix', 'note'])

    writer.writeheader()

    writer.writerows(liste_livres)

print(f"\n💾 Données sauvegardées dans {nom_fichier} !")
