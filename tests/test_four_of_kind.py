from src.poker.hands import is_four_of_a_kind


def test_four_of_a_kind():
    """Test qu'un carré est détecté."""
    hand = ["KS", "KH"]
    board = ["KD", "KC", "3S", "7H", "9D"]
    assert is_four_of_a_kind(hand, board) is True


def test_four_of_a_kind_on_board():
    """Test qu'un carré entièrement sur le board est détecté."""
    hand = ["2S", "3H"]
    board = ["AS", "AH", "AD", "AC", "9D"]
    assert is_four_of_a_kind(hand, board) is True


def test_not_four_of_a_kind_three():
    """Test qu'un brelan n'est PAS un carré."""
    hand = ["KS", "KH"]
    board = ["KD", "4C", "3S", "7H", "9D"]
    assert is_four_of_a_kind(hand, board) is False


def test_not_four_of_a_kind_two_pairs():
    """Test que deux paires ne sont PAS un carré."""
    hand = ["KS", "QH"]
    board = ["KD", "QC", "3S", "7H", "9D"]
    assert is_four_of_a_kind(hand, board) is False


def test_four_of_a_kind_aces():
    """Test carré d'As."""
    hand = ["AS", "AH"]
    board = ["AD", "AC", "5S", "7H", "9D"]
    assert is_four_of_a_kind(hand, board) is True
