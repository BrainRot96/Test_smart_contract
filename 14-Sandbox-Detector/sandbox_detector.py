import psutil
import platform
import socket
import time
from datetime import datetime

print("🔍 SANDBOX DETECTOR - Détection d'environnement virtuel\n")

# PARTIE 1 : DÉTECTION DES RESSOURCES SYSTÈME
# ============================================

def detecter_ressources():
    """Détecte si les ressources système sont suspectes (sandbox)"""

    print("📊 Analyse des ressources système...")
    print("="*60)

    score_sandbox = 0
    indices = []

    # 1. RAM
    ram_gb = psutil.virtual_memory().total / (1024**3)
    print(f"💾 RAM : {ram_gb:.2f} GB")

    if ram_gb < 4:
        score_sandbox += 20
        indices.append(f"⚠️ RAM faible ({ram_gb:.2f} GB) - Typique d'une sandbox")
    elif ram_gb < 8:
        score_sandbox += 10
        indices.append(f"⚠️ RAM modérée ({ram_gb:.2f} GB) - Possible sandbox")
    else:
        print("    ✅ RAM normale pour un vrai PC")
    
    # 2. CPU
    cpu_count = psutil.cpu_count(logical=False)
    cpu_logical = psutil.cpu_count(logical=True)
    print(f"⚙️  CPU : {cpu_count} cœurs physiques, {cpu_logical} threads")

    if cpu_count < 2:
        score_sandbox += 20
        indices.append(f"⚠️ Peu de CPUs ({cpu_count}) - Typique sandbox")
    elif cpu_count < 4:
        score_sandbox += 10
        indices.append(f"⚠️ CPUs limités ({cpu_count}) - Possible sandbox")
    else:
        print("   ✅ CPUs normaux pour un vrai PC")

    # 3. Disque
    disk_gb = psutil.disk_usage('/').total / (1024**3)
    print(f"💿 Disque : {disk_gb:.2f} GB")

    if disk_gb < 50:
        score_sandbox += 20
        indices.append(f"⚠️ Disque petit ({disk_gb:.2f} GB) - Sandbox probable")
    elif disk_gb < 100:
        score_sandbox += 10
        indices.append(f"⚠️ Disque limité ({disk_gb:.2f} GB) - Possible sandbox")
    else:
        print("     ✅ Disque normal pour un vrai PC")

    # 4. Processus actifs
    processus = len(psutil.pids())
    print(f"🔄 Processus actifs : {processus}")

    if processus < 50:
        score_sandbox += 20
        indices.append(f"⚠️ Peu de processus ({processus}) - Sandbox probable")
    elif processus < 100:
        score_sandbox += 10
        indices.append(f"⚠️ Processus limités ({processus}) - Possible sandbox")
    else:
        print("   ✅ Nombre de processus normal")
    
    print("\n" + "="*60)
    return score_sandbox, indices

# PARTIE 2 : DÉTECTION DE LA VIRTUALISATION
# ==========================================

def detecter_virtualisation():
    """Détecte si on tourne dans une VM"""
    
    print("\n🖥️  Analyse de virtualisation...")
    print("="*60)
    
    score_vm = 0
    indices = []
    
    # 1. Vérifier le système
    systeme = platform.system()
    machine = platform.machine()
    
    print(f"Architecture : {machine}")
    
    # 2. Chercher des mots-clés suspects dans les infos système
    mots_vm = ["virtual", "vmware", "vbox", "qemu", "xen", "hyperv"]
    
    infos_complete = f"{platform.platform()} {platform.processor()}".lower()
    
    for mot in mots_vm:
        if mot in infos_complete:
            score_vm += 30
            indices.append(f"⚠️ Mot-clé VM détecté : '{mot}'")
            print(f"⚠️ '{mot}' trouvé dans les infos système")
    
    if score_vm == 0:
        print("✅ Aucune trace de virtualisation")
    
    print("="*60)
    return score_vm, indices

# PARTIE 3 : VÉRIFICATION HOSTNAME
# =================================

def verifier_hostname():
    """Vérifie si le hostname est suspect"""
    
    print("\n🏷️  Analyse du hostname...")
    print("="*60)
    
    score_host = 0
    indices = []
    
    hostname = socket.gethostname().lower()
    print(f"Hostname : {hostname}")
    
    # Mots suspects dans les noms de machines sandbox
    mots_suspects = [
        "sandbox", "test", "malware", "virus", "analysis",
        "cuckoo", "joe", "anubis", "sample", "vm", "virtual"
    ]
    
    for mot in mots_suspects:
        if mot in hostname:
            score_host += 25
            indices.append(f"⚠️ Mot suspect dans hostname : '{mot}'")
            print(f"⚠️ '{mot}' trouvé dans le hostname")
    
    if score_host == 0:
        print("✅ Hostname normal")
    
    print("="*60)
    return score_host, indices

# PARTIE 4 : TIMING ATTACK
# =========================

def timing_attack():
    """Détecte les sandbox avec accélération temporelle"""
    
    print("\n⏱️  Test de timing...")
    print("="*60)
    
    score_timing = 0
    indices = []
    
    print("Attente de 2 secondes...")
    
    start = time.time()
    time.sleep(2)
    end = time.time()
    
    temps_ecoule = end - start
    print(f"Temps réel écoulé : {temps_ecoule:.3f} secondes")
    
    # Les sandbox peuvent "accélérer" le temps
    if temps_ecoule < 1.5:
        score_timing += 30
        indices.append(f"⚠️ Accélération temporelle détectée ({temps_ecoule:.3f}s)")
        print("⚠️ Le temps s'écoule trop vite - Sandbox avec accélération")
    elif temps_ecoule > 2.5:
        score_timing += 10
        indices.append(f"⚠️ Temps ralenti détecté ({temps_ecoule:.3f}s)")
        print("⚠️ Le temps s'écoule trop lentement - Possible sandbox")
    else:
        print("✅ Timing normal")
    
    print("="*60)
    return score_timing, indices

# PARTIE 5 : FONCTION PRINCIPALE
# ===============================

def analyser_environnement():
    """Analyse complète de l'environnement"""

    print(f"🖥️  Système : {platform.system()} {platform.release()}")
    print(f"🏷️  Hostname : {socket.gethostname()}")
    print(f"🕐 Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n")
    
    # Détection ressources
    score_ressources, indices_ressources = detecter_ressources()
    
    # Détection virtualisation
    score_vm, indices_vm = detecter_virtualisation()
    
    # Vérification hostname
    score_host, indices_host = verifier_hostname()
    
    # Timing attack
    score_timing, indices_timing = timing_attack()
    
    # Score total
    score_total = score_ressources + score_vm + score_host + score_timing
    indices = indices_ressources + indices_vm + indices_host + indices_timing
    
    # Afficher le résultat
    print(f"\n📊 SCORE SANDBOX : {score_total}/100")
    
    if score_total >= 60:
        print("🔴 SANDBOX DÉTECTÉE - Environnement virtuel probable")
    elif score_total >= 30:
        print("🟡 SUSPECT - Possible environnement virtuel")
    else:
        print("🟢 VRAI PC - Environnement normal détecté")
    
    if indices:
        print("\n🔍 Indices détectés :")
        for indice in indices:
            print(f"   {indice}")
    
    return score_total

# PROGRAMME PRINCIPAL
analyser_environnement()