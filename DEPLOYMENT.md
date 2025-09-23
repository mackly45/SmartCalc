# Guide de Déploiement Vercel pour SmartCalc

## 📋 Prérequis

- [x] Compte GitHub
- [x] Compte Vercel (gratuit)
- [x] Application web SmartCalc prête

## 🚀 Étapes de Déploiement

### Étape 1: Préparer le Repository GitHub

1. **Créer un nouveau repository sur GitHub**
   ```
   Nom: SmartCalc-Web
   Description: Calculatrice scientifique web avec Flask
   Public/Private: Public (recommandé pour le déploiement gratuit)
   ```

2. **Initialiser et pousser le code**
   ```bash
   # Dans le dossier SmartCalc
   git init
   git add .
   git commit -m "Initial commit: SmartCalc web version"
   git branch -M main
   git remote add origin https://github.com/VOTRE_USERNAME/SmartCalc-Web.git
   git push -u origin main
   ```

### Étape 2: Configuration Vercel

1. **Se connecter à Vercel**
   - Aller sur [vercel.com](https://vercel.com)
   - Se connecter avec GitHub

2. **Importer le projet**
   - Cliquer sur "New Project"
   - Sélectionner votre repository `SmartCalc-Web`
   - Cliquer sur "Import"

3. **Configuration automatique**
   Vercel détectera automatiquement:
   - `vercel.json` pour la configuration
   - `requirements-web.txt` pour les dépendances Python
   - `app.py` comme point d'entrée

4. **Déployer**
   - Cliquer sur "Deploy"
   - Attendre la fin du déploiement (1-3 minutes)

### Étape 3: Vérification du Déploiement

Une fois déployé, vous recevrez:
- **URL de production**: `https://smart-calc-web-xxx.vercel.app`
- **URL de prévisualisation**: Pour chaque commit

## 🔧 Configuration Avancée

### Variables d'Environnement (optionnel)

Dans les paramètres Vercel du projet:
```
FLASK_ENV=production
PYTHONPATH=./
```

### Domaine Personnalisé

1. Dans les paramètres Vercel
2. Section "Domains"
3. Ajouter votre domaine personnalisé

## 📁 Structure de Fichiers Importante

```
SmartCalc/
├── app.py                 # ✅ Point d'entrée principal
├── vercel.json           # ✅ Configuration Vercel
├── requirements-web.txt  # ✅ Dépendances Python
├── .vercelignore        # ✅ Fichiers à ignorer
├── models/              # ✅ Logique métier
├── templates/           # ✅ Templates HTML
├── static/              # ✅ CSS, JS, images
└── .gitignore          # ✅ Fichiers Git à ignorer
```

## 🚦 Commandes Git Utiles

```bash
# Vérifier le statut
git status

# Ajouter tous les fichiers
git add .

# Commit avec message
git commit -m "Votre message de commit"

# Pousser vers GitHub
git push origin main

# Vérifier les branches
git branch -a

# Vérifier les remotes
git remote -v
```

## 🐛 Résolution de Problèmes

### Erreur de Build

Si le déploiement échoue:

1. **Vérifier les logs** dans l'interface Vercel
2. **Dépendances manquantes**:
   ```bash
   # Tester localement
   pip install -r requirements-web.txt
   python app.py
   ```

3. **Erreur de chemin**:
   - Vérifier que `app.py` est à la racine
   - Vérifier les imports relatifs

### Erreur 404

- Vérifier que les routes Flask sont correctes
- Vérifier la configuration dans `vercel.json`

### Erreur de dépendances

```bash
# Mettre à jour requirements-web.txt
pip freeze > requirements-web.txt
```

## 🔄 Déploiement Automatique

**Avantage**: Chaque push vers la branche `main` déclenche automatiquement un nouveau déploiement.

```bash
# Modifier du code
git add .
git commit -m "Amélioration de l'interface"
git push origin main
# ✨ Déploiement automatique démarré !
```

## 📊 Monitoring et Analytics

### Dans l'interface Vercel:
- **Functions**: Temps d'exécution des API
- **Analytics**: Trafic et performance
- **Speed Insights**: Métriques de vitesse

## 🔒 Sécurité

### Recommandations:
- Garder `requirements-web.txt` à jour
- Ne pas exposer de clés API dans le code
- Utiliser les variables d'environnement Vercel pour les secrets

## 🌐 URLs de Test

Après déploiement, testez ces URLs:

```
https://votre-app.vercel.app/           # Page d'accueil
https://votre-app.vercel.app/scientific # Calculatrice scientifique
https://votre-app.vercel.app/converter  # Convertisseur
https://votre-app.vercel.app/health     # Health check
```

## 📈 Optimisations

### Performance:
- Activer la compression gzip (automatique sur Vercel)
- Optimiser les images dans `/static/`
- Utiliser un CDN pour les ressources externes

### SEO:
- Ajouter des meta tags dans `base.html`
- Créer un `sitemap.xml`
- Ajouter un `robots.txt`

## ✅ Checklist Final

- [ ] Code poussé sur GitHub
- [ ] Repository public/accessible
- [ ] `vercel.json` configuré
- [ ] `requirements-web.txt` complet
- [ ] Application testée localement
- [ ] Déploiement Vercel réussi
- [ ] URLs de test fonctionnelles
- [ ] Domaine personnalisé configuré (optionnel)

## 📞 Support

- **Documentation Vercel**: [vercel.com/docs](https://vercel.com/docs)
- **Support Vercel**: [vercel.com/support](https://vercel.com/support)
- **GitHub Issues**: Pour les bugs du projet

---

🎉 **Félicitations !** Votre calculatrice SmartCalc est maintenant en ligne et accessible au monde entier !