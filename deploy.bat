@echo off
REM Script de déploiement automatique pour SmartCalc Web (Windows)
REM Usage: deploy.bat "message de commit"

echo 🚀 Déploiement SmartCalc Web vers GitHub et Vercel
echo =================================================

REM Vérifier si un message de commit est fourni
if "%~1"=="" (
    echo ❌ Erreur: Veuillez fournir un message de commit
    echo Usage: deploy.bat "votre message de commit"
    exit /b 1
)

set "COMMIT_MESSAGE=%~1"

echo 📝 Message de commit: %COMMIT_MESSAGE%
echo.

REM Vérifier si nous sommes dans un repo git
if not exist ".git" (
    echo 🔧 Initialisation du repository Git...
    git init
    git branch -M main
    
    echo 🔗 Ajout du remote origin...
    echo ⚠️  N'oubliez pas de remplacer YOUR_USERNAME par votre nom d'utilisateur GitHub !
    echo git remote add origin https://github.com/YOUR_USERNAME/SmartCalc-Web.git
    echo.
    echo Appuyez sur Entrée après avoir configuré le remote...
    pause >nul
)

REM Ajouter tous les fichiers
echo 📁 Ajout des fichiers...
git add .

REM Vérifier s'il y a des changements
git diff --staged --quiet
if %errorlevel% equ 0 (
    echo ⚠️  Aucun changement détecté
    exit /b 0
)

REM Afficher les fichiers qui vont être commités
echo 📋 Fichiers à commiter:
git diff --staged --name-only

echo.
echo 💾 Création du commit...
git commit -m "%COMMIT_MESSAGE%"

echo.
echo 🌐 Push vers GitHub...
git push origin main

echo.
echo ✅ Déploiement terminé !
echo 🔗 Vercel va automatiquement déployer les changements
echo 📱 Vérifiez votre dashboard Vercel dans quelques minutes

echo.
echo 🌟 URLs utiles:
echo    - GitHub Repo: https://github.com/YOUR_USERNAME/SmartCalc-Web
echo    - Vercel Dashboard: https://vercel.com/dashboard
echo.
echo 🎉 SmartCalc Web est prêt !
pause