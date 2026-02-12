from src.poker.hands import is_full_house


def test_full_house():
    """Test qu'un full house (brelan + paire) est détecté."""
    hand = ["KS", "KH"]
    board = ["KD", "7C", "7S", "2H", "9D"]
    assert is_full_house(hand, board) is True


def test_full_house_pair_in_hand():
    """Test full house avec la paire en main et le brelan sur le board."""
    hand = ["5S", "5H"]
    board = ["JD", "JC", "JS", "2H", "9D"]
    assert is_full_house(hand, board) is True


def test_not_full_house_only_three():
    """Test qu'un brelan seul n'est PAS un full house."""
    hand = ["KS", "KH"]
    board = ["KD", "4C", "3S", "7H", "9D"]
    assert is_full_house(hand, board) is False


def test_not_full_house_two_pairs():
    """Test que deux paires ne sont PAS un full house."""
    hand = ["KS", "QH"]
    board = ["KD", "QC", "3S", "7H", "9D"]
    assert is_full_house(hand, board) is False


def test_not_full_house_only_pair():
    """Test qu'une simple paire n'est PAS un full house."""
    hand = ["KS", "2H"]
    board = ["KD", "4C", "3S", "7H", "9D"]
    assert is_full_house(hand, board) is False
