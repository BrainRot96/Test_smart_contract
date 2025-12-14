import requests
import json
from datetime import datetime

print("🤖 SECURITY TESTER - Test automatique des vulnérabilités")
print("="*60)

# Configuration
BASE_URL = "http://127.0.0.1:5000"

def charger_payloads():
    """Charge les payloads depuis le fichier JSON"""
    
    print("\n📂 Chargement des payloads...")
    
    try:
        with open("payloads_generated.json", "r") as f:
            data = json.load(f)
        
        sqli = data.get("sql_injection", [])
        xss = data.get("xss", [])
        path = data.get("path_traversal", [])
        
        print(f"✅ {len(sqli)} payloads SQL Injection")
        print(f"✅ {len(xss)} payloads XSS")
        print(f"✅ {len(path)} payloads Path Traversal")
        print(f"📊 Total : {len(sqli) + len(xss) + len(path)} payloads\n")
        
        return sqli, xss, path
        
    except FileNotFoundError:
        print("❌ Fichier payloads_generated.json non trouvé !")
        print("➤ Lance d'abord : python ai_payload_generator.py")
        return [], [], []

def tester_sqli(payloads):
    """Teste les payloads SQL Injection"""
    
    print("\n" + "="*60)
    print("🔍 TEST 1 : SQL INJECTION")
    print("="*60)
    
    reussites = []
    
    for i, payload_data in enumerate(payloads, 1):
        payload = payload_data.get("payload", "")
        description = payload_data.get("description", "")
        
        print(f"\n[{i}/{len(payloads)}] Test : {payload[:50]}...")
        
        try:
            # Envoyer la requête GET avec headers
            url = f"{BASE_URL}/search"
            params = {"username": payload}
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            response = requests.get(url, params=params, headers=headers, timeout=5)
            
            # Vérifier si l'injection a réussi
            if response.status_code == 200:
                # Compter les lignes de résultats
                if response.text.count("<tr>") > 2:  # Plus que le header
                    print(f"✅ RÉUSSI - Plusieurs résultats retournés")
                    reussites.append({
                        "payload": payload,
                        "description": description,
                        "type": payload_data.get("type", "unknown")
                    })
                else:
                    print(f"❌ Échec - Pas assez de résultats")
            else:
                print(f"❌ Échec - Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erreur : {e}")
    
    print(f"\n📊 Résultat : {len(reussites)}/{len(payloads)} payloads réussis")
    return reussites

def tester_xss(payloads):
    """Teste les payloads XSS"""
    
    print("\n" + "="*60)
    print("💬 TEST 2 : XSS (Cross-Site Scripting)")
    print("="*60)
    
    reussites = []
    
    for i, payload_data in enumerate(payloads, 1):
        payload = payload_data.get("payload", "")
        description = payload_data.get("description", "")
        
        print(f"\n[{i}/{len(payloads)}] Test : {payload[:50]}...")
        
        try:
            # Envoyer la requête POST avec headers
            url = f"{BASE_URL}/comment"
            data = {"comment": payload}
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            response = requests.post(url, data=data, headers=headers, timeout=5)
            
            # Vérifier si le payload est présent dans la réponse
            if response.status_code == 200:
                if payload in response.text:
                    print(f"✅ RÉUSSI - Payload injecté sans échappement")
                    reussites.append({
                        "payload": payload,
                        "description": description,
                        "type": payload_data.get("type", "unknown")
                    })
                else:
                    print(f"❌ Échec - Payload échappé ou absent")
            else:
                print(f"❌ Échec - Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erreur : {e}")
    
    print(f"\n📊 Résultat : {len(reussites)}/{len(payloads)} payloads réussis")
    return reussites

