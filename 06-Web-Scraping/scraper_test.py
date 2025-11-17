import requests
from bs4 import BeautifulSoup

print("=== WEB SCRAPER - Citations Inspirantes ===\n")

# 1. Site à scraper
url = "http://quotes.toscrape.com/"
print(f"Connexion à {url}...")

response = requests.get(url)

# 2. Vérifier que ça a marché
if response.status_code == 200:
    print("✅ Connexion réussie !\n")
else:
    print("❌ Erreur de connexion")
    exit()

# 3. Parser le HTML
soup = BeautifulSoup(response.text, 'html.parser')

# 4. Extraire les citations, auteurs ET tags
citations = soup.find_all('span', class_='text')
auteurs = soup.find_all('small', class_='author')
tags_containers = soup.find_all('div', class_='tags')

print(f"💬 {len(citations)} citations trouvées :\n")

# 5. Afficher les citations avec leurs auteurs ET tags
for i in range(min(10, len(citations))):
    citation = citations[i].text
    auteur = auteurs[i].text
    
    # Extraire les tags de cette citation
    tags_de_cette_citation = tags_containers[i].find_all('a', class_='tag')
    
    # Créer une liste des noms de tags
    noms_tags = [tag.text for tag in tags_de_cette_citation]
    
    print(f"{i+1}. {citation}")
    print(f"   — {auteur}")
    print(f"   🏷️  Tags : {', '.join(noms_tags)}\n")

print("✅ Scraping terminé !")
