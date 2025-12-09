import random
import time

print("🎯 NMAP TRAINER - Apprends Nmap en pratiquant !")
print("="*60)
print()

# PARTIE 1 : BASE DE QUESTIONS
# ============================

QUESTIONS = {
    # Niveau 1 : DÉBUTANT
    "debutant": [
        {
            "question": "Quelle commande scanne les 1000 ports les plus courants ?",
            "reponse": "nmap target",
            "alternatives": ["nmap target.com", "nmap 192.168.1.1"],
            "explication": "La commande de base 'nmap target' scanne les 1000 ports TCP les plus courants par défaut.",
            "points": 10
        },
        {
            "question": "Quelle option détecte les versions des services ?",
            "reponse": "-sV",
            "alternatives": [],
            "explication": "-sV (Version detection) envoie des requêtes spéciales aux services pour identifier leurs versions exactes.",
            "points": 10
        },
        {
            "question": "Quel port utilise le service SSH ?",
            "reponse": "22",
            "alternatives": [],
            "explication": "SSH (Secure Shell) utilise le port 22 par défaut pour les connexions à distance sécurisées.",
            "points": 10
        },
        {
            "question": "Quelle option fait un scan de TOUS les ports (1-65535) ?",
            "reponse": "-p-",
            "alternatives": ["-p 1-65535"],
            "explication": "-p- est un raccourci pour scanner tous les 65535 ports TCP. Équivalent à -p 1-65535",
            "points": 15
        },
        {
            "question": "Quel port utilise le service DNS ?",
            "reponse": "53",
            "alternatives": [],
            "explication": "DNS (Domain Name System) utilise le port 53 pour traduire les noms de domaine en adresses IP.",
            "points": 10
        }
    ],
    
    # Niveau 2 : INTERMÉDIAIRE
    "intermediaire": [
        {
            "question": "Quelle commande fait un scan agressif complet ?",
            "reponse": "nmap -A target",
            "alternatives": ["sudo nmap -A target", "nmap -A target.com"],
            "explication": "-A active : détection OS, versions, scripts NSE et traceroute. C'est TRÈS détectable !",
            "points": 20
        },
        {
            "question": "Quelle option fait un SYN scan (stealth) ?",
            "reponse": "-sS",
            "alternatives": [],
            "explication": "-sS fait un 'half-open scan' : envoie SYN, reçoit SYN-ACK, puis RST. Plus discret qu'une connexion complète.",
            "points": 20
        },
        {
            "question": "Quelle option définit le timing le plus LENT (stealth) ?",
            "reponse": "-T0",
            "alternatives": [],
            "explication": "-T0 (Paranoid) : 1 paquet toutes les 5 minutes ! Ultra lent mais très discret.",
            "points": 20
        },
        {
            "question": "Comment scanner uniquement les ports 80, 443 et 8080 ?",
            "reponse": "nmap -p 80,443,8080 target",
            "alternatives": ["nmap -p80,443,8080 target"],
            "explication": "-p 80,443,8080 scanne seulement ces 3 ports spécifiques (séparés par des virgules).",
            "points": 15
        }
    ],
    
    # Niveau 3 : AVANCÉ
    "avance": [
        {
            "question": "Comment utiliser 5 leurres aléatoires ?",
            "reponse": "nmap -D RND:5 target",
            "alternatives": ["sudo nmap -D RND:5 target", "nmap -D RND:5 target.com"],
            "explication": "-D RND:5 génère 5 IPs aléatoires comme leurres. La cible voit 6 IPs (5 faux + toi).",
            "points": 30
        },
        {
            "question": "Quelle option fragmente les paquets pour contourner les firewalls ?",
            "reponse": "-f",
            "alternatives": [],
            "explication": "-f fragmente les paquets en petits morceaux (8 bytes). Les firewalls basiques ne peuvent pas analyser.",
            "points": 30
        },
        {
            "question": "Comment spécifier le port source 53 (DNS) ?",
            "reponse": "--source-port 53",
            "alternatives": ["-g 53"],
            "explication": "--source-port 53 fait croire que le scan vient du port DNS. Certains firewalls font confiance au port 53.",
            "points": 25
        },
        {
            "question": "Quel port utilise SMB (exploité par EternalBlue) ?",
            "reponse": "445",
            "alternatives": [],
            "explication": "SMB utilise le port 445. EternalBlue (CVE-2017-0144) exploite ce service pour WannaCry.",
            "points": 20
        }
    ]
}

