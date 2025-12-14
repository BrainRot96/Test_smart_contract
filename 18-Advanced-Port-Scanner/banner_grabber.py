import socket

def grab_banner(ip, port, timeout=2):
    """
    Récupère la bannière d'un service
    
    Args:
        ip: Adresse IP cible
        port: Port à tester
        timeout: Timeout en secondes
    
    Returns:
        str: Bannière du service ou None
    """
    
    try:
        # Créer un socket TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        # Connexion
        sock.connect((ip, port))
        
        # Certains services envoient la bannière automatiquement
        try:
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            if banner:
                return banner
        except:
            pass
        
        # D'autres nécessitent une requête
        # Essayer différentes requêtes selon le port
        if port == 80 or port == 8080:
            # HTTP
            sock.send(b"GET / HTTP/1.1\r\nHost: target\r\n\r\n")
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            # Extraire la première ligne (Server: ...)
            for line in banner.split('\n'):
                if 'Server:' in line or 'HTTP' in line:
                    return line.strip()
        
        elif port == 21:
            # FTP envoie automatiquement
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            return banner
        
        elif port == 22:
            # SSH envoie automatiquement
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            return banner
        
        elif port == 25:
            # SMTP
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            return banner
        
        else:
            # Tentative générique
            try:
                sock.send(b"\r\n")
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                if banner:
                    return banner
            except:
                pass
        
        sock.close()
        return None
        
    except socket.timeout:
        return None
    except ConnectionRefusedError:
        return None
    except Exception as e:
        return None

def parse_banner(banner):
    """
    Parse une bannière pour extraire des infos
    
    Args:
        banner: Bannière brute
    
    Returns:
        dict: Infos extraites (service, version)
    """
    
    if not banner:
        return {"service": "Unknown", "version": "Unknown"}
    
    info = {
        "service": "Unknown",
        "version": "Unknown",
        "raw": banner[:100]  # Limiter à 100 chars
    }
    
    banner_lower = banner.lower()
    
    # Détection Apache
    if 'apache' in banner_lower:
        info["service"] = "Apache"
        # Extraire version
        if 'apache/' in banner_lower:
            try:
                version = banner.split('Apache/')[1].split()[0]
                info["version"] = version
            except:
                pass
    
    # Détection nginx
    elif 'nginx' in banner_lower:
        info["service"] = "nginx"
        if 'nginx/' in banner_lower:
            try:
                version = banner.split('nginx/')[1].split()[0]
                info["version"] = version
            except:
                pass
    
    # Détection OpenSSH
    elif 'openssh' in banner_lower or 'ssh-' in banner_lower:
        info["service"] = "OpenSSH"
        if 'openssh_' in banner_lower:
            try:
                version = banner.split('OpenSSH_')[1].split()[0]
                info["version"] = version
            except:
                pass
    
    # Détection FTP
    elif 'ftp' in banner_lower:
        info["service"] = "FTP"
        # vsftpd, ProFTPD, etc.
        if 'vsftpd' in banner_lower:
            info["service"] = "vsftpd"
        elif 'proftpd' in banner_lower:
            info["service"] = "ProFTPD"
    
    # Détection MySQL
    elif 'mysql' in banner_lower:
        info["service"] = "MySQL"
    
    # Détection PostgreSQL
    elif 'postgresql' in banner_lower:
        info["service"] = "PostgreSQL"
    
    # Détection Microsoft IIS
    elif 'microsoft-iis' in banner_lower or 'iis/' in banner_lower:
        info["service"] = "Microsoft-IIS"
    
    return info