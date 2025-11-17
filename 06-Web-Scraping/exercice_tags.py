import requests
from bs4 import BeautifulSoup

print("=== EXERCICE : Scraper avec Tags ===\n")

url = "http://quotes.toscrape.com/"
responses = requests.get(url)

if responses.status_code == 200:
    print("✅ Connecté !\n")
    soup = BeautifulSoup(responses.text, 'html.parser')
else:
    print("❌ Erreur")
    exit()

# Extraire citations, auteurs et tags
citations = soup.find_all('span', class_='text')
auteurs = soup.find_all('small', class_='author')
tags_containers = soup.find_all('div', class_='tags')  # ✅ CORRIGÉ

print(f"Trouvé {len(citations)} citations\n")

# Afficher les 5 premières citations
for i in range(5):
    citation = citations[i].text
    auteur = auteurs[i].text
    
    # Extraire les tags
    conteneur = tags_containers[i]
    liste_tags = conteneur.find_all('a', class_='tag')
    
    # Extraire le texte des tags
    noms_tags = []
    for tag in liste_tags:
        noms_tags.append(tag.text)
    
    # Afficher
    print(f"{i+1}. {citation}")
    print(f"   — {auteur}")
    print(f"   🏷️ Tags : {', '.join(noms_tags)}")
    print()