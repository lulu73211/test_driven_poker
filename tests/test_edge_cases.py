"""Tests des cas limites mentionnés dans l'énoncé (section 7).

Ces tests correspondent exactement aux exemples A, B, C, D, E de l'énoncé.
Ils valident les cas particuliers importants du poker Texas Hold'em.
"""
from src.poker.game import best_five, determine_winner


# Example A — Ace-low straight (wheel)
def test_example_a_ace_low_straight_wheel():
    """Example A de l'énoncé: Ace-low straight (wheel).

    Board: A♣ 2♦ 3♥ 4♠ 9♦
    Player: 5♣ K♦
    Best: Straight (5-high), chosen5: 5♣ 4♠ 3♥ 2♦ A♣
    """
    board = ["AC", "2D", "3H", "4S", "9D"]
    hand = ["5C", "KD"]

    hand_name, cards = best_five(hand, board)

    assert hand_name == "Straight"
    # Vérifier que les 5 cartes de la suite sont présentes
    card_values = [c[:-1] for c in cards]  # Extraire les valeurs
    assert set(card_values) == {"A", "2", "3", "4", "5"}


# Example B — Ace-high straight
def test_example_b_ace_high_straight():
    """Example B de l'énoncé: Ace-high straight.

    Board: 10♣ J♦ Q♥ K♠ 2♦
    Player: A♣ 3♦
    Best: Straight (A-high), chosen5: A♣ K♠ Q♥ J♦ 10♣
    """
    board = ["10C", "JD", "QH", "KS", "2D"]
    hand = ["AC", "3D"]

    hand_name, cards = best_five(hand, board)

    assert hand_name == "Straight"
    # Vérifier que les 5 cartes de la suite sont présentes
    card_values = [c[:-1] for c in cards]  # Extraire les valeurs
    assert set(card_values) == {"A", "K", "Q", "J", "10"}


# Example C — Flush with more than 5 suited cards available
def test_example_c_flush_with_more_than_5_suited_cards():
    """Example C de l'énoncé: Flush avec plus de 5 cartes de même couleur.

    Board: A♥ J♥ 9♥ 4♥ 2♣
    Player: 6♥ K♦
    Best: Flush, chosen5 doit être les 5 meilleurs cœurs: A♥ J♥ 9♥ 6♥ 4♥
    """
    board = ["AH", "JH", "9H", "4H", "2C"]
    hand = ["6H", "KD"]

    hand_name, cards = best_five(hand, board)

    assert hand_name == "Flush"
    # Toutes les cartes doivent être des cœurs
    assert all(c.endswith("H") for c in cards)
    # Les 5 meilleurs cœurs sont A, J, 9, 6, 4
    card_values = [c[:-1] for c in cards]  # Extraire les valeurs
    assert set(card_values) == {"A", "J", "9", "6", "4"}


# Example D — Board plays (tie)
def test_example_d_board_plays_tie():
    """Example D de l'énoncé: Board plays (égalité).

    Board: 5♣ 6♦ 7♥ 8♠ 9♦ (suite sur le board)
    Player1: A♣ A♦
    Player2: K♣ Q♦
    Best pour les deux: Straight (9-high), chosen5: 9♦ 8♠ 7♥ 6♦ 5♣
    Résultat: Égalité
    """
    board = ["5C", "6D", "7H", "8S", "9D"]
    players = [
        {"name": "Player1", "hand": ["AC", "AD"]},
        {"name": "Player2", "hand": ["KC", "QD"]},
    ]

    # Vérifier que les deux joueurs ont une suite
    hand1_name, hand1_cards = best_five(players[0]["hand"], board)
    hand2_name, hand2_cards = best_five(players[1]["hand"], board)

    assert hand1_name == "Straight"
    assert hand2_name == "Straight"

    # Les deux doivent avoir la même suite
    card1_values = set(c[:-1] for c in hand1_cards)
    card2_values = set(c[:-1] for c in hand2_cards)
    assert card1_values == {"5", "6", "7", "8", "9"}
    assert card2_values == {"5", "6", "7", "8", "9"}

    # Vérifier l'égalité avec determine_winner
    winners = determine_winner(board, players)
    assert len(winners) == 2


