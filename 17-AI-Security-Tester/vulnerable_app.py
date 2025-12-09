from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Créer une base de données SQLite en mémoire
def init_db():
    """Initialise la base de données avec des données de test"""
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    cursor = conn.cursor()
    
    # Table users (pour SQLi)
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            email TEXT
        )
    ''')
    
    # Données de test
    cursor.execute("INSERT INTO users VALUES (1, 'admin', 'super_secret_pass', 'admin@test.com')")
    cursor.execute("INSERT INTO users VALUES (2, 'tom', 'password123', 'tom@test.com')")
    cursor.execute("INSERT INTO users VALUES (3, 'alice', 'alice2024', 'alice@test.com')")
    
    conn.commit()
    return conn

# Base de données globale
db = init_db()

# PAGE D'ACCUEIL
@app.route('/')
def home():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Security Tester - Vulnerable App</title>
        <style>
            body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #e74c3c; }
            .warning { background: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0; }
            .section { background: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 5px; }
            input, textarea { padding: 10px; width: 100%; margin: 10px 0; }
            button { background: #3498db; color: white; padding: 10px 20px; border: none; cursor: pointer; }
            button:hover { background: #2980b9; }
        </style>
    </head>
    <body>
        <h1>AI Security Tester - Vulnerable App</h1>
        
        <div class="warning">
            ATTENTION : Cette application contient des failles de sécurité VOLONTAIRES pour apprentissage.
            Ne JAMAIS utiliser ce code en production !
        </div>
        
        <div class="section">
            <h2>Test 1 : SQL Injection</h2>
            <p>Rechercher un utilisateur par nom :</p>
            <form action="/search" method="GET">
                <input type="text" name="username" placeholder="Nom utilisateur">
                <button type="submit">Rechercher</button>
            </form>
            <p style="color: #7f8c8d; font-size: 12px;">
                Essaie : admin' OR '1'='1
            </p>
        </div>
        
        <div class="section">
            <h2>Test 2 : XSS (Cross-Site Scripting)</h2>
            <p>Poster un commentaire :</p>
            <form action="/comment" method="POST">
                <textarea name="comment" placeholder="Ton commentaire..."></textarea>
                <button type="submit">Publier</button>
            </form>
            <p style="color: #7f8c8d; font-size: 12px;">
                Essaie : &lt;script&gt;alert('XSS')&lt;/script&gt;
            </p>
        </div>
        
        <div class="section">
            <h2>Test 3 : Path Traversal</h2>
            <p>Lire un fichier :</p>
            <form action="/read" method="GET">
                <input type="text" name="file" placeholder="Nom du fichier">
                <button type="submit">Lire</button>
            </form>
            <p style="color: #7f8c8d; font-size: 12px;">
                Essaie : test.txt
            </p>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)

# VULNERABILITE 1 : SQL INJECTION
@app.route('/search')
def search():
    username = request.args.get('username', '')
    
    # VULNERABLE : Concatenation directe (SQLi possible)
    query = f"SELECT * FROM users WHERE username = '{username}'"
    
    try:
        cursor = db.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Resultats de recherche</title>
            <style>
                body {{ font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background: #3498db; color: white; }}
            </style>
        </head>
        <body>
            <h1>Resultats de recherche</h1>
            <p><strong>Requete SQL executee :</strong> <code>{query}</code></p>
            
            <table>
                <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Password</th>
                    <th>Email</th>
                </tr>
        '''
        
        for row in results:
            html += f'''
                <tr>
                    <td>{row[0]}</td>
                    <td>{row[1]}</td>
                    <td>{row[2]}</td>
                    <td>{row[3]}</td>
                </tr>
            '''
        
        html += '''
            </table>
            <div><a href="/">Retour</a></div>
        </body>
        </html>
        '''
        
        return render_template_string(html)
        
    except Exception as e:
        return f"<h1>Erreur SQL</h1><p>{str(e)}</p><a href='/'>Retour</a>"

# VULNERABILITE 2 : XSS
@app.route('/comment', methods=['POST'])
def comment():
    comment = request.form.get('comment', '')
    
    # VULNERABLE : Pas d'echappement HTML (XSS possible)
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Commentaire publie</title>
        <style>
            body {{ font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }}
            .comment {{ background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <h1>Commentaire publie</h1>
        <div class="comment">
            {comment}
        </div>
        <a href="/">Retour</a>
    </body>
    </html>
    '''
    
    return render_template_string(html)

# VULNERABILITE 3 : PATH TRAVERSAL
@app.route('/read')
def read_file():
    import os
    
    filename = request.args.get('file', 'test.txt')
    
    # Chemin de base (dossier du script)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, filename)
    
    # VULNERABLE : Pas de validation du chemin (Path Traversal possible)
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Contenu du fichier</title>
            <style>
                body {{ font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }}
                pre {{ background: #2c3e50; color: #ecf0f1; padding: 20px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <h1>Contenu de : {filename}</h1>
            <pre>{content}</pre>
            <a href="/">Retour</a>
        </body>
        </html>
        '''
        
        return render_template_string(html)
        
    except Exception as e:
        return f"<h1>Erreur</h1><p>{str(e)}</p><a href='/'>Retour</a>"

if __name__ == '__main__':
    print("Demarrage de l'application vulnerable...")
    print("URL : http://127.0.0.1:5000")
    print("Cette app contient des failles VOLONTAIRES pour apprentissage !")
    app.run(debug=True, port=5000)

