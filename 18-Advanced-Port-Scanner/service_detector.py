import socket
import json

def load_port_database():
    """Charge la base de données des ports"""
    try:
        with open("common_ports.json", "r") as f:
            return json.load(f)
    except:
        return {"top_20": [], "top_100": [], "all_ports": {"start": 1, "end": 65535}}

def get_service_name(port):
    """
    Retourne le nom du service pour un port donné
    
    Args:
        port: Numéro de port
    
    Returns:
        str: Nom du service ou "Unknown"
    """
    
    db = load_port_database()
    
    # Chercher dans top_20
    for item in db["top_20"]:
        if item["port"] == port:
            return item["service"]
    
    # Services communs non listés dans top_20
    common_services = {
        20: "FTP-Data",
        69: "TFTP",
        123: "NTP",
        161: "SNMP",
        389: "LDAP",
        636: "LDAPS",
        1433: "MS-SQL",
        1521: "Oracle",
        2082: "cPanel",
        2083: "cPanel-SSL",
        2086: "WHM",
        2087: "WHM-SSL",
        3000: "Node.js",
        5001: "Synology",
        5432: "PostgreSQL",
        5555: "Personal Web Server",
        6379: "Redis",
        8000: "HTTP-Alt",
        8008: "HTTP-Alt",
        8081: "HTTP-Alt",
        8888: "HTTP-Alt",
        9000: "SonarQube",
        9200: "Elasticsearch",
        27017: "MongoDB",
        50000: "SAP"
    }
    
    if port in common_services:
        return common_services[port]
    
    return "Unknown"

def detect_service(ip, port, timeout=2):
    """
    Détecte si un port est ouvert
    
    Args:
        ip: Adresse IP cible
        port: Port à tester
        timeout: Timeout en secondes
    
    Returns:
        dict: {"status": "open/closed/filtered", "service": "nom"}
    """
    
    try:
        # TCP Scan
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        result = sock.connect_ex((ip, port))
        sock.close()
        
        if result == 0:
            # Port ouvert
            return {
                "status": "open",
                "service": get_service_name(port)
            }
        else:
            # Port fermé
            return {
                "status": "closed",
                "service": get_service_name(port)
            }
    
    except socket.timeout:
        # Filtré (firewall)
        return {
            "status": "filtered",
            "service": get_service_name(port)
        }
    
    except Exception as e:
        return {
            "status": "error",
            "service": get_service_name(port),
            "error": str(e)
        }

def get_port_list(mode="top20"):
    """
    Retourne la liste des ports à scanner selon le mode
    
    Args:
        mode: "top20", "top100", ou "all"
    
    Returns:
        list: Liste de ports
    """
    
    db = load_port_database()
    
    if mode == "top20":
        return [item["port"] for item in db["top_20"]]
    
    elif mode == "top100":
        return db["top_100"]
    
    elif mode == "all":
        # Retourner range 1-65535 (attention: très long!)
        return list(range(1, 65536))
    
    else:
        # Mode custom: liste de ports
        try:
            # Si c'est une string "80,443,8080"
            if isinstance(mode, str) and ',' in mode:
                return [int(p.strip()) for p in mode.split(',')]
            # Si c'est une range "1-1000"
            elif isinstance(mode, str) and '-' in mode:
                start, end = mode.split('-')
                return list(range(int(start), int(end) + 1))
            # Si c'est un seul port
            else:
                return [int(mode)]
        except:
            # Par défaut: top20
            return [item["port"] for item in db["top_20"]]