#!/bin/bash

# Script de déploiement automatique pour SmartCalc Web
# Usage: ./deploy.sh "message de commit"

echo "🚀 Déploiement SmartCalc Web vers GitHub et Vercel"
echo "================================================="

# Vérifier si un message de commit est fourni
if [ -z "$1" ]; then
    echo "❌ Erreur: Veuillez fournir un message de commit"
    echo "Usage: ./deploy.sh \"votre message de commit\""
    exit 1
fi

COMMIT_MESSAGE="$1"

echo "📝 Message de commit: $COMMIT_MESSAGE"
echo ""

# Vérifier si nous sommes dans un repo git
if [ ! -d ".git" ]; then
    echo "🔧 Initialisation du repository Git..."
    git init
    git branch -M main
    
    echo "🔗 Ajout du remote origin..."
    echo "⚠️  N'oubliez pas de remplacer YOUR_USERNAME par votre nom d'utilisateur GitHub !"
    echo "git remote add origin https://github.com/YOUR_USERNAME/SmartCalc-Web.git"
    echo ""
    echo "Appuyez sur Entrée après avoir configuré le remote..."
    read
fi

# Ajouter tous les fichiers
echo "📁 Ajout des fichiers..."
git add .

# Vérifier s'il y a des changements
if git diff --staged --quiet; then
    echo "⚠️  Aucun changement détecté"
    exit 0
fi

# Afficher les fichiers qui vont être commités
echo "📋 Fichiers à commiter:"
git diff --staged --name-only

echo ""
echo "💾 Création du commit..."
git commit -m "$COMMIT_MESSAGE"

echo ""
echo "🌐 Push vers GitHub..."
git push origin main

echo ""
echo "✅ Déploiement terminé !"
echo "🔗 Vercel va automatiquement déployer les changements"
echo "📱 Vérifiez votre dashboard Vercel dans quelques minutes"

echo ""
echo "🌟 URLs utiles:"
echo "   - GitHub Repo: https://github.com/YOUR_USERNAME/SmartCalc-Web"
echo "   - Vercel Dashboard: https://vercel.com/dashboard"
echo ""
echo "🎉 SmartCalc Web est prêt !"