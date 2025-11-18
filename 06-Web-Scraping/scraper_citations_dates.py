import requests
from bs4 import BeautifulSoup
import csv

print("=== SCRAPER DE CITATIONS AVEC TAGS ===\n")

url = "http://quotes.toscrape.com/"
response = requests.get(url)

if response.status_code == 200:
    print("✅ Connecté !\n")
    soup = BeautifulSoup(response.text, 'html.parser')
else:
    print("❌ Erreur")
    exit()

# Extraire tous les conteneurs de citations
citations_conteneurs = soup.find_all('div', class_='quote')

print(f"Trouvé {len(citations_conteneurs)} citations\n")

# Liste pour stocker les données
liste_citations = []

# Parcourir TOUTES les citations
for i in range(10):
    conteneur = citations_conteneurs[i]
    
    citation = conteneur.find('span', class_='text').text
    auteur = conteneur.find('small', class_='author').text
    
    # Extraire les tags
    conteneur_tags = conteneur.find('div', class_='tags')
    liste_tags = conteneur_tags.find_all('a', class_='tag')
    
    # Extraire le texte de chaque tag
    noms_tags = []
    for tag in liste_tags:
        noms_tags.append(tag.text)
    
    print(f"{i+1}. {citation}")
    print(f"   — {auteur}")
    print(f"   🏷️  Tags : {', '.join(noms_tags)}\n")
    
    # Ajouter à la liste
    liste_citations.append({
        'citation': citation,
        'auteur': auteur,
        'tags': ', '.join(noms_tags)
    })

# Sauvegarder dans un fichier CSV
nom_fichier = "citations.csv"

with open(nom_fichier, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['citation', 'auteur', 'tags'])
    
    writer.writeheader()
    writer.writerows(liste_citations)

print(f"\n💾 Données sauvegardées dans {nom_fichier} !")