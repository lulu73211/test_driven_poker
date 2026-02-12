from src.poker.hands import is_flush


def test_flush():
    """Test qu'une flush (5 cartes de même couleur) est détectée."""
    hand = ["2S", "9S"]
    board = ["10S", "JS", "QS", "4H", "3D"]
    assert is_flush(hand, board) is True


def test_flush_more_than_five():
    """Test flush avec 6 cartes de même couleur."""
    hand = ["2S", "9S"]
    board = ["10S", "JS", "QS", "4S", "3D"]
    assert is_flush(hand, board) is True


def test_not_flush_four_same_suit():
    """Test que 4 cartes de même couleur ne sont PAS une flush."""
    hand = ["2S", "9S"]
    board = ["10S", "JS", "QH", "4H", "3D"]
    assert is_flush(hand, board) is False


def test_not_flush_mixed_suits():
    """Test que des couleurs mélangées ne sont PAS une flush."""
    hand = ["2S", "9H"]
    board = ["10D", "JC", "QS", "4H", "3D"]
    assert is_flush(hand, board) is False


def test_flush_all_on_board():
    """Test flush entièrement sur le board."""
    hand = ["2H", "9D"]
    board = ["10S", "JS", "QS", "4S", "3S"]
    assert is_flush(hand, board) is True
