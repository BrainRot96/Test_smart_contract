import re
import json
import os
from datetime import datetime

print("🛡️ ASSISTANT SOC - Analyse de Sécurité avec IA\n")

# PARTIE 1 : CONFIGURATION DES PATTERNS D'ATTAQUES
PATTERNS_ATTAQUES = {
# CVE spécifiques (priorité haute)
    "CVE-2021-44228 (Log4Shell)": {
        "pattern": r"\$\{jndi:(ldap|rmi|dns)://",
        "cvss": 10.0,
        "gravite": "CRITIQUE"
    },
    "CVE-2017-0144 (EternalBlue)": {
        "pattern": r"MS17-010|SMBv1.*exploit",
        "cvss": 9.3,
        "gravite": "CRITIQUE"
    },
    "CVE-2014-6271 (Shellshock)": {
        "pattern": r"\(\)\s*\{\s*:;\s*\}",
        "cvss": 9.8,
        "gravite": "CRITIQUE"
    },
    
    # Attaques génériques
    "SQL Injection": {
        "pattern": r"(union|select|insert|drop|delete).*from|('|\")\s*(or|and)\s*('|\")|--",
        "cvss": 8.5,
        "gravite": "ÉLEVÉ"
    },
    "XSS": {
        "pattern": r"<script|javascript:|onerror=|onload=|alert\(",
        "cvss": 6.1,
        "gravite": "MOYEN"
    },
    "Directory Traversal": {
        "pattern": r"\.\./|\.\.\\|/etc/passwd|/etc/shadow",
        "cvss": 7.5,
        "gravite": "ÉLEVÉ"
    },
    "Brute Force": {
        "pattern": r"failed.*password|invalid.*login",
        "cvss": 5.3,
        "gravite": "MOYEN"
    },
    "Command Injection": {
        "pattern": r";\s*(cat|ls|rm|wget|curl)\s",
        "cvss": 9.0,
        "gravite": "CRITIQUE"
    }
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
    """Analyse une ligne de log et détecte les attaques avec CVE et CVSS"""
    attaques_detectees = []
    
    # Parcourir tous patterns avec .items()
    for nom_attaque, infos in PATTERNS_ATTAQUES.items():

        # Extraire le pattern regex du dictionnaire
        pattern = infos.get("pattern", "")
        cvss = infos.get("cvss", 0.0)
        gravite = infos.get("gravite", "INCONNU")

        # Chercher le pattern dans la ligne
        if re.search(pattern, ligne, re.IGNORECASE):
            # Ajouter l'attaque avec ses infos
            attaques_detectees.append({
                "nom": nom_attaque,
                "cvss": cvss,
                "gravite": gravite
            })
        
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
                
                # Calculer le CVSS maximum (l'attaque la plus grave)
                cvss_max = max(a.get("cvss", 0) for a in attaques)
                gravite_max = max(attaques, key=lambda a: a.get("cvss", 0)).get("gravite", "INCONNU")

                alerte = {
                    "ligne": numero_ligne,
                    "ip": ip,
                    "contenu": ligne.strip(),
                    "attaques": attaques,
                    "cvss_max": cvss_max,
                    "gravite_max": gravite_max
                }
                
                alertes.append(alerte)

                # Afficher en temps réel avec couleurs selon gravité
                if cvss_max >= 9.0:
                    emoji = "🔴"
                elif cvss_max >= 7.0:
                    emoji = "🟠"
                elif cvss_max >= 4.0:
                    emoji = "🟡"
                else:
                    emoji = "🟢"
                
                print(f"\n{emoji} ALERTE Ligne {numero_ligne} - {gravite_max} (CVSS {cvss_max})")
                print(f"   IP : {ip}")

                # Afficher chaque type d'attaque
                for attaque in attaques:
                    nom = attaque.get("nom", "Inconnu")
                    cvss = attaque.get("cvss", 0)
                    print(f"   └─ {nom} (CVSS {cvss})")
                
                
    print("\n" + "="*60)
    print(f"📊 ANALYSE TERMINÉE")
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
        cvss_max = alerte.get("cvss_max", 0.0)
        gravite_max = alerte.get("gravite_max", "INCONNU")

        # Formater les attaques pour l'IA
        attaques_formattees = []
        for att in attaques:
            attaques_formattees.append({
                "nom": att.get("nom", "Inconnu"),
                "cvss": att.get("cvss", 0.0),
                "gravite": att.get("gravite", "INCONNU")
            })
        
        resume_alertes.append({
            "ligne": ligne,
            "ip": ip,
            "cvss_max": cvss_max,
            "gravite": gravite_max,
            "attaques": attaques_formattees
        })
    
    # Créer le prompt pour Claude
    prompt = f"""Tu es un expert en cybersécurité travaillant dans un SOC (Security Operations Center).

Voici les alertes de sécurité détectées dans les logs serveur :

{json.dumps(resume_alertes, indent=2, ensure_ascii=False)}

Analyse ces alertes en tenant compte des scores CVSS et fournis :

1. 📊 RÉSUMÉ : Vue d'ensemble des attaques avec focus sur les CVE critiques
2. 🎯 ATTAQUES PAR IP : Grouper par IP avec le CVSS maximum de chaque IP
3. ⚠️ PRIORISATION : Trier par urgence selon CVSS (10.0 = IMMÉDIAT, 7-9 = URGENT, 4-6 = IMPORTANT, 0-3 = SURVEILLER)
4. 💡 RECOMMANDATIONS : Actions concrètes PRIORISÉES selon les scores CVSS

Pour les CVE connus (Log4Shell, EternalBlue, etc.), explique brièvement le risque.

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

    # Créer le nom du fichier avec la date
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
    
    # Trier les alertes par CVSS (les plus graves en premier)
    alertes_triees = sorted(alertes, key=lambda a: a.get("cvss_max", 0), reverse=True)

    # Ajouter chaque alerte avec CVSS
    for i, alerte in enumerate(alertes_triees, 1):
        ligne = alerte.get("ligne", 0)
        ip = alerte.get("ip", "Inconnue")
        attaques = alerte.get("attaques", [])
        contenu = alerte.get("contenu", "")
        cvss_max = alerte.get("cvss_max", 0.0)
        gravite_max = alerte.get("gravite_max", "INCONNU")
        
        # Emoji selon gravité
        if cvss_max >= 9.0:
            emoji = "🔴"
        elif cvss_max >= 7.0:
            emoji = "🟠"
        elif cvss_max >= 4.0:
            emoji = "🟡"
        else:
            emoji = "🟢"
        
        rapport += f"""### {emoji} Alerte #{i} - {gravite_max} (CVSS {cvss_max})

- **Ligne :** {ligne}
- **IP :** {ip}
- **Gravité :** {gravite_max} (Score CVSS : {cvss_max}/10.0)
- **Attaques détectées :**
"""
        
        # Lister chaque attaque avec son CVSS
        for att in attaques:
            nom = att.get("nom", "Inconnu")
            cvss = att.get("cvss", 0.0)
            gravite = att.get("gravite", "INCONNU")
            rapport += f"  - {nom} (CVSS {cvss} - {gravite})\n"
        
        rapport += f"\n- **Log :** `{contenu[:100]}...`\n\n"

    # Sauvegarder le fichier
    with open(nom_fichier, 'w', encoding='utf-8') as f:
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