# Example E — Quads on board, kicker decides
def test_example_e_quads_on_board_kicker_decides():
    """Example E de l'énoncé: Carré sur le board, le kicker décide.

    Board: 7♣ 7♦ 7♥ 7♠ 2♦
    Player1: A♣ K♣
    Player2: Q♣ J♣
    Best: Four of a Kind (7s) pour les deux
    Player1 gagne (kicker A vs kicker Q)
    """
    board = ["7C", "7D", "7H", "7S", "2D"]
    players = [
        {"name": "Player1", "hand": ["AC", "KC"]},
        {"name": "Player2", "hand": ["QC", "JC"]},
    ]

    # Vérifier que les deux ont un carré
    hand1_name, hand1_cards = best_five(players[0]["hand"], board)
    hand2_name, hand2_cards = best_five(players[1]["hand"], board)

    assert hand1_name == "Four of a Kind"
    assert hand2_name == "Four of a Kind"

    # Player1 doit gagner avec le kicker As
    winners = determine_winner(board, players)
    assert len(winners) == 1
    assert winners[0]["name"] == "Player1"

    # Vérifier que le carré contient bien les 4 sept
    player1_values = [c[:-1] for c in hand1_cards]
    assert player1_values.count("7") == 4
    # Le kicker doit être l'As
    assert "A" in player1_values


def test_wheel_is_lowest_straight():
    """Le wheel (A-2-3-4-5) est la suite la plus faible.

    Vérifie qu'une suite 6-high bat le wheel.
    """
    board = ["2D", "3H", "4C", "5S", "10D"]
    players = [
        {"name": "WheelPlayer", "hand": ["AS", "KH"]},  # A-2-3-4-5 (wheel)
        {"name": "SixHighPlayer", "hand": ["6C", "7D"]},  # 3-4-5-6-7 (7-high straight)
    ]

    winners = determine_winner(board, players)
    assert len(winners) == 1
    assert winners[0]["name"] == "SixHighPlayer"


def test_ace_high_straight_beats_king_high():
    """Une suite A-high (10-J-Q-K-A) bat une suite K-high (9-10-J-Q-K)."""
    board = ["10D", "JC", "QS", "2H", "3D"]
    players = [
        {"name": "AceHigh", "hand": ["AS", "KH"]},  # 10-J-Q-K-A
        {"name": "KingHigh", "hand": ["9S", "KD"]},  # 9-10-J-Q-K
    ]

    winners = determine_winner(board, players)
    assert len(winners) == 1
    assert winners[0]["name"] == "AceHigh"


def test_no_wrap_around_straight():
    """Pas de suite "wrap-around" (Q-K-A-2-3 n'est pas une suite valide)."""
    board = ["QD", "KC", "AS", "2H", "3D"]
    hand = ["4S", "7H"]

    hand_name, _ = best_five(hand, board)

    # Devrait être High Card, pas une suite
    # (Q-K-A-2-3 n'est pas valide, et A-2-3-4 manque le 5)
    assert hand_name == "High Card"


def test_suits_dont_matter_for_tiebreak():
    """Les couleurs ne comptent pas pour départager (sauf pour flush).

    Deux joueurs avec la même suite mais de couleurs différentes = égalité.
    """
    board = ["5C", "6D", "7H", "8S", "9D"]
    players = [
        {"name": "Player1", "hand": ["2C", "3D"]},
        {"name": "Player2", "hand": ["2H", "3S"]},
    ]

    winners = determine_winner(board, players)
    # Les deux ont la même suite 5-6-7-8-9, donc égalité
    assert len(winners) == 2
