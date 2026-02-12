from src.poker.hands2 import is_three_of_a_kind


def test_three_of_a_kind_basic():
    """Test qu'un brelan basique est détecté."""
    hand = ["8S", "8H"]
    board = ["8D", "JC", "QS", "2H", "3D"]
    assert is_three_of_a_kind(hand, board) is True


def test_three_of_a_kind_on_board():
    """Test brelan entièrement sur le board."""
    hand = ["AS", "KH"]
    board = ["8S", "8D", "8C", "2H", "3D"]
    assert is_three_of_a_kind(hand, board) is True


def test_three_of_a_kind_with_pair_in_hand():
    """Test brelan avec paire en main + une carte sur le board."""
    hand = ["JS", "JH"]
    board = ["JD", "QC", "KS", "2H", "3D"]
    assert is_three_of_a_kind(hand, board) is True


def test_three_of_a_kind_with_four():
    """Test qu'un carré est aussi détecté comme brelan."""
    hand = ["AS", "AH"]
    board = ["AD", "AC", "KS", "2H", "3D"]
    assert is_three_of_a_kind(hand, board) is True


def test_not_three_of_a_kind_only_pair():
    """Test qu'une simple paire n'est PAS un brelan."""
    hand = ["8S", "8H"]
    board = ["JD", "QC", "KS", "2H", "3D"]
    assert is_three_of_a_kind(hand, board) is False


def test_not_three_of_a_kind_two_pairs():
    """Test que deux paires ne sont PAS un brelan."""
    hand = ["8S", "8H"]
    board = ["JD", "JC", "KS", "2H", "3D"]
    assert is_three_of_a_kind(hand, board) is False


def test_not_three_of_a_kind_no_match():
    """Test que des cartes sans correspondance ne forment PAS un brelan."""
    hand = ["2S", "7H"]
    board = ["9S", "JD", "KC", "3H", "5D"]
    assert is_three_of_a_kind(hand, board) is False


def test_three_of_a_kind_aces():
    """Test brelan d'As."""
    hand = ["AS", "AH"]
    board = ["AD", "KC", "QS", "2H", "3D"]
    assert is_three_of_a_kind(hand, board) is True


def test_three_of_a_kind_with_full_house():
    """Test qu'un full house est aussi détecté comme brelan."""
    hand = ["AS", "AH"]
    board = ["AD", "KC", "KS", "2H", "3D"]
    assert is_three_of_a_kind(hand, board) is True


def test_three_of_a_kind_low_cards():
    """Test brelan de petites cartes."""
    hand = ["2S", "2H"]
    board = ["2D", "KC", "QS", "JH", "10D"]
    assert is_three_of_a_kind(hand, board) is True
