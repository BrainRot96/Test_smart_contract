import socket
import json
import os

print("🖥️  GESTIONNAIRE DE SERVEURS RÉSEAU\n")

# Base de données de serveurs (dictionnaire)
serveurs = {
    "web-prod": {
        "ip": "scanme.nmap.org",
        "ports": [22, 80, 443],
        "type": "Web Server"
    },  
    "localhost": {
        "ip": "127.0.0.1",
        "ports": [22, 80, 443, 3306],
        "type": "Local Dev"
    }  
}

def scanner_port(ip, port):  
    """Scanne un port"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        resultat = sock.connect_ex((ip, port))
        sock.close()
        return resultat == 0
    except:
        return False 
    
def obtenir_info_serveur(nom_serveur):
    """Obtient les informations d'un serveur de manière sécurisée"""
    
    serveur = serveurs.get(nom_serveur, None)
    
    if serveur is None:
        print(f"❌ Serveur '{nom_serveur}' non trouvé")
        return None
    
    ip = serveur.get("ip", "Inconnue")  
    ports = serveur.get("ports", []) 
    serveur_type = serveur.get("type", "Type inconnu")  
    
    print(f"\n📋 Infos du serveur : {nom_serveur}")
    print(f"   IP : {ip}")
    print(f"   Type : {serveur_type}")  
    print(f"   Ports à surveiller : {ports}")
    
    return serveur

def lister_tous_serveurs():
    """Liste tous les serveurs avec .items()"""

    print("\n" + "="*60)
    print("📋 LISTE DE TOUS LES SERVEURS")
    print("="*60)

    if len(serveurs) == 0:
        print("📭 Aucun serveur enregistré")
        return
    
    for nom, infos in serveurs.items():
        ip = infos.get("ip", "Inconnue")
        serveur_type = infos.get("type", "Type inconnu")
        nb_ports = len(infos.get("ports", []))

        print(f"\n🖥️  {nom}")
        print(f"   IP : {ip}")
        print(f"   Type : {serveur_type}")
        print(f"   Ports surveillés : {nb_ports}")


def scanner_serveur(nom_serveur):
    """Scanne tous les ports d'un serveur"""
    
    print("\n" + "="*60)
    print(f"🔍 SCAN DU SERVEUR : {nom_serveur}")
    print("="*60)
    
    # Récupérer le serveur avec .get()
    serveur = serveurs.get(nom_serveur, None)
    
    if serveur is None:
        print(f"❌ Serveur '{nom_serveur}' non trouvé")
        return
    
    ip = serveur.get("ip", "")
    ports = serveur.get("ports", [])
    
    if not ip:
        print("❌ Pas d'IP configurée")
        return
    
    print(f"Cible : {ip}")
    print(f"Ports à scanner : {ports}\n")
    
    ports_ouverts = 0
    ports_fermes = 0
    
    # Scanner chaque port
    for port in ports:
        if scanner_port(ip, port):
            print(f"✅ Port {port} : OUVERT")
            ports_ouverts += 1
        else:
            print(f"❌ Port {port} : FERMÉ")
            ports_fermes += 1
    
    print("\n" + "="*60)
    print(f"📊 Résultat : {ports_ouverts} ouvert(s), {ports_fermes} fermé(s)")
    print("="*60)

def afficher_statistiques():
    """Affiche des statistiques globales"""
    
    print("\n" + "="*60)
    print("📊 STATISTIQUES GLOBALES")
    print("="*60)
    
    total_serveurs = len(serveurs)
    total_ports = 0
    types_serveurs = {}
    
    # Parcourir tous les serveurs avec .items()
    for nom, infos in serveurs.items():
        # Compter les ports
        ports = infos.get("ports", [])
        total_ports += len(ports)
        
        # Compter les types de serveurs
        server_type = infos.get("type", "Inconnu")
        types_serveurs[server_type] = types_serveurs.get(server_type, 0) + 1
    
    print(f"\n🖥️  Serveurs enregistrés : {total_serveurs}")
    print(f"🔌 Ports surveillés au total : {total_ports}")
    
    print("\n📋 Serveurs par type :")
    for type_serveur, count in types_serveurs.items():
        print(f"   - {type_serveur} : {count}")



# Tests
obtenir_info_serveur("web-prod")
obtenir_info_serveur("serveur-inexistant")

lister_tous_serveurs()

scanner_serveur("web-prod")

afficher_statistiques()

