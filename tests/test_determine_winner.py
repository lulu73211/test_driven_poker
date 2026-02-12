"""Tests pour déterminer le gagnant parmi plusieurs joueurs."""
from src.poker.game import determine_winner


def test_determine_winner_single_winner():
    """Un seul gagnant parmi plusieurs joueurs."""
    board = ["10S", "JS", "QS", "2H", "3D"]
    players = [
        {"name": "Alice", "hand": ["8S", "9S"]},  # Straight Flush
        {"name": "Bob", "hand": ["KS", "KH"]},    # Pair of Kings
        {"name": "Charlie", "hand": ["AS", "KD"]}, # High card Ace
    ]

    result = determine_winner(board, players)

    assert len(result) == 1
    assert result[0]["name"] == "Alice"


def test_determine_winner_tie_between_two_players():
    """Égalité entre deux joueurs (board plays)."""
    board = ["5C", "6D", "7H", "8S", "9D"]  # Straight on board
    players = [
        {"name": "Alice", "hand": ["AC", "AD"]},  # Has pair but board is better
        {"name": "Bob", "hand": ["KC", "QD"]},    # Has high cards but board is better
    ]

    result = determine_winner(board, players)

    assert len(result) == 2
    names = [p["name"] for p in result]
    assert "Alice" in names
    assert "Bob" in names


def test_determine_winner_tie_between_three_players():
    """Égalité entre trois joueurs."""
    board = ["AS", "KS", "QS", "JS", "10S"]  # Royal Flush on board
    players = [
        {"name": "Alice", "hand": ["2C", "3D"]},
        {"name": "Bob", "hand": ["4C", "5D"]},
        {"name": "Charlie", "hand": ["6C", "7D"]},
    ]

    result = determine_winner(board, players)

    assert len(result) == 3


def test_determine_winner_with_two_players():
    """Deux joueurs, un gagnant clair."""
    board = ["KD", "KC", "3S", "7H", "9D"]
    players = [
        {"name": "Alice", "hand": ["KS", "KH"]},  # Four of a Kind
        {"name": "Bob", "hand": ["AS", "AD"]},    # Two Pair (Aces and Kings)
    ]

    result = determine_winner(board, players)

    assert len(result) == 1
    assert result[0]["name"] == "Alice"


def test_determine_winner_quads_on_board_kicker_decides():
    """Carré sur le board, le kicker décide (exemple D de l'énoncé)."""
    board = ["7C", "7D", "7H", "7S", "2D"]
    players = [
        {"name": "Alice", "hand": ["AC", "KC"]},  # Quads + Ace kicker
        {"name": "Bob", "hand": ["QC", "JC"]},    # Quads + Queen kicker
    ]

    result = determine_winner(board, players)

    assert len(result) == 1
    assert result[0]["name"] == "Alice"


def test_determine_winner_best_flush_from_six_cards():
    """Flush avec plus de 5 cartes disponibles (exemple C de l'énoncé)."""
    board = ["AH", "JH", "9H", "4H", "2C"]
    players = [
        {"name": "Alice", "hand": ["6H", "KD"]},  # Flush A-J-9-6-4
        {"name": "Bob", "hand": ["3H", "QD"]},    # Flush A-J-9-4-3
    ]

    result = determine_winner(board, players)

    assert len(result) == 1
    assert result[0]["name"] == "Alice"


def test_determine_winner_ace_high_vs_ace_low_straight():
    """Ace-high straight gagne contre wheel."""
    board = ["2D", "3H", "4C", "5S", "10D"]
    players = [
        {"name": "Alice", "hand": ["AS", "KH"]},  # Ace-low straight (wheel)
        {"name": "Bob", "hand": ["6C", "7D"]},    # 7-high straight
    ]

    result = determine_winner(board, players)

    assert len(result) == 1
    assert result[0]["name"] == "Bob"


def test_determine_winner_returns_player_info():
    """Le résultat contient les informations du joueur."""
    board = ["10S", "JS", "QS", "2H", "3D"]
    players = [
        {"name": "Alice", "hand": ["8S", "9S"]},
    ]

    result = determine_winner(board, players)

    assert len(result) == 1
    assert "name" in result[0]
    assert "hand" in result[0]
    assert result[0]["name"] == "Alice"
    assert result[0]["hand"] == ["8S", "9S"]


def test_determine_winner_includes_best_hand_info():
    """Le résultat inclut les informations sur la meilleure main."""
    board = ["10S", "JS", "QS", "2H", "3D"]
    players = [
        {"name": "Alice", "hand": ["8S", "9S"]},
    ]

    result = determine_winner(board, players)

    assert len(result) == 1
    assert "best_hand" in result[0]
    assert "hand_name" in result[0]["best_hand"]
    assert "cards" in result[0]["best_hand"]
    assert result[0]["best_hand"]["hand_name"] == "Straight Flush"
    assert len(result[0]["best_hand"]["cards"]) == 5


def test_determine_winner_four_players_with_tie():
    """Quatre joueurs avec une égalité partielle."""
    board = ["KD", "KC", "KS", "7H", "7D"]  # Full house Kings over 7s
    players = [
        {"name": "Alice", "hand": ["2C", "3D"]},  # Full house K-K-K-7-7
        {"name": "Bob", "hand": ["4C", "5D"]},    # Full house K-K-K-7-7
        {"name": "Charlie", "hand": ["KH", "6C"]}, # Four of a Kind Kings
        {"name": "Dave", "hand": ["AS", "AD"]},   # Full house K-K-K-A-A
    ]

    result = determine_winner(board, players)

    assert len(result) == 1
    assert result[0]["name"] == "Charlie"


def test_determine_winner_tie_with_different_suits():
    """Égalité malgré des couleurs différentes (les couleurs ne comptent pas)."""
    board = ["KD", "QC", "JS", "10H", "9D"]  # K-high straight
    players = [
        {"name": "Alice", "hand": ["2C", "3D"]},  # Same straight
        {"name": "Bob", "hand": ["2H", "3S"]},    # Same straight
    ]

    result = determine_winner(board, players)

    assert len(result) == 2


def test_determine_winner_single_player():
    """Un seul joueur (gagne automatiquement)."""
    board = ["10S", "JS", "QS", "2H", "3D"]
    players = [
        {"name": "Alice", "hand": ["8S", "9S"]},
    ]

    result = determine_winner(board, players)

    assert len(result) == 1
    assert result[0]["name"] == "Alice"


def test_determine_winner_with_high_card_tiebreak():
    """Départage sur High Card avec plusieurs kickers."""
    board = ["2D", "5C", "8H", "JD", "3S"]
    players = [
        {"name": "Alice", "hand": ["AS", "KH"]},  # A-K-J-8-5
        {"name": "Bob", "hand": ["AD", "QC"]},    # A-Q-J-8-5
    ]

    result = determine_winner(board, players)

    assert len(result) == 1
    assert result[0]["name"] == "Alice"


def test_determine_winner_pair_vs_pair_kicker_decides():
    """Même paire, le kicker décide."""
    board = ["KD", "KC", "5C", "8H", "3S"]
    players = [
        {"name": "Alice", "hand": ["AS", "2H"]},  # Pair K + A kicker
        {"name": "Bob", "hand": ["QD", "JC"]},    # Pair K + Q kicker
    ]

    result = determine_winner(board, players)

    assert len(result) == 1
    assert result[0]["name"] == "Alice"
