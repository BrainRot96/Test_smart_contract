from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

def creer_memo_ascii():
    """Crée un mémo ASCII en PDF"""
    
    # Créer le PDF
    c = canvas.Canvas("MEMO_ASCII.pdf", pagesize=A4)
    width, height = A4
    
    # Couleurs
    bleu_fonce = HexColor('#2c3e50')
    bleu_clair = HexColor('#3498db')
    vert = HexColor('#27ae60')
    orange = HexColor('#e67e22')
    
    # TITRE
    c.setFillColor(bleu_fonce)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(2*cm, height - 3*cm, "📋 MÉMO ASCII - Table de Référence")
    
    c.setFont("Helvetica", 10)
    c.drawString(2*cm, height - 3.7*cm, "ASCII = American Standard Code for Information Interchange")
    
    # LIGNE SÉPARATRICE
    c.setStrokeColor(bleu_clair)
    c.setLineWidth(2)
    c.line(2*cm, height - 4*cm, width - 2*cm, height - 4*cm)
    
    y = height - 5*cm
    
    # SECTION 1 : RÈGLES ESSENTIELLES
    c.setFillColor(bleu_clair)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2*cm, y, "🎯 RÈGLES ESSENTIELLES")
    y -= 0.7*cm
    
    c.setFillColor(bleu_fonce)
    c.setFont("Helvetica", 11)
    
    regles = [
        "• Chiffres : '0' = 48  →  '9' = 57",
        "• Majuscules : 'A' = 65  →  'Z' = 90",
        "• Minuscules : 'a' = 97  →  'z' = 122",
        "• Différence Maj/Min = 32  (ex: 'A' + 32 = 'a')",
        "• Espace = 32",
        "• Underscore '_' = 95"
    ]
    
    for regle in regles:
        c.drawString(2.5*cm, y, regle)
        y -= 0.6*cm
    
    y -= 0.5*cm
    
    # SECTION 2 : TABLE COMPLÈTE
    c.setFillColor(bleu_clair)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2*cm, y, "📊 TABLE ASCII (32-127)")
    y -= 0.7*cm
    
    c.setFont("Courier", 9)
    c.setFillColor(bleu_fonce)
    
    # Header
    c.drawString(2*cm, y, "Code")
    c.drawString(3.5*cm, y, "Char")
    c.drawString(5*cm, y, "Description")
    c.drawString(11*cm, y, "Code")
    c.drawString(12.5*cm, y, "Char")
    c.drawString(14*cm, y, "Description")
    y -= 0.5*cm
    
    # Ligne
    c.setStrokeColor(bleu_clair)
    c.line(2*cm, y, width - 2*cm, y)
    y -= 0.5*cm
    
    # Caractères importants
    ascii_table = [
        (32, " ", "Espace", 65, "A", "Maj A"),
        (33, "!", "Point excl.", 66, "B", "Maj B"),
        (35, "#", "Dièse", 67, "C", "Maj C"),
        (40, "(", "Parenthèse", 68, "D", "Maj D"),
        (41, ")", "Parenthèse", 69, "E", "Maj E"),
        (43, "+", "Plus", 70, "F", "Maj F"),
        (45, "-", "Moins", 90, "Z", "Maj Z"),
        (46, ".", "Point", 95, "_", "Underscore"),
        (47, "/", "Slash", 97, "a", "Min a"),
        (48, "0", "Chiffre 0", 98, "b", "Min b"),
        (49, "1", "Chiffre 1", 99, "c", "Min c"),
        (50, "2", "Chiffre 2", 100, "d", "Min d"),
        (57, "9", "Chiffre 9", 122, "z", "Min z"),
        (58, ":", "Deux-points", 123, "{", "Accolade ouv."),
        (64, "@", "Arobase", 125, "}", "Accolade ferm."),
    ]
    
    for (code1, char1, desc1, code2, char2, desc2) in ascii_table:
        c.drawString(2*cm, y, str(code1))
        c.drawString(3.5*cm, y, char1 if char1 != " " else "' '")
        c.drawString(5*cm, y, desc1)
        
        c.drawString(11*cm, y, str(code2))
        c.drawString(12.5*cm, y, char2)
        c.drawString(14*cm, y, desc2)
        y -= 0.5*cm
        
        if y < 5*cm:
            # Nouvelle page si nécessaire
            c.showPage()
            y = height - 3*cm
    
    # NOUVELLE PAGE - EXEMPLES PYTHON
    c.showPage()
    y = height - 3*cm
    
    # TITRE PAGE 2
    c.setFillColor(bleu_fonce)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(2*cm, y, "🐍 EXEMPLES PYTHON")
    y -= 1.5*cm
    
    # SECTION ord()
    c.setFillColor(bleu_clair)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2*cm, y, "🔢 ord() - Caractère → Code ASCII")
    y -= 0.7*cm
    
    c.setFont("Courier", 10)
    c.setFillColor(bleu_fonce)
    
    exemples_ord = [
        "ord('A')   # → 65",
        "ord('a')   # → 97",
        "ord('0')   # → 48",
        "ord(' ')   # → 32",
        "ord('_')   # → 95",
    ]
    
    for ex in exemples_ord:
        c.drawString(2.5*cm, y, ex)
        y -= 0.5*cm
    
    y -= 0.5*cm
    
    # SECTION chr()
    c.setFillColor(bleu_clair)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2*cm, y, "🔤 chr() - Code ASCII → Caractère")
    y -= 0.7*cm
    
    c.setFont("Courier", 10)
    c.setFillColor(bleu_fonce)
    
    exemples_chr = [
        "chr(65)    # → 'A'",
        "chr(97)    # → 'a'",
        "chr(48)    # → '0'",
        "chr(32)    # → ' '",
        "chr(95)    # → '_'",
    ]
    
    for ex in exemples_chr:
        c.drawString(2.5*cm, y, ex)
        y -= 0.5*cm
    
    y -= 0.5*cm
    
    # SECTION CONVERSIONS
    c.setFillColor(bleu_clair)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2*cm, y, "🔄 CONVERSIONS UTILES")
    y -= 0.7*cm
    
    c.setFont("Courier", 9)
    c.setFillColor(bleu_fonce)
    
    conversions = [
        "# Majuscule → Minuscule",
        "chr(ord('A') + 32)  # → 'a'",
        "",
        "# Minuscule → Majuscule",
        "chr(ord('a') - 32)  # → 'A'",
        "",
        "# Décaler une lettre (César +3)",
        "chr(ord('a') + 3)   # → 'd'",
        "",
        "# César avec boucle (a-z)",
        "chr(((ord('z') - 97 + 3) % 26) + 97)  # → 'c'",
    ]
    
    for conv in conversions:
        c.drawString(2.5*cm, y, conv)
        y -= 0.45*cm
    
    y -= 0.5*cm
    
    # SECTION CHIFFREMENT CÉSAR
    c.setFillColor(orange)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2*cm, y, "🔐 EXEMPLE COMPLET : CÉSAR")
    y -= 0.7*cm
    
    c.setFont("Courier", 8)
    c.setFillColor(bleu_fonce)
    
    code_cesar = [
        "def cesar(texte, decalage):",
        "    resultat = ''",
        "    for lettre in texte:",
        "        if lettre.isalpha() and lettre.islower():",
        "            # Décaler en restant dans a-z",
        "            nouveau = chr(((ord(lettre) - 97 + decalage) % 26) + 97)",
        "            resultat += nouveau",
        "        else:",
        "            resultat += lettre",
        "    return resultat",
        "",
        "# Utilisation :",
        "cesar('hello', 3)   # → 'khoor'",
        "cesar('xyz', 3)     # → 'abc'  (boucle !)",
    ]
    
    for line in code_cesar:
        c.drawString(2.5*cm, y, line)
        y -= 0.4*cm
    
    # FOOTER
    y = 2*cm
    c.setFillColor(HexColor('#7f8c8d'))
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(2*cm, y, "Créé avec Python & ReportLab")
    c.drawString(width - 6*cm, y, "Victor (Tom) - 2025")
    
    # Sauvegarder
    c.save()
    print("✅ Mémo ASCII créé : MEMO_ASCII.pdf")

if __name__ == "__main__":
    creer_memo_ascii()