# PARTIE 2 : FONCTIONS DU JEU
# ============================

def afficher_score(score, total):
    """Affiche le score actuel"""
    pourcentage = (score / total * 100) if total > 0 else 0
    print(f"\n📊 Score : {score}/{total} points ({pourcentage:.1f}%)")

def poser_question(question_data, numero):
    """Pose une question et vérifie la réponse"""
    
    print(f"\n{'='*60}")
    print(f"❓ QUESTION {numero}")
    print(f"{'='*60}")
    print(f"\n{question_data['question']}")
    print(f"\n💡 Valeur : {question_data['points']} points")
    
    # Input utilisateur
    reponse_user = input("\n➤ Ta réponse : ").strip().lower()
    
    # Vérifier la réponse
    reponse_correcte = question_data['reponse'].lower()
    alternatives = [alt.lower() for alt in question_data['alternatives']]
    
    if reponse_user == reponse_correcte or reponse_user in alternatives:
        print("\n✅ CORRECT !")
        print(f"📚 Explication : {question_data['explication']}")
        return question_data['points']
    else:
        print("\n❌ INCORRECT !")
        print(f"✅ Bonne réponse : {question_data['reponse']}")
        print(f"📚 Explication : {question_data['explication']}")
        return 0

def jouer_niveau(niveau_nom, questions):
    """Joue un niveau complet"""
    
    print(f"\n{'='*60}")
    print(f"🎮 NIVEAU : {niveau_nom.upper()}")
    print(f"{'='*60}")
    print(f"📝 {len(questions)} questions")
    
    input("\n➤ Appuie sur Entrée pour commencer...")
    
    score = 0
    total_possible = sum(q['points'] for q in questions)
    
    for i, question in enumerate(questions, 1):
        points = poser_question(question, i)
        score += points
        afficher_score(score, total_possible)
        time.sleep(0.5)
    
    return score, total_possible

# PARTIE 3 : MENU PRINCIPAL
# ==========================

def menu_principal():
    """Affiche le menu et gère le jeu"""
    
    print("\n🎯 CHOISIS TON NIVEAU :\n")
    print("1. 🟢 Débutant (5 questions)")
    print("2. 🟡 Intermédiaire (4 questions)")
    print("3. 🔴 Avancé (4 questions)")
    print("4. 🏆 Tous les niveaux (13 questions)")
    print("5. ❌ Quitter")
    
    choix = input("\n➤ Ton choix (1-5) : ").strip()
    
    if choix == "1":
        score, total = jouer_niveau("Débutant", QUESTIONS["debutant"])
    elif choix == "2":
        score, total = jouer_niveau("Intermédiaire", QUESTIONS["intermediaire"])
    elif choix == "3":
        score, total = jouer_niveau("Avancé", QUESTIONS["avance"])
    elif choix == "4":
        print("\n🏆 MODE COMPLET - TOUS LES NIVEAUX !")
        score_total = 0
        points_total = 0
        
        for niveau in ["debutant", "intermediaire", "avance"]:
            s, t = jouer_niveau(niveau, QUESTIONS[niveau])
            score_total += s
            points_total += t
        
        score, total = score_total, points_total
    elif choix == "5":
        print("\n👋 À bientôt !")
        return
    else:
        print("\n❌ Choix invalide !")
        return menu_principal()
    
    # Résultat final
    print(f"\n{'='*60}")
    print("🏁 RÉSULTAT FINAL")
    print(f"{'='*60}")
    print(f"\n📊 Score : {score}/{total} points")
    
    pourcentage = (score / total * 100) if total > 0 else 0
    
    if pourcentage >= 90:
        print("🏆 EXCELLENT ! Tu maîtrises Nmap !")
    elif pourcentage >= 70:
        print("✅ BIEN ! Continue comme ça !")
    elif pourcentage >= 50:
        print("🟡 MOYEN ! Révise encore un peu !")
    else:
        print("❌ À AMÉLIORER ! Retente ta chance !")
    
    # Rejouer ?
    rejouer = input("\n➤ Rejouer ? (o/n) : ").strip().lower()
    if rejouer == "o":
        menu_principal()
    else:
        print("\n👋 À bientôt !")

# LANCER LE JEU
menu_principal()