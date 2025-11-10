# 🤖 Projets APIs IA - Simulateur & Chatbots

Découverte des APIs IA à travers 3 projets progressifs.

## 📚 Projets

### 1. Simulateur IA
**Fichier** : `simulateur_ia.py`

Moteur de simulation d'API IA (comme Claude, GPT).

**Fonctionnalités** :
- Détection mots-clés contextuels
- Génération réponses intelligentes
- Historique conversation
- Sauvegarde/chargement JSON

**Compétences** :
- Classes POO
- Dictionnaires imbriqués
- Manipulation JSON
- Gestion erreurs (try/except)

---

### 2. Chatbot Console
**Fichier** : `chatbot_console.py`

Interface conversationnelle interactive en terminal.

**Fonctionnalités** :
- Conversation continue (boucle while)
- Commandes spéciales (historique, sauvegarder, quitter)
- Effet typing (délai visuel)
- Sauvegarde à la demande

**Compétences** :
- Boucles while interactives
- Input utilisateur
- Import modules personnalisés
- Gestion état conversation

---

### 3. Assistant Jardinier IA 🌱
**Fichier** : `assistant_jardinier.py`

Chatbot spécialisé jardinage urbain (Île-de-France).

**Fonctionnalités** :
- Conseils roses, tulipes, arrosage, taille
- Spécialité jardinage parisien
- Base connaissances métier
- Interface personnalisée

**Compétences** :
- Héritage POO (extends SimulateurIA)
- Spécialisation métier
- Personnalisation réponses

## 🎯 Structure code
```
SimulateurIA (classe de base)
    ↓
ChatbotConsole → Utilise SimulateurIA
    ↓
AssistantJardinier → Hérite de SimulateurIA
```

## 💻 Utilisation

### Chatbot générique
```bash
python chatbot_console.py
```

### Assistant jardinier
```bash
python assistant_jardinier.py
```

## 🔧 Technologies

- Python 3.12
- POO (Classes, héritage)
- JSON (persistance)
- Modules (import)

## 🎓 Concepts avancés

✅ Architecture modulaire  
✅ Héritage de classes  
✅ Polymorphisme (méthodes surchargées)  
✅ Encapsulation données  
✅ Gestion état (conversation)

## 📈 Évolution possible

- [ ] Connecter vraie API (OpenAI, Claude)
- [ ] Interface graphique (Tkinter)
- [ ] Commandes vocales
- [ ] Base données SQLite
- [ ] Déploiement web

## 📅 Session 16 - Novembre 2025

Premier contact avec les APIs IA !