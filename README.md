# tp_251211_python

- PARTIE 1 — Bases Python en mode Game Dev (1h) = Partie1.py
- PARTIE 2 — Construire un vrai mini-jeu avec classes (1h) = Partie2.py
- PARTIE 3 — Extensions avancées (45 min) = Partie3.py + dossier asset. il faut installer : pip install pillow

Partie 3 : 

# Jeu de Combat Graphique RPG

Un jeu de combat RPG en Python avec interface graphique Tkinter. Le joueur choisit une classe, affronte une série d'ennemis puis un boss, gagne des objets et peut sauvegarder/charger sa progression.

## Description

Le jeu propose un système simple de combats au tour par tour : le joueur attaque, se soigne et subit l'attaque de l'ennemi. Après chaque victoire, le joueur choisit un objet parmi trois tirés aléatoirement, ce qui améliore ses statistiques (attaque, défense, points de vie maximum, etc.).

## Fonctionnalités

- **Interface graphique** avec Tkinter.
- **Système de classes** de personnage (Barbare, Mage, Archer) avec statistiques de départ différentes.
- **Combats au tour par tour** contre plusieurs ennemis successifs puis un boss final.
- **Objets aléatoires** après chaque victoire (armes, armures, potions, etc.).
- **Gestion des statistiques** : vie, attaque, défense, inventaire, PV max.
- **Système de cooldown** pour le soin du joueur et les compétences du boss.
- **Sauvegarde/chargement** de la partie au format JSON.
- **Suppression de sauvegardes** depuis l'interface.

## Prérequis

- Python 3.10 ou supérieur
- Aucune bibliothèque externe requise (utilise uniquement les modules standard)

## Installation

1. Cloner ou télécharger le projet
2. Vérifier que Python 3 est installé et accessible dans le PATH
3. Placer tous les fichiers du projet dans un même dossier

## Lancement du jeu

Dans un terminal ou invite de commande, à la racine du projet :

```bash
pip install pillow
python Part3-Graphique.py
```

ou, selon la configuration :

```bash
pip install pillow
python3 Part3-Graphique.py
```

Une fenêtre Tkinter s'ouvre alors avec l'écran de création de personnage.

## Comment jouer

### Création du personnage

1. Entrer un nom de personnage
2. Choisir une classe parmi celles proposées :
   - **Barbare** : 85 PV, 17 d'attaque, 5 de défense (attaquant)
   - **Mage** : 90 PV, 20 d'attaque, 5 de défense (très attaquant)
   - **Archer** : 100 PV, 15 d'attaque, 7 de défense (équilibré)
3. Cliquer sur « Nouvelle partie » pour commencer

### Pendant un combat

Utiliser les boutons pour :
- **Attaquer** : inflige des dégâts à l'ennemi basés sur votre attaque moins sa défense
- **Soigner** : rend 20 PV au joueur avec un cooldown de 3 tours
- **Quitter** : sauvegarde la partie et ferme le jeu

### Progression

- Après chaque victoire, vous récupérez vos PV au maximum
- Choisissez un objet parmi trois proposés aléatoirement
- Les objets augmentent vos statistiques (attaque, défense, PV max)
- Affrontez tous les ennemis : Gobelin → Orc → Troll → Dragon (boss final)

## Système de dégâts

Les dégâts sont calculés comme suit :

```
dégâts = max(1, attaque_attaquant + bonus_inventaire - défense_défenseur)
```

- La défense réduit les dégâts reçus
- Les objets équipés augmentent votre défense et réduisent les dégâts
- Les dégâts minimum sont toujours de 1

## Sauvegardes

- Une sauvegarde JSON est créée automatiquement après chaque combat
- Fichier sauvegardé : `sauvegarde_<nom_du_personnage>.json`
- Depuis l'écran de démarrage, vous pouvez :
  - Charger une sauvegarde en la sélectionnant
  - Supprimer une sauvegarde

## Ennemis et Boss

### Ennemis normaux

| Nom | PV | Attaque | Défense |
|-----|----|---------| --------|
| Gobelin | 50 | 12 | 5 |
| Orc | 75 | 19 | 8 |
| Troll | 120 | 28 | 12 |

### Boss

| Nom | PV | Attaque | Défense |
|-----|----|---------| --------|
| Dragon | 200 | 35 | 20 |

**Compétences du boss :**
- **Attaque simple** : inflige dégâts normaux
- **Attaque ultime** (cooldown 2 tours) : inflige 2× les dégâts normaux
- **Soin** (cooldown 3 tours) : récupère 25 PV

## Objets disponibles

Les objets générés aléatoirement incluent :

- **Épée** : +5 à +10 attaque
- **Bouclier** : +5 à +10 défense
- **Armure** : +8 à +15 défense
- **Amulette** : +3 à +8 attaque et défense
- **Potion** : +15 à +25 PV max
- **Anneau de régénération** : +8 à +15 PV max, +2 à +5 attaque
- **Cape de vitesse** : +3 à +7 attaque et défense
- **Tome de connaissance** : +5 à +9 attaque
- **Ceinture de force** : +2 à +5 attaque, +6 à +10 défense
- **Gants de précision** : +4 à +8 attaque, +1 à +4 défense

## Structure du projet

```
main.py                 # Fichier principal contenant tout le code
sauvegarde_*.json      # Fichiers de sauvegarde (générés automatiquement)
README.md              # Ce fichier
```

## Personnalisation

Plusieurs éléments peuvent être facilement modifiés dans le code :

- **Classes de personnage** : dictionnaire `CLASSES`
- **Liste des ennemis** : dans la méthode `GameEngine.__init__`
- **Stats du boss** : instance `Boss("Dragon", ...)`
- **Objets générés** : liste `types` dans la méthode `generer_objets`

## Limitations connues

- Pas de système de niveaux ou d'XP
- Les objets sont cumulés sans limite
- L'IA des ennemis est simple (attaques aléatoires pour le boss)
- Interface basique sans éléments graphiques avancés

## Licence

Ce projet est fourni à titre d'exemple pédagogique. Vous êtes libre de le modifier et de le redistribuer pour un usage non commercial.

## Auteur

Développé en Python 3 avec Tkinter
