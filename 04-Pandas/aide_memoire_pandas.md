# 🐼 AIDE-MÉMOIRE PANDAS - Tom

Synthèse opérations essentielles Pandas pour projets data.

---

## 📦 IMPORT
```python
import pandas as pd
```

---

## 🔧 CRÉER DATAFRAME

### Depuis dictionnaire
```python
df = pd.DataFrame({
    'colonne1': [1, 2, 3],
    'colonne2': ['a', 'b', 'c']
})
```

### Depuis CSV
```python
df = pd.read_csv('fichier.csv')
```

### Depuis Excel
```python
df = pd.read_excel('fichier.xlsx')
```

---

## 👀 EXPLORER DONNÉES
```python
df.head()           # 5 premières lignes
df.head(10)         # 10 premières lignes
df.tail()           # 5 dernières lignes
df.shape            # (lignes, colonnes)
df.columns          # Noms colonnes
df.info()           # Infos types/mémoire
df.describe()       # Stats colonnes numériques
```

---

## 🎯 SÉLECTIONNER

### Une colonne (Series)
```python
df['nom_colonne']
```

### Plusieurs colonnes (DataFrame)
```python
df[['col1', 'col2', 'col3']]
```

### Une ligne par index
```python
df.loc[0]           # Ligne index 0
df.iloc[0]          # Première ligne (position)
```

### Plage lignes
```python
df[0:5]             # Lignes 0 à 4
df.head(5)          # 5 premières (mieux)
```

---

## 🔍 FILTRER

### Condition simple
```python
df[df['age'] > 30]
df[df['ville'] == 'Paris']
df[df['prix'] <= 10]
```

### Conditions multiples ET (&)
```python
df[(df['age'] > 30) & (df['ville'] == 'Paris')]
#  ^^^^^^^^^^^^^^^^    ^^^^^^^^^^^^^^^^^^^^^^
#  Parenthèses OBLIGATOIRES !
```

### Conditions multiples OU (|)
```python
df[(df['age'] < 20) | (df['age'] > 60)]
```

### Contient (string)
```python
df[df['nom'].str.contains('Tom')]
```

---

## 📊 TRIER
```python
df.sort_values('colonne')                    # Croissant
df.sort_values('colonne', ascending=False)   # Décroissant
df.sort_values(['col1', 'col2'])             # Multi-colonnes
```

---

## 🎲 GROUPER & AGRÉGER

### Groupby simple
```python
df.groupby('zone')['prix'].mean()    # Prix moyen par zone
df.groupby('zone').size()            # Nombre par zone
```

### Agrégations multiples
```python
df.groupby('zone')['prix'].agg(['mean', 'min', 'max'])
```

### Plusieurs colonnes
```python
df.groupby('zone').agg({
    'prix': ['mean', 'min', 'max'],
    'hauteur': 'mean'
})
```

---

## ➕ AJOUTER/MODIFIER COLONNES

### Colonne calculée
```python
df['nouvelle'] = df['col1'] + df['col2']
df['ratio'] = df['prix'] / df['quantite']
```

### Fonction apply
```python
def ma_fonction(valeur):
    if valeur > 10:
        return 'Grand'
    else:
        return 'Petit'

df['categorie'] = df['taille'].apply(ma_fonction)
```

### Avec lambda
```python
df['double'] = df['prix'].apply(lambda x: x * 2)
```

---

## 🗑️ SUPPRIMER
```python
df.drop('colonne', axis=1)           # Supprimer colonne
df.drop([0, 1, 2], axis=0)          # Supprimer lignes
df.drop_duplicates()                 # Supprimer doublons
```

---

## 📈 STATISTIQUES
```python
df['colonne'].mean()     # Moyenne
df['colonne'].median()   # Médiane
df['colonne'].min()      # Minimum
df['colonne'].max()      # Maximum
df['colonne'].sum()      # Somme
df['colonne'].count()    # Nombre valeurs
df['colonne'].std()      # Écart-type
```

---

## 🔝 TOP N
```python
df.nlargest(3, 'prix')   # 3 plus grandes valeurs
df.nsmallest(3, 'prix')  # 3 plus petites valeurs
```

---

## 💾 SAUVEGARDER
```python
df.to_csv('fichier.csv', index=False)     # Vers CSV
df.to_excel('fichier.xlsx', index=False)  # Vers Excel
df.to_json('fichier.json')                # Vers JSON
```

---

## 🧹 GESTION VALEURS MANQUANTES
```python
df.isnull()              # Détecter NaN
df.isnull().sum()        # Compter NaN par colonne
df.dropna()              # Supprimer lignes avec NaN
df.fillna(0)             # Remplacer NaN par 0
df.fillna(df.mean())     # Remplacer NaN par moyenne
```

---

## 🎯 ASTUCES FRÉQUENTES

### Renommer colonnes
```python
df.rename(columns={'ancien': 'nouveau'})
```

### Réinitialiser index
```python
df.reset_index(drop=True)
```

### Copier DataFrame
```python
df_copie = df.copy()     # Copie indépendante
```

### Valeurs uniques
```python
df['colonne'].unique()        # Liste valeurs uniques
df['colonne'].nunique()       # Nombre valeurs uniques
df['colonne'].value_counts()  # Comptage par valeur
```

---

## 🔗 CHAÎNAGE OPÉRATIONS
```python
# Enchaîner plusieurs opérations
resultat = (df
    .query('age > 30')
    .groupby('ville')['prix']
    .mean()
    .sort_values(ascending=False)
)
```

---

## 💡 RAPPELS IMPORTANTS

- ⚠️ Toujours `import pandas as pd`
- ⚠️ Filtres multiples : Parenthèses obligatoires !
- ⚠️ `&` pour ET, `|` pour OU (pas `and`/`or`)
- ⚠️ `df.copy()` pour éviter modifications involontaires
- ⚠️ `index=False` dans to_csv pour éviter colonne index
- 💡 Google "pandas [opération]" = OK même après 10 ans !
- 📚 Documentation : https://pandas.pydata.org/docs/

---

## 🎯 WORKFLOW TYPE
```python
# 1. CHARGER
df = pd.read_csv('data.csv')

# 2. EXPLORER
df.head()
df.info()
df.describe()

# 3. NETTOYER
df = df.dropna()
df = df.drop_duplicates()

# 4. FILTRER
df_filtre = df[df['prix'] > 10]

# 5. ANALYSER
resultat = df_filtre.groupby('zone')['prix'].mean()

# 6. SAUVEGARDER
df_filtre.to_csv('resultat.csv', index=False)
```

---

**Session 18 - Victor, Jardinier → Data Analyst ! 🌱📊**