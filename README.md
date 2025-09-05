##### Projet conçu et développé en solo pour le titre RNCP5 Développeur Web/Web Mobile   #####

# PAUSE EMPATHIQUE
#### Observer, Ressentir, Comprendre, Agir

Une application web qui permet de pratiquer l'auto-empathie de façon guidée, inspirée par la Communication Non Violente (CNV).
C'est un outil accessible et gratuit, pour affiner son discernement et apprendre à accueillir ses émotions. 


## ✨ Fonctionnalités

- **Journal personnel** : Créez et gérez vos pauses empathiques
- **Processus guidé** : Suivez les étapes de la CNV (Observation, Sentiments, Besoins)
- **Suivi émotionnel** : Identifiez vos sentiments
- **Identification des besoins** : Explorez vos besoins fondamentaux
- **Interface responsive** : Optimisée pour mobile et desktop
- **Limitation de largeur** : Lecture optimisée sur grands écrans

## 🛠️ Technologies

   ### Backend
- **Django 5.2+** : Framework web Python
- **PostgreSQL** : Base de données
- **Python 3.13+** : Langage de programmation

  ### Frontend
- **Tailwind CSS 4.1** : Framework CSS utilitaire
- **JavaScript Vanilla** : Interactions dynamiques
- **Templates Django** : Rendu côté serveur

## 💻 Outils de développement

- **Poetry** : Gestion des dépendances Python
- **Docker & Docker Compose** : Containerisation
- **Node.js** : Build tools pour Tailwind CSS

## 📁 Structure globale du projet

```
pause_empathique/
├── pause_empathique/          # Configuration Django principale
├── pauses/                    # App principale (pauses empathiques)
├── users/                     # Gestion des utilisateurs
├── templates/                 
│   ├── base.html
│   ├── header.html
│   ├── pauses/
│   └── users/
├── static/                   
│   ├── css/
│   ├── js/
│   └── icons/
├── docker-compose.yml         # Configuration Docker
├── pyproject.toml            # Configuration Poetry
├── package.json              # Dépendances Node.js
└── manage.py                 # Script de gestion Django
```

## ⌚ A venir

- [ ] Visualisation de statistiques des données
- [ ] Mise en place de tests
- [ ] Déploiement avec Railway
- [ ] Mise en place CI/CD
      
et + encore... ! 

 P+E=🤍
