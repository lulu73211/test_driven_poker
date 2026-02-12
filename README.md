# Texas Hold'em Poker Hand Evaluator

Évaluateur de mains de poker Texas Hold'em développé en TDD (Test-Driven Development).

## 📋 Description

Ce projet implémente un évaluateur complet de mains de poker Texas Hold'em qui :
- Détermine la meilleure main de 5 cartes parmi 7 cartes disponibles (2 hole cards + 5 board cards)
- Compare les mains selon les règles officielles du poker
- Détermine le(s) gagnant(s) parmi plusieurs joueurs
- Gère les égalités (split pot)

## 🎯 Fonctionnalités

### 1. Évaluation des catégories de mains
Détection de toutes les catégories de mains, de la plus forte à la plus faible :
1. **Straight Flush** - Quinte flush (5 cartes consécutives de même couleur)
2. **Four of a Kind** - Carré (4 cartes de même valeur)
3. **Full House** - Full (brelan + paire)
4. **Flush** - Couleur (5 cartes de même couleur)
5. **Straight** - Suite (5 cartes consécutives)
6. **Three of a Kind** - Brelan (3 cartes de même valeur)
7. **Two Pair** - Double paire
8. **One Pair** - Paire
9. **High Card** - Carte haute

### 2. Sélection des 5 meilleures cartes
La fonction `best_five()` retourne :
- La catégorie de la main
- Les 5 cartes choisies (dans un ordre logique)

### 3. Comparaison de mains (Tie-breaks)
Règles de départage quand deux mains ont la même catégorie :
- **Straight/Straight Flush** : Carte la plus haute (wheel = 5-high)
- **Four of a Kind** : Rang du carré, puis kicker
- **Full House** : Rang du brelan, puis rang de la paire
- **Flush** : Comparaison des 5 cartes en ordre décroissant
- **Three of a Kind** : Rang du brelan, puis kickers
- **Two Pair** : Paire haute, paire basse, puis kicker
- **One Pair** : Rang de la paire, puis 3 kickers
- **High Card** : Comparaison des 5 cartes en ordre décroissant

### 4. Détermination du gagnant
La fonction `determine_winner()` :
- Accepte plusieurs joueurs
- Retourne le(s) gagnant(s) avec leurs informations complètes
- Gère les égalités (plusieurs gagnants possibles)

## 📝 Format des cartes

Les cartes sont représentées par des chaînes de caractères :
- **Valeurs** : `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `J`, `Q`, `K`, `A`
- **Couleurs** : `S` (Spades/Pique), `H` (Hearts/Cœur), `D` (Diamonds/Carreau), `C` (Clubs/Trèfle)

**Exemples** : `AS` (As de pique), `10H` (10 de cœur), `KD` (Roi de carreau)

## 🚀 Utilisation

### Évaluer une main
```python
from src.poker.hands import evaluate_hand

hand = ["AS", "KH"]  # As de pique, Roi de cœur
board = ["QD", "JC", "10S", "2H", "3D"]  # 5 cartes communes

category = evaluate_hand(hand, board)
print(category)  # "Straight"
```

### Obtenir les 5 meilleures cartes
```python
from src.poker.game import best_five

hand = ["AS", "KH"]
board = ["QD", "JC", "10S", "2H", "3D"]

category, cards = best_five(hand, board)
print(category)  # "Straight"
print(cards)     # Les 5 cartes de la suite
```

### Comparer deux mains
```python
from src.poker.game import best_five, compare_hands

hand1 = best_five(["AS", "KH"], ["QD", "JC", "10S", "2H", "3D"])
hand2 = best_five(["9S", "8H"], ["7D", "6C", "5S", "2H", "3D"])

result = compare_hands(hand1, hand2)
# result = 1 si hand1 gagne
# result = 2 si hand2 gagne
# result = 0 en cas d'égalité
```

### Déterminer le gagnant parmi plusieurs joueurs
```python
from src.poker.game import determine_winner

board = ["10S", "JS", "QS", "2H", "3D"]
players = [
    {"name": "Alice", "hand": ["8S", "9S"]},   # Straight Flush
    {"name": "Bob", "hand": ["KS", "KH"]},     # Pair of Kings
    {"name": "Charlie", "hand": ["AS", "KD"]}, # High card Ace
]

