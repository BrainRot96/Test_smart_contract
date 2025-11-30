import re
import json
import os
from datetime import datetime

print("🛡️ ASSISTANT SOC - Analyse de Sécurité avec IA\n")

# PARTIE 1 : CONFIGURATION DES PATTERNS D'ATTAQUES
PATTERNS_ATTAQUES = {
    "SQL Injection": r"(union|select|insert|drop|delete).*from|('|\")\s*(or|and)\s*('|\")|--",
    "XSS": r"<script|javascript:|onerror=|onload=|alert\(",
    "Directory Traversal": r"\.\./|\.\.\\|/etc/passwd|/etc/shadow",
    "Brute Force": r"failed.*password|invalid.*login",
    "Command Injection": r";\s*(cat|ls|rm|wget|curl)\s"
}

print("✅ Patterns d'attaques chargés")
print(f"   Types d'attaques surveillées : {len(PATTERNS_ATTAQUES)}")

print("\n📋 Types d'attaques détectables :")
for nom_attaque, pattern in PATTERNS_ATTAQUES.items():
    print(f"   - {nom_attaque}")

# PARTIE 2 : FONCTIONS D'ANALYSE DES LOGS

def extraire_ip(ligne):
    """Extrait l'adresse IP d'une ligne de log"""
    pattern_ip = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    match = re.search(pattern_ip, ligne)
    
    if match:
        return match.group()
    else:
        return "IP inconnue"

def analyser_ligne(ligne):
    """Analyse une ligne de log et détecte les attaques"""
    attaques_detectees = []
    
    for nom_attaque, pattern in PATTERNS_ATTAQUES.items():
        if re.search(pattern, ligne, re.IGNORECASE):
            attaques_detectees.append(nom_attaque)
    
    return attaques_detectees

def analyser_fichier_logs(fichier):
    """Analyse un fichier de logs complet"""
    
    print(f"\n📂 Analyse du fichier : {fichier}")
    print("="*60)
    
    if not os.path.exists(fichier):
        print(f"❌ Fichier '{fichier}' non trouvé")
        return None
    
    alertes = []
    lignes_analysees = 0
    
    with open(fichier, 'r', encoding='utf-8') as f:
        for numero_ligne, ligne in enumerate(f, 1):
            lignes_analysees += 1
            
            attaques = analyser_ligne(ligne)
            
            if attaques:
                ip = extraire_ip(ligne)
                
                alerte = {
                    "ligne": numero_ligne,
                    "ip": ip,
                    "contenu": ligne.strip(),
                    "attaques": attaques
                }
                
                alertes.append(alerte)
                
                print(f"\n🚨 ALERTE Ligne {numero_ligne}")
                print(f"   IP : {ip}")
                print(f"   Type(s) : {', '.join(attaques)}")
                print(f"   Log : {ligne.strip()[:70]}...")
    
    print("\n" + "="*60)
    print(f"📊 ANALYSE TERMINÉE")
    print(f"   Lignes analysées : {lignes_analysees}")
    print(f"   Alertes détectées : {len(alertes)}")
    print("="*60)
    
    return alertes

# PARTIE 3 : ANALYSE INTELLIGENTE AVEC CLAUDE IA

def analyser_avec_ia(alertes):
    """Demande à Claude IA d'analyser les alertes"""
    
    print("\n🤖 Analyse intelligente avec Claude IA...")
    print("="*60)
    
    from anthropic import Anthropic
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")

    print(f"DEBUG - Clé API trouvée : {api_key[:20] if api_key else 'AUCUNE'}...")

    
    if not api_key:
        print("❌ Clé API non trouvée dans .env")
        return
    
    client = Anthropic(api_key=api_key)
    
    # Préparer le résumé des alertes pour Claude
    resume_alertes = []
    
    for alerte in alertes:
        ip = alerte.get("ip", "Inconnue")
        attaques = alerte.get("attaques", [])
        ligne = alerte.get("ligne", 0)
        
        resume_alertes.append({
            "ligne": ligne,
            "ip": ip,
            "types": attaques
        })
    
    # Créer le prompt pour Claude
    prompt = f"""Tu es un expert en cybersécurité travaillant dans un SOC (Security Operations Center).

Voici les alertes de sécurité détectées dans les logs serveur :

{json.dumps(resume_alertes, indent=2, ensure_ascii=False)}

Analyse ces alertes et fournis :

1. 📊 RÉSUMÉ : Vue d'ensemble des attaques
2. 🎯 ATTAQUES PAR IP : Grouper les attaques par adresse IP suspecte
3. ⚠️ NIVEAU DE RISQUE : Évaluer la gravité (CRITIQUE/ÉLEVÉ/MOYEN)
4. 💡 RECOMMANDATIONS : Actions concrètes à prendre immédiatement

Sois concis et précis. Format en texte clair avec des émojis."""

    # Appeler l'API Claude
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Afficher la réponse de Claude
        reponse_ia = message.content[0].text
        print(reponse_ia)
        
        return reponse_ia
        
    except Exception as e:
        print(f"❌ Erreur API : {e}")
        return None
    
# PARTIE 4 : SAUVEGARDE DU RAPPORT
# =================================

def sauvegarder_rapport(reponse_ia, alertes):
    """Sauvegarde le rapport d'analyse dans un fichier Markdown"""

    # Créer el nom du fichier avec la date
    date_rapport = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nom_fichier = f"rapport_soc_{date_rapport}.md"

    print(f"\n💾 Sauvegarde du rapport...")

    # Contenu du rapport 
    rapport = f"""# 🛡️ RAPPORT D'ANALYSE SOC
**Date :** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---
## 📊 STATISTIQUES

- **Alertes détectées :** {len(alertes)}
- **IPs suspectes :** {len(set(a.get('ip', 'Inconnue') for a in alertes))}

---

## 🤖 ANALYSE INTELLIGENTE

{reponse_ia}

---

## 📋 DÉTAILS DES ALERTES

"""
    
    # Ajouter chaque alerte 
    for i, alerte in enumerate(alertes, 1):
        ligne = alerte.get("ligne", 0)
        ip = alerte.get("ip", "Inconnue")
        attaques = alerte.get("attaques", [])
        contenu = alerte.get("contenu", "")

        rapport += f"""### Alerte #{i}
- **Ligne :** {ligne}
- **IP :** {ip}
- **Types :** {', '.join(attaques)}
- **Log :** `{contenu[:100]}...`

"""
        #Sauvegarder le fichier
        with open(nom_fichier, 'w', encoding='utf_8') as f:
            f.write(rapport)

        print(f"✅ Rapport sauvegardé : {nom_fichier}")

        return nom_fichier



# PROGRAMME PRINCIPAL - TEST
chemin_fichier = os.path.join(os.path.dirname(__file__), "server_logs.txt")
alertes = analyser_fichier_logs(chemin_fichier)

# Analyse avec IA
if alertes:
    reponse_ia = analyser_avec_ia(alertes)

    # Sauvegarder le rapport
    if reponse_ia:
        sauvegarder_rapport(reponse_ia, alertes)