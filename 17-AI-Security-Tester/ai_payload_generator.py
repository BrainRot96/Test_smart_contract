import anthropic
import os
import json

print("🤖 AI PAYLOAD GENERATOR")
print("Génération automatique de payloads d'attaque avec Claude\n")

# Configuration de l'API Claude
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

def generer_payloads_sqli(nombre=10):
    """Génère des payloads SQL Injection avec Claude"""
    
    print(f"🔍 Génération de {nombre} payloads SQL Injection...")
    
    prompt = f"""Tu es un expert en cybersécurité qui teste des applications.

Génère {nombre} payloads SQL Injection variés pour tester une application vulnérable.
Les payloads doivent être réalistes et divers (union, boolean-based, time-based, etc.).

Réponds UNIQUEMENT avec un JSON valide dans ce format :
{{
  "payloads": [
    {{"payload": "' OR '1'='1", "type": "boolean-based", "description": "Contournement authentification"}},
    {{"payload": "admin'--", "type": "comment", "description": "Commentaire SQL"}},
    ...
  ]
}}

IMPORTANT : Réponds SEULEMENT avec le JSON, pas de texte avant ou après."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extraire le contenu
        response_text = message.content[0].text.strip()
        
        # Nettoyer : chercher le JSON entre { et }
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        
        if start != -1 and end > start:
            json_text = response_text[start:end]
        else:
            json_text = response_text
        
        # Parser le JSON
        data = json.loads(json_text)
        payloads = data.get("payloads", [])
        
        print(f"✅ {len(payloads)} payloads SQL Injection générés !\n")
        
        return payloads
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        print(f"Réponse brute : {response_text[:200]}...")
        return []

def generer_payloads_xss(nombre=10):
    """Génère des payloads XSS avec Claude"""
    
    print(f"🔍 Génération de {nombre} payloads XSS...")
    
    prompt = f"""Tu es un expert en cybersécurité qui teste des applications.

Génère {nombre} payloads XSS (Cross-Site Scripting) variés pour tester une application vulnérable.
Les payloads doivent être réalistes et divers (reflected, stored, DOM-based, etc.).

Réponds UNIQUEMENT avec un JSON valide dans ce format :
{{
  "payloads": [
    {{"payload": "<script>alert('XSS')</script>", "type": "basic", "description": "Alert box classique"}},
    {{"payload": "<img src=x onerror=alert(1)>", "type": "img-onerror", "description": "Image avec onerror"}},
    ...
  ]
}}

IMPORTANT : Réponds SEULEMENT avec le JSON, pas de texte avant ou après."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extraire le contenu
        response_text = message.content[0].text.strip()
        
        # Nettoyer : chercher le JSON entre { et }
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        
        if start != -1 and end > start:
            json_text = response_text[start:end]
        else:
            json_text = response_text
        
        # Parser le JSON
        data = json.loads(json_text)
        payloads = data.get("payloads", [])
        
        print(f"✅ {len(payloads)} payloads XSS générés !\n")
        
        return payloads
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        print(f"Réponse brute : {response_text[:200]}...")
        return []

def generer_payloads_path_traversal(nombre=10):
    """Génère des payloads Path Traversal avec Claude"""
    
    print(f"🔍 Génération de {nombre} payloads Path Traversal...")
    
    prompt = f"""Tu es un expert en cybersécurité qui teste des applications.

Génère {nombre} payloads Path Traversal variés pour tester une application vulnérable.
Les payloads doivent cibler des fichiers sensibles sur différents systèmes (Linux, Windows, Mac).

Réponds UNIQUEMENT avec un JSON valide dans ce format :
{{
  "payloads": [
    {{"payload": "../../../etc/passwd", "type": "linux", "description": "Fichier passwd Linux"}},
    {{"payload": "..\\\\..\\\\..\\\\windows\\\\system32\\\\config\\\\sam", "type": "windows", "description": "SAM Windows"}},
    ...
  ]
}}

IMPORTANT : Réponds SEULEMENT avec le JSON, pas de texte avant ou après."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extraire le contenu
        response_text = message.content[0].text.strip()
        
        # Nettoyer : chercher le JSON entre { et }
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        
        if start != -1 and end > start:
            json_text = response_text[start:end]
        else:
            json_text = response_text
        
        # Parser le JSON
        data = json.loads(json_text)
        payloads = data.get("payloads", [])
        
        print(f"✅ {len(payloads)} payloads Path Traversal générés !\n")
        
        return payloads
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        print(f"Réponse brute : {response_text[:200]}...")
        return []

def sauvegarder_payloads(sqli, xss, path):
    """Sauvegarde tous les payloads dans un fichier JSON"""
    
    data = {
        "sql_injection": sqli,
        "xss": xss,
        "path_traversal": path
    }
    
    with open("payloads_generated.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"💾 Payloads sauvegardés dans payloads_generated.json")

# PROGRAMME PRINCIPAL
if __name__ == "__main__":
    
    print("="*60)
    print("🎯 Génération automatique de payloads d'attaque")
    print("="*60)
    print()
    
    # Vérifier la clé API
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ ERREUR : Variable ANTHROPIC_API_KEY non définie !")
        print("➤ Export ta clé API : export ANTHROPIC_API_KEY='ta-clé'")
        exit(1)
    
    # Générer les payloads
    sqli_payloads = generer_payloads_sqli(10)
    xss_payloads = generer_payloads_xss(10)
    path_payloads = generer_payloads_path_traversal(10)
    
    # Afficher quelques exemples
    print("\n" + "="*60)
    print("📋 EXEMPLES DE PAYLOADS GÉNÉRÉS")
    print("="*60)
    
    if sqli_payloads:
        print(f"\n🔍 SQL Injection (3 premiers) :")
        for p in sqli_payloads[:3]:
            print(f"  • {p['payload']} - {p['description']}")
    
    if xss_payloads:
        print(f"\n💬 XSS (3 premiers) :")
        for p in xss_payloads[:3]:
            print(f"  • {p['payload']} - {p['description']}")
    
    if path_payloads:
        print(f"\n📁 Path Traversal (3 premiers) :")
        for p in path_payloads[:3]:
            print(f"  • {p['payload']} - {p['description']}")
    
    # Sauvegarder
    sauvegarder_payloads(sqli_payloads, xss_payloads, path_payloads)
    
    print("\n✅ Génération terminée !")
    print(f"📊 Total : {len(sqli_payloads) + len(xss_payloads) + len(path_payloads)} payloads")