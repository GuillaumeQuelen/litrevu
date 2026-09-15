# LITRevu

## Le service
Un service mettant en lien des utilisateurs pour construire leur propre communauté de critiques de livres et articles.

## Pré-requis
- Python 3.12
- Git

## Installation & Lancement
- Télécharger le dossier (https://github.com/GuillaumeQuelen/litrevu) ou cloner le git:
```bash 
git clone https://github.com/GuillaumeQuelen/litrevu.git
``` 
- Créer l'environnement virtuel:
```bash 
python3 -m venv venv
 ```
- Activer l'environnement virtuel:
```bash 
source venv/bin/activate
``` 
sur windows 
```bash 
venv\Scripts\activate 
```

Utiliser les commandes suivantes dans le terminal:
```bash 
pip install -r requirements.txt
```
```bash 
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" 
```
créez un fichier .env à la racine, sur le modèle de .env.example, et renseignez-y la clé générée

## Lancement
effectuer les commandes suivantes dans le terminal :
```bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```
ouvrir la page http://127.0.0.1:8000/ dans votre navigateur

## Les comptes test
Nom d’utilisateur: marie_l
Mot de passe : LitRevu2026!

Nom d’utilisateur: thomas_d
Mot de passe : LitRevu2026!

Nom d’utilisateur: sarah_b
Mot de passe : LitRevu2026!

## Compte Administrateur
Nom d’utilisateur: Utilisateur1
Mot de passe : %#!ùS98hZ/éjHSWa27

## Les fonctionnalités
Créer un compte avec un mot de passe
Demander une critique
Ecrire une critique
Suivre un utilisateur
Bloquer et débloquer un utilisateur

## Outils d'audit
Flake8 - limité à 119 caractères par ligne - à lancer via la commande : flake8