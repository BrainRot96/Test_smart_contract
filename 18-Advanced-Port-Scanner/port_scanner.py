#!/usr/bin/env python3
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from service_detector import detect_service, get_port_list
from banner_grabber import grab_banner, parse_banner
from report_generator import save_report

print("🔍 ADVANCED PORT SCANNER")
print("="*60)
print()

def scan_port(ip, port, timeout=2, grab_banners=True):
    """
    Scanne un port spécifique
    
    Args:
        ip: Adresse IP cible
        port: Port à scanner
        timeout: Timeout en secondes
        grab_banners: Récupérer les bannières
    
    Returns:
        dict: Résultat du scan
    """
    
    # Détecter si le port est ouvert
    result = detect_service(ip, port, timeout)
    result["port"] = port
    
    # Si ouvert, récupérer la bannière
    if result["status"] == "open" and grab_banners:
        banner = grab_banner(ip, port, timeout)
        result["banner"] = banner
        result["banner_info"] = parse_banner(banner)
    else:
        result["banner"] = None
        result["banner_info"] = {}
    
    return result

def scan_host(target, ports, max_threads=100, timeout=2, grab_banners=True, verbose=True):
    """
    Scanne un hôte avec plusieurs ports
    
    Args:
        target: IP ou hostname
        ports: Liste de ports à scanner
        max_threads: Nombre de threads simultanés
        timeout: Timeout par port
        grab_banners: Récupérer les bannières
        verbose: Afficher les résultats en temps réel
    
    Returns:
        list: Liste des résultats
    """
    
    print(f"🎯 Target: {target}")
    print(f"📋 Ports to scan: {len(ports)}")
    print(f"⚡ Threads: {max_threads}")
    print(f"⏱️  Timeout: {timeout}s")
    print(f"🏷️  Banner grabbing: {'Enabled' if grab_banners else 'Disabled'}")
    print()
    print("🚀 Starting scan...")
    print()
    
    results = []
    start_time = time.time()
    
    # Résoudre le hostname si nécessaire
    try:
        ip = socket.gethostbyname(target)
        if ip != target:
            print(f"✅ Resolved {target} → {ip}\n")
    except:
        print(f"❌ Could not resolve {target}")
        return []
    
    # Scanner avec multi-threading
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Soumettre tous les scans
        future_to_port = {
            executor.submit(scan_port, ip, port, timeout, grab_banners): port 
            for port in ports
        }
        
        # Afficher progression
        completed = 0
        total = len(ports)
        
        for future in as_completed(future_to_port):
            port = future_to_port[future]
            completed += 1
            
            try:
                result = future.result()
                results.append(result)
                
                # Afficher seulement les ports ouverts si verbose
                if verbose and result["status"] == "open":
                    banner_info = result.get("banner_info", {})
                    service = result.get("service", "Unknown")
                    banner_service = banner_info.get("service", "")
                    version = banner_info.get("version", "")
                    
                    info_str = f"{service}"
                    if banner_service and banner_service != "Unknown":
                        info_str += f" ({banner_service}"
                        if version and version != "Unknown":
                            info_str += f" {version}"
                        info_str += ")"
                    
                    print(f"✅ Port {port:5d} - OPEN  - {info_str}")
            
            except Exception as e:
                if verbose:
                    print(f"❌ Port {port:5d} - ERROR - {e}")
            
            # Afficher progression tous les 10%
            if completed % max(1, total // 10) == 0:
                percent = (completed / total) * 100
                print(f"⏳ Progress: {completed}/{total} ({percent:.1f}%)")
    
    # Fin du scan
    scan_duration = time.time() - start_time
    
    print()
    print("="*60)
    print("✅ SCAN COMPLETE")
    print("="*60)
    print(f"⏱️  Duration: {scan_duration:.2f} seconds")
    print(f"📊 Ports scanned: {len(results)}")
    print(f"🔓 Open ports: {len([r for r in results if r['status'] == 'open'])}")
    print(f"🔒 Closed ports: {len([r for r in results if r['status'] == 'closed'])}")
    print(f"🛡️  Filtered ports: {len([r for r in results if r['status'] == 'filtered'])}")
    print()
    
    return results, scan_duration

def main():
    """Programme principal"""
    
    print("🎯 CONFIGURATION DU SCAN")
    print("="*60)
    print()
    
    # Configuration
    target = input("➤ Target (IP or hostname): ").strip()
    
    if not target:
        print("❌ Target required!")
        return
    
    print("\n📋 SCAN MODE:")
    print("1. 🟢 Fast (Top 20 ports)")
    print("2. 🟡 Normal (Top 100 ports)")
    print("3. 🔴 Full (All 65535 ports)")
    print("4. 🔵 Custom (ex: 80,443,8080 or 1-1000)")
    
    mode = input("\n➤ Choose mode (1-4): ").strip()
    
    if mode == "1":
        ports = get_port_list("top20")
        mode_name = "Fast"
    elif mode == "2":
        ports = get_port_list("top100")
        mode_name = "Normal"
    elif mode == "3":
        confirm = input("⚠️  Full scan takes VERY long! Continue? (y/n): ")
        if confirm.lower() != 'y':
            print("❌ Scan cancelled")
            return
        ports = get_port_list("all")
        mode_name = "Full"
    elif mode == "4":
        custom = input("➤ Enter ports (ex: 80,443,8080 or 1-1000): ").strip()
        ports = get_port_list(custom)
        mode_name = "Custom"
    else:
        print("❌ Invalid mode! Using Fast mode.")
        ports = get_port_list("top20")
        mode_name = "Fast"
    
    # Options avancées
    grab_banners = input("\n➤ Grab banners? (y/n, default=y): ").strip().lower() != 'n'
    
    threads = input("➤ Threads (default=100): ").strip()
    threads = int(threads) if threads.isdigit() else 100
    
    timeout = input("➤ Timeout per port in seconds (default=2): ").strip()
    timeout = float(timeout) if timeout else 2.0
    
    print()
    print("="*60)
    print()
    
    # Lancer le scan
    results, scan_duration = scan_host(
        target=target,
        ports=ports,
        max_threads=threads,
        timeout=timeout,
        grab_banners=grab_banners,
        verbose=True
    )
    
    # Sauvegarder les rapports
    if results:
        print("💾 SAVING REPORTS...")
        print()
        save_report(results, target, scan_duration, format="all")
        print()
        print("✅ All reports saved!")
    
    print()
    print("👋 Thank you for using Advanced Port Scanner!")

if __name__ == "__main__":
    main()