def tester_path_traversal(payloads):
    """Teste les payloads Path Traversal"""
    
    print("\n" + "="*60)
    print("📁 TEST 3 : PATH TRAVERSAL")
    print("="*60)
    
    reussites = []
    
    for i, payload_data in enumerate(payloads, 1):
        payload = payload_data.get("payload", "")
        description = payload_data.get("description", "")
        
        print(f"\n[{i}/{len(payloads)}] Test : {payload[:50]}...")
        
        try:
            # Envoyer la requête GET avec headers
            url = f"{BASE_URL}/read"
            params = {"file": payload}
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            response = requests.get(url, params=params, headers=headers, timeout=5)
            
            # Vérifier si on a accédé à un fichier
            if response.status_code == 200:
                if "root:" in response.text or "def " in response.text or len(response.text) > 100:
                    print(f"✅ RÉUSSI - Fichier lu avec succès")
                    reussites.append({
                        "payload": payload,
                        "description": description,
                        "type": payload_data.get("type", "unknown")
                    })
                else:
                    print(f"❌ Échec - Réponse vide ou erreur")
            else:
                print(f"❌ Échec - Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erreur : {e}")
    
    print(f"\n📊 Résultat : {len(reussites)}/{len(payloads)} payloads réussis")
    return reussites

def generer_rapport(sqli_reussites, xss_reussites, path_reussites):
    """Génère un rapport de sécurité complet"""
    
    print("\n" + "="*60)
    print("📋 GÉNÉRATION DU RAPPORT DE SÉCURITÉ")
    print("="*60)
    
    total_tests = len(sqli_reussites) + len(xss_reussites) + len(path_reussites)
    
    rapport = f"""
# 🛡️ RAPPORT DE SÉCURITÉ - AI Security Tester

**Date :** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Cible :** {BASE_URL}  
**Tests effectués :** {total_tests} vulnérabilités détectées

---

## 📊 RÉSUMÉ

| Vulnérabilité | Réussis |
|---------------|---------|
| **SQL Injection** | {len(sqli_reussites)} |
| **XSS** | {len(xss_reussites)} |
| **Path Traversal** | {len(path_reussites)} |

---

## 🔍 DÉTAILS

### 1. SQL INJECTION ({len(sqli_reussites)} attaques)
"""
    
    for i, vuln in enumerate(sqli_reussites, 1):
        rapport += f"\n{i}. `{vuln['payload']}` - {vuln['description']}"
    
    rapport += f"""

### 2. XSS ({len(xss_reussites)} attaques)
"""
    
    for i, vuln in enumerate(xss_reussites, 1):
        rapport += f"\n{i}. `{vuln['payload']}` - {vuln['description']}"
    
    rapport += f"""

### 3. PATH TRAVERSAL ({len(path_reussites)} attaques)
"""
    
    for i, vuln in enumerate(path_reussites, 1):
        rapport += f"\n{i}. `{vuln['payload']}` - {vuln['description']}"
    
    rapport += "\n\n**Rapport généré par AI Security Tester**"
    
    # Sauvegarder
    with open("security_report.md", "w") as f:
        f.write(rapport)
    
    print("\n✅ Rapport généré : security_report.md")
    print(f"\n📊 RÉSUMÉ :")
    print(f"   🔴 SQL Injection : {len(sqli_reussites)} vulnérabilités")
    print(f"   🔴 XSS : {len(xss_reussites)} vulnérabilités")
    print(f"   🔴 Path Traversal : {len(path_reussites)} vulnérabilités")

# PROGRAMME PRINCIPAL
if __name__ == "__main__":
    
    sqli_payloads, xss_payloads, path_payloads = charger_payloads()
    
    if not sqli_payloads and not xss_payloads and not path_payloads:
        print("\n❌ Aucun payload à tester !")
        exit(1)
    
    print("🔍 Vérification de l'application cible...")
    try:
        response = requests.get(BASE_URL, timeout=5)
        print(f"✅ Application accessible ({BASE_URL})\n")
    except:
        print(f"❌ Application non accessible !")
        print(f"➤ Lance d'abord : python vulnerable_app.py")
        exit(1)
    
    sqli_reussites = tester_sqli(sqli_payloads)
    xss_reussites = tester_xss(xss_payloads)
    path_reussites = tester_path_traversal(path_payloads)
    
    generer_rapport(sqli_reussites, xss_reussites, path_reussites)
    
    print("\n" + "="*60)
    print("✅ TESTS TERMINÉS !")
    print("="*60)
