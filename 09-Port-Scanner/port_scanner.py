import socket
from datetime import datetime

print("🔍 SCANNER DE PORTS AVANCÉ\n")

# Dictionnaire des ports communs et leurs services
PORTS_COMMUNS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt"
}

def scanner_port(ip, port):
    """Scanne un port sur une IP donnée"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)  # Plus rapide
        resultat = sock.connect_ex((ip, port))
        sock.close()
        
        return resultat == 0
    except:
        return False

def scanner_ip(ip, ports=None):
    """Scanne tous les ports d'une IP"""
    
    # Si pas de liste de ports, scanner les ports communs
    if ports is None:
        ports = PORTS_COMMUNS.keys()
    
    print(f"🎯 Cible : {ip}")
    print(f"📅 Début : {datetime.now().strftime('%H:%M:%S')}")
    print("="*60)
    
    ports_ouverts = []
    
    for port in ports:
        if scanner_port(ip, port):
            service = PORTS_COMMUNS.get(port, "Service inconnu")
            print(f"✅ Port {port} ({service}) : OUVERT")
            ports_ouverts.append({"port": port, "service": service})
        else:
            print(f"❌ Port {port} : FERMÉ")
    
    print("="*60)
    print(f"📊 Résumé : {len(ports_ouverts)} port(s) ouvert(s)")
    print(f"📅 Fin : {datetime.now().strftime('%H:%M:%S')}")
    
    return ports_ouverts

# Sauvegarder les scan dans un JSON

def sauvegarder_scan(ip, resultats):
    """Sauvegarde les resultats du scan en JSON"""
    import json
    import os

    fichier = "scan_historique.json" # <---- créer un fichier s'il n'existe pas encore
    if os.path.exists(fichier):
        with open(fichier, 'r') as f:
            historique = json.load(f)
    else:
        historique = []

# Ajouter le nouveau scan 

    scan_data = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip": ip,
        "ports_ouverts": resultats
        
    }

    historique.append(scan_data)

    # Sauvegarder

    with open(fichier, 'w') as f:
        json.dump(historique, f, indent=2)

    print(f"\n💾 Scan sauvegardé dans {fichier}")

def afficher_historique():
    """Affiche Historique des scans"""

    import json
    import os

    fichier = "scan_historique.json"

    if not os.path.exists(fichier):
         print("\n📭 Aucun scan dans l'historique")
         return
    
    with open(fichier, 'r') as f:
        historique = json.load(f)

    print(f"\n📊 HISTORIQUE DES SCANS ({len(historique)} scan(s))")
    print("="*60)

    for i, scan in enumerate(historique, 1):
        print(f"\n{i}.  {scan['date']} - {scan['ip']}")
        print(f".  Ports ouverts : {len(scan['ports_ouverts'])}")
        for port_info in scan['ports_ouverts']:
              print(f"      - Port {port_info['port']} : {port_info['service']}")
         
      
# Programme principal
def menu():
    """Affiche le menu"""
    print("\n" + "="*60)
    print("🔍 SCANNER DE PORTS")
    print("="*60)
    print("1. Scanner une IP")
    print("2. Voir l'historique")
    print("3. Quitter")
    print("="*60)

while True:
    menu()
    choix = input("\nTon choix : ")
    
    if choix == "1":
        ip_cible = input("\nEntre l'IP à scanner (ou 'localhost') : ")
        
        if ip_cible.lower() == "localhost":
            ip_cible = "127.0.0.1"
        
        resultats = scanner_ip(ip_cible)
        
        if resultats:
            print("\n🚨 PORTS OUVERTS DÉTECTÉS :")
            for resultat in resultats:
                print(f"   - Port {resultat['port']} : {resultat['service']}")
        else:
            print("\n✅ Aucun port ouvert détecté")
        
        # Sauvegarder
        sauvegarder_scan(ip_cible, resultats)
    
    elif choix == "2":
        afficher_historique()
    
    elif choix == "3":
        print("\n👋 À bientôt !")
        break
    
    else:
        print("\n❌ Choix invalide")