from src.poker.hands import is_two_pair


def test_two_pair_basic():
    """Test que deux paires basiques sont détectées."""
    hand = ["8S", "8H"]
    board = ["JD", "JC", "QS", "2H", "3D"]
    assert is_two_pair(hand, board) is True


def test_two_pair_on_board():
    """Test deux paires entièrement sur le board."""
    hand = ["AS", "KH"]
    board = ["8S", "8D", "JC", "JH", "3D"]
    assert is_two_pair(hand, board) is True


def test_two_pair_one_in_hand_one_on_board():
    """Test paire en main + paire sur le board."""
    hand = ["8S", "8H"]
    board = ["JD", "JC", "QS", "2H", "3D"]
    assert is_two_pair(hand, board) is True


def test_two_pair_split():
    """Test deux paires formées avec des cartes mixtes main/board."""
    hand = ["8S", "JH"]
    board = ["8D", "JC", "QS", "2H", "3D"]
    assert is_two_pair(hand, board) is True


def test_two_pair_with_three():
    """Test que trois paires sont aussi détectées comme deux paires."""
    hand = ["8S", "8H"]
    board = ["JD", "JC", "QS", "QH", "3D"]
    assert is_two_pair(hand, board) is True


def test_two_pair_with_full_house():
    """Test qu'un full house est aussi détecté comme deux paires (brelan compte comme paire)."""
    hand = ["AS", "AH"]
    board = ["AD", "KC", "KS", "2H", "3D"]
    assert is_two_pair(hand, board) is True


def test_two_pair_with_four_of_kind():
    """Test qu'un carré n'est PAS détecté comme deux paires."""
    hand = ["AS", "AH"]
    board = ["AD", "AC", "KS", "2H", "3D"]
    assert is_two_pair(hand, board) is False


def test_not_two_pair_only_one():
    """Test qu'une seule paire n'est PAS deux paires."""
    hand = ["8S", "8H"]
    board = ["JD", "QC", "KS", "2H", "3D"]
    assert is_two_pair(hand, board) is False


def test_not_two_pair_no_pairs():
    """Test que des cartes sans paires ne forment PAS deux paires."""
    hand = ["2S", "7H"]
    board = ["9S", "JD", "KC", "3H", "5D"]
    assert is_two_pair(hand, board) is False


def test_two_pair_aces_and_kings():
    """Test deux paires hautes (As et Rois)."""
    hand = ["AS", "AH"]
    board = ["KD", "KC", "QS", "2H", "3D"]
    assert is_two_pair(hand, board) is True


def test_two_pair_low_cards():
    """Test deux paires de petites cartes."""
    hand = ["2S", "2H"]
    board = ["3D", "3C", "KS", "QH", "JD"]
    assert is_two_pair(hand, board) is True