winners = determine_winner(board, players)
print(winners[0]["name"])  # "Alice"
print(winners[0]["best_hand"]["hand_name"])  # "Straight Flush"
print(winners[0]["best_hand"]["cards"])      # Les 5 cartes
```

## 🧪 Tests

Le projet contient **117 tests** couvrant tous les aspects :

### Lancer tous les tests
```bash
pytest
```

### Lancer les tests avec verbose
```bash
pytest -v
```

### Lancer les tests avec couverture
```bash
pytest --cov=src --cov-report=html
```

### Structure des tests
```
tests/
├── test_edge_cases.py          # Cas limites de l'énoncé (exemples A-E)
├── test_compare_hands.py       # Tests de tie-breaks (21 tests)
├── test_determine_winner.py    # Tests multi-joueurs (14 tests)
├── test_chosen_five.py         # Tests best_five()
├── test_evaluate_hand.py       # Tests catégories de mains
├── test_straight.py            # Tests des suites
├── test_straight_flush.py      # Tests des quintes flush
├── test_flush.py               # Tests des couleurs
├── test_four_of_kind.py        # Tests des carrés
├── test_full_house.py          # Tests des full house
├── test_three_of_a_kind.py     # Tests des brelans
├── test_two_pair.py            # Tests des doubles paires
└── test_sanity.py              # Test de base
```

## 📐 Ordre des cartes dans `chosen5`

Les 5 cartes retournées par `best_five()` sont ordonnées selon l'importance pour la catégorie :

- **Straight/Straight Flush** : Ordre croissant de la suite (ex: 5-6-7-8-9)
  - Pour le wheel (A-2-3-4-5), l'As peut être en début ou fin
- **Four of a Kind** : 4 cartes du carré, puis le kicker
- **Full House** : 3 cartes du brelan, puis 2 cartes de la paire
- **Flush** : 5 cartes en ordre croissant de valeur
- **Three of a Kind** : 3 cartes du brelan, puis 2 kickers (décroissant)
- **Two Pair** : Paire haute (2 cartes), paire basse (2 cartes), kicker
- **One Pair** : 2 cartes de la paire, puis 3 kickers (décroissant)
- **High Card** : 5 cartes en ordre décroissant

## 🎲 Cas particuliers

### Ace-low straight (Wheel)
L'As peut être utilisé comme carte basse dans une suite A-2-3-4-5 (appelée "wheel").
Cette suite vaut **5-high** et est la plus faible de toutes les suites.

```python
board = ["AC", "2D", "3H", "4S", "9D"]
hand = ["5C", "KD"]
# Résultat : Straight (5-high)
```

### Ace-high straight
L'As peut aussi être la carte haute dans une suite 10-J-Q-K-A.

```python
board = ["10C", "JD", "QH", "KS", "2D"]
hand = ["AC", "3D"]
# Résultat : Straight (A-high)
```

### Board plays
Si les 5 meilleures cartes sont toutes sur le board, tous les joueurs ont la même main (égalité).

```python
board = ["5C", "6D", "7H", "8S", "9D"]  # Suite sur le board
players = [
    {"name": "Alice", "hand": ["AC", "AD"]},
    {"name": "Bob", "hand": ["KC", "QD"]},
]
# Résultat : Égalité (les deux jouent le board)
```

### Flush avec plus de 5 cartes
Si plus de 5 cartes de la même couleur sont disponibles, les 5 plus hautes sont choisies.

```python
board = ["AH", "JH", "9H", "4H", "2C"]
hand = ["6H", "KD"]
# 5 cœurs disponibles : A, J, 9, 6, 4
# Résultat : Flush avec A-J-9-6-4
```

## 🔍 Validation des entrées

**Hypothèse actuelle** : Le code suppose qu'il n'y a pas de cartes dupliquées dans l'input.

Si vous avez besoin de valider les entrées, ajoutez une fonction de validation avant d'appeler les fonctions principales.

## 📊 Développement TDD

Ce projet a été développé en suivant strictement la méthodologie TDD :
1. ✅ **RED** : Écrire un test qui échoue
2. ✅ **GREEN** : Écrire le code minimal pour faire passer le test
3. ✅ **REFACTOR** : Améliorer le code tout en gardant les tests verts

L'historique Git montre clairement cette progression avec des commits séparant :
- L'ajout de tests
- L'implémentation des fonctionnalités
- Les refactorings

## 🛠️ Technologies

- **Python 3.12+**
- **pytest** pour les tests
- **pytest-cov** pour la couverture de code

## 📦 Installation

```bash
# Cloner le repository
git clone <url-du-repo>
cd test_driven_poker

# Installer les dépendances
pip install -r requirements.txt

# Lancer les tests
pytest
```

## 📜 Licence

Ce projet a été développé dans le cadre d'un examen TDD sur le poker Texas Hold'em.

## 👥 Contributeurs

Voir `students.txt` pour la liste des étudiants ayant participé au projet.

---

**Source des règles** : [Wikipedia - List of poker hands](https://en.wikipedia.org/wiki/List_of_poker_hands)
