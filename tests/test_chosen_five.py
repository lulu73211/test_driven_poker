from src.poker.game import best_five


def test_best_five_straight_flush():
    """Les 5 cartes d'une quinte flush doivent être retournées dans l'ordre."""
    hand = ["8S", "9S"]
    board = ["10S", "JS", "QS", "2H", "3D"]
    result = best_five(hand, board)
    assert result == ("Straight Flush", ["8S", "9S", "10S", "JS", "QS"])


def test_best_five_four_of_a_kind():
    """Le carré + la meilleure carte restante (kicker)."""
    hand = ["KS", "KH"]
    board = ["KD", "KC", "AS", "7H", "3D"]
    result = best_five(hand, board)
    assert result == ("Four of a Kind", ["KS", "KH", "KD", "KC", "AS"])


def test_best_five_full_house():
    """Le brelan + la meilleure paire."""
    hand = ["KS", "KH"]
    board = ["KD", "7C", "7S", "2H", "9D"]
    result = best_five(hand, board)
    assert result == ("Full House", ["KS", "KH", "KD", "7C", "7S"])


def test_best_five_flush():
    """Les 5 meilleures cartes de la même couleur dans l'ordre."""
    hand = ["2S", "9S"]
    board = ["10S", "JS", "QS", "4H", "3D"]
    result = best_five(hand, board)
    assert result == ("Flush", ["2S", "9S", "10S", "JS", "QS"])


def test_best_five_straight():
    """Les 5 cartes de la suite dans l'ordre."""
    hand = ["8S", "9H"]
    board = ["10D", "JC", "QS", "2H", "3D"]
    result = best_five(hand, board)
    assert result == ("Straight", ["8S", "9H", "10D", "JC", "QS"])


def test_best_five_three_of_a_kind():
    """Le brelan + les 2 meilleures cartes restantes."""
    hand = ["KS", "KH"]
    board = ["KD", "4C", "3S", "7H", "9D"]
    result = best_five(hand, board)
    assert result == ("Three of a Kind", ["KS", "KH", "KD", "9D", "7H"])


def test_best_five_two_pair():
    """Les deux paires + la meilleure carte restante."""
    hand = ["KS", "QH"]
    board = ["KD", "QC", "3S", "7H", "9D"]
    result = best_five(hand, board)
    assert result == ("Two Pair", ["KS", "KD", "QH", "QC", "9D"])


def test_best_five_one_pair():
    """La paire + les 3 meilleures cartes restantes."""
    hand = ["KS", "2H"]
    board = ["KD", "4C", "3S", "7H", "9D"]
    result = best_five(hand, board)
    assert result == ("One Pair", ["KS", "KD", "9D", "7H", "4C"])


def test_best_five_high_card():
    """Les 5 cartes les plus hautes dans l'ordre décroissant."""
    hand = ["2S", "7H"]
    board = ["10D", "JC", "QS", "4H", "3D"]
    result = best_five(hand, board)
    assert result == ("High Card", ["QS", "JC", "10D", "7H", "4H"])


def test_best_five_returns_tuple():
    """Vérifie que le retour est un tuple (nom, liste de 5 cartes)."""
    hand = ["AS", "KS"]
    board = ["QS", "JS", "10S", "2H", "3D"]
    result = best_five(hand, board)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], str)
    assert isinstance(result[1], list)
    assert len(result[1]) == 5


def test_best_five_cards_come_from_hand_and_board():
    """Vérifie que toutes les cartes retournées proviennent bien de la main + board."""
    hand = ["KS", "KH"]
    board = ["KD", "KC", "AS", "7H", "3D"]
    _, cards = best_five(hand, board)
    all_cards = hand + board
    for card in cards:
        assert card in all_cards
