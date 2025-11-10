"""
Chatbot IA en mode console
Conversation interactive avec l'utilisateur
Victor - Session 16 - APIs IA
"""

from simulateur_ia import SimulateurIA

class ChatbotConsole:
    """Chatbot interactif en console"""
    
    def __init__(self):
        self.ia = SimulateurIA(nom_modele="ChatBot-1.0")
        self.en_conversation = True
    
    def afficher_banner(self):
        """Affiche la bannière de bienvenue"""
        print("\n" + "="*50)
        print("🤖  CHATBOT IA - Mode Console")
        print("="*50)
        print("\nCommandes disponibles :")
        print("  - Tapez votre message pour discuter")
        print("  - 'historique' : Voir toute la conversation")
        print("  - 'sauvegarder' : Sauvegarder la conversation")
        print("  - 'charger' : Charger conversation précédente")
        print("  - 'quitter' : Terminer la conversation")
        print("\n" + "="*50 + "\n")
    
    def traiter_commande(self, message):
        """Traite les commandes spéciales"""
        message_lower = message.lower().strip()
        
        if message_lower == "historique":
            self.ia.afficher_historique()
            return True
        
        elif message_lower == "sauvegarder":
            self.ia.sauvegarder_conversation()
            return True
        
        elif message_lower == "charger":
            self.ia.charger_conversation()
            return True
        
        elif message_lower in ["quitter", "quit", "exit", "bye"]:
            print("\n🤖 IA: Au revoir ! À bientôt ! 👋\n")
            
            # Demander sauvegarde
            sauver = input("💾 Sauvegarder la conversation ? (o/n) : ")
            if sauver.lower() in ["o", "oui", "y", "yes"]:
                self.ia.sauvegarder_conversation()
            
            self.en_conversation = False
            return True
        
        return False
    
    def demarrer(self):
        """Démarre la conversation"""
        self.afficher_banner()
        
        # Demander si charger conversation
        charger = input("📂 Charger conversation précédente ? (o/n) : ")
        if charger.lower() in ["o", "oui", "y", "yes"]:
            self.ia.charger_conversation()
            print()
        
        print("💬 Conversation démarrée ! (tapez 'quitter' pour terminer)\n")
        
        # Boucle conversation
        while self.en_conversation:
            # Message utilisateur
            message_user = input("🧑 VOUS: ")
            
            # Vérifier si vide
            if not message_user.strip():
                continue
            
            # Traiter commandes spéciales
            if self.traiter_commande(message_user):
                continue
            
            # Envoyer à l'IA
            print("🤖 IA: ", end="", flush=True)
            
            # Simuler typing (effet visuel)
            import time
            time.sleep(0.3)
            
            reponse = self.ia.envoyer_message(message_user)
            print(reponse + "\n")


# === LANCEMENT ===
if __name__ == "__main__":
    chatbot = ChatbotConsole()
    chatbot.demarrer()
