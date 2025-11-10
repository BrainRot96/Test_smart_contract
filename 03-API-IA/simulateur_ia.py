"""Simulateur d'API IA avec sauvegarde JSON"""

import random
import time
import json

class SimulateurIA:
    """Simule une API IA (comme Claude, GPT)"""
    
    def __init__(self, nom_modele="SimulIA-1.0"):
        self.nom_modele = nom_modele
        self.historique = []
        self.reponses = {
            "bonjour": [
                "Bonjour ! Comment puis-je vous aider ?",
                "Salut ! Que puis-je faire pour vous ?",
            ],
            "python": [
                "Python est excellent pour l'IA !",
                "J'adore Python ! Parfait pour débuter.",
            ],
            "jardin": [
                "Ah, le jardinage ! Conseils pour vos plantes ?",
                "Les jardins sont magnifiques !",
            ],
            "merci": [
                "De rien ! Ravi d'avoir aidé !",
                "Avec plaisir !",
            ],
            "default": [
                "Intéressant ! Dites-moi plus ?",
                "Je comprends. Précisez votre demande ?",
            ]
        }
    
    def generer_reponse(self, message_utilisateur):
        """Génère une réponse basée sur le message"""
        time.sleep(0.5)
        message_lower = message_utilisateur.lower()
        
        for mot_cle, reponses_possibles in self.reponses.items():
            if mot_cle in message_lower:
                return random.choice(reponses_possibles)
        
        return random.choice(self.reponses["default"])
    
    def envoyer_message(self, message_utilisateur):
        """Envoie un message et reçoit réponse"""
        self.historique.append({
            "role": "user",
            "content": message_utilisateur
        })
        
        reponse = self.generer_reponse(message_utilisateur)
        
        self.historique.append({
            "role": "assistant",
            "content": reponse
        })
        
        return reponse
    
    def afficher_historique(self):
        """Affiche tout l'historique"""
        print("\n=== HISTORIQUE ===\n")
        for msg in self.historique:
            role = "🧑 VOUS" if msg["role"] == "user" else "🤖 IA"
            print(f"{role}: {msg['content']}\n")
    
    def sauvegarder_conversation(self, nom_fichier="conversation_ia.json"):
        """Sauvegarde l'historique en JSON"""
        with open(nom_fichier, "w", encoding="utf-8") as f:
            json.dump(self.historique, f, indent=4, ensure_ascii=False)
        print(f"💾 Sauvegardé dans {nom_fichier}")
    
    def charger_conversation(self, nom_fichier="conversation_ia.json"):
        """Charge l'historique depuis JSON"""
        try:
            with open(nom_fichier, "r", encoding="utf-8") as f:
                self.historique = json.load(f)
            print(f"📂 Chargé depuis {nom_fichier}")
            return True
        except FileNotFoundError:
            print("📝 Nouvelle conversation")
            return False


# === TEST ===
if __name__ == "__main__":
    print("=== Test Simulateur IA ===\n")
    
    ia = SimulateurIA()
    ia.charger_conversation()
    
    print("🧑 VOUS: Bonjour !")
    print(f"🤖 IA: {ia.envoyer_message('Bonjour !')}\n")
    
    print("🧑 VOUS: J'apprends Python")
    print(f"🤖 IA: {ia.envoyer_message('J\'apprends Python')}\n")
    
    print("🧑 VOUS: Je suis jardinier")
    print(f"🤖 IA: {ia.envoyer_message('Je suis jardinier')}\n")
    
    print("🧑 VOUS: Merci !")
    print(f"🤖 IA: {ia.envoyer_message('Merci !')}\n")
    
    ia.afficher_historique()
    ia.sauvegarder_conversation()