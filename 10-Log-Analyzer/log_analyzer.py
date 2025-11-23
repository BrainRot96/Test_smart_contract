import re
from datetime import datetime

print("🛡️ ANALYSEUR DE LOGS DE SÉCURITÉ\n")

# Patterns d'attaques à détecter
PATTERNS_ATTAQUES = {
    "SQL Injection": r"(union|select|insert|drop|delete|update).*from|('|\")\s*(or|and)\s*('|\")|--",
    "XSS": r"<script|javascript:|onerror=|onload=|alert\(|document\.",
    "Directory Traversal": r"\.\./|\.\.\\|/etc/passwd|/etc/shadow",
    "Brute Force": r"failed.*password|invalid.*login|authentication.*failed",
    "Command Injection": r";\s*(cat|ls|rm|wget|curl|bash|sh)\s|&&|\|\|"
}

def analyser_ligne(ligne):
    """Analyse une ligne de log et détecte les attaques"""

    attaques_detectees = []

    for nom_attaque, pattern in PATTERNS_ATTAQUES.items():
        if re.search(pattern, ligne, re.IGNORECASE):
            attaques_detectees.append(nom_attaque)

    return attaques_detectees

def analyser_fichier_logs(fichier):
    """Analyse un fichier de logs complet"""

    print(f"📂 Analyse de : {fichier}")
    print(f"📅 Début : {datetime.now().strftime('%H:%M:%S')}")
    print("="*60)

    alertes = []
    lignes_analysees = 0

    try:
        with open(fichier, 'r', encoding='utf-8') as f:
            for numero_ligne, ligne in enumerate(f, 1):
                lignes_analysees += 1
                attaques = analyser_ligne(ligne)

                if attaques:
                    alerte = {
                        "ligne": numero_ligne,
                        "contenu": ligne.strip(),
                        "attaques": attaques
                    }
                    alertes.append(alerte)

                    # Afficher l'alerte en temps réel
                    print(f"\n🚨 ALERTE Ligne {numero_ligne}")
                    print(f"   Type(s) : {', '.join(attaques)}")
                    print(f"   Log : {ligne.strip()[:70]}...")

    except FileNotFoundError:
           print(f"❌ Fichier non trouvé : {fichier}")
           return None
    
    print("\n" + "="*60)
    print(f"📊 RÉSUMÉ DE L'ANALYSE")
    print(f"   Lignes analysées : {lignes_analysees}")
    print(f"   Alertes : {len(alertes)}")
    print(f"📅 Fin : {datetime.now().strftime('%H:%M:%S')}")
    
    return alertes

def extraire_ip(ligne):
    """Extraire l'adresse IP d'une ligne de log"""
    match = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ligne)
    if match:
        return match.group()
    return "IP inconnue"

def generer_rapport(alertes):
    """Génère un rapport de sécurité"""
    if not alertes:
        print("\n✅ Aucune alerte - Système sécurisé")
        return
    
    print("\n" + "="*60)
    print("📋 RAPPORT DE SÉCURITÉ")
    print("="*60)

    # Compter les attaques par type

    stats_attaques = {}
    ip_suspectes = {}

    for alerte in alertes:
        #compter par type
        for attaque in alerte['attaques']:
            stats_attaques['attaque'] = stats_attaques.get(attaque, 0) + 1

        # Compter par IP 
        ip = extraire_ip(alerte['contenu'])
        ip_suspectes[ip] = ip_suspectes.get(ip, 0) + 1

    # Afficher les stats par types d'attaque 
    print("\n🚨 ATTAQUES PAR TYPE :")
    for attaque, count in sorted(stats_attaques.items(), key=lambda x: x[1], reverse=True):
           print(f"   - {attaque} : {count} occurrence(s)")

    # Afficher les IP les plus suspectes 
    print("\n🔴 IPS SUSPECTES :")
    for ip, count in sorted(ip_suspectes.items(), key=lambda x: x[1], reverse=True):
        niveau = "CRITIQUE" if count >= 5 else "ELEVE" if count >= 3 else "MOYEN"
        print(f"   - {ip} : {count} alerte(s) [{niveau}]")

    # Recommandation 
    print("\n💡 RECOMMANDATIONS :")
    if "Brute Force" in stats_attaques:
        print("     - Activer le blocage après trois tentatives échoués")
        print("     - Implémenter un CAPTCHA")
    if "SQL Injection" in stats_attaques:
        print("     - Utiliser des requêtes préparées")
        print("     - Valider et échapper les entrées utilisateur")
    if "XSS" in stats_attaques:
        print("     - Echapper les sorties HTML")
        print("     - Implémnter Content Security Policy (CSP)")
    if "Directory Traversal" in stats_attaques:
        print("     - Valider les chemins de fichiers")
        print("     - Restreindre l'accès aux répertoires sensibles")

     

    


# Programme principal :

fichier_logs = input("Fichier de logs a analyser : ")
resultats = analyser_fichier_logs(fichier_logs)

if resultats:
    generer_rapport(resultats)

    
    
    


