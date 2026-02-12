from src.poker.hands import is_straight


def test_straight_basic():
    """Test qu'une quinte basique est détectée."""
    hand = ["8S", "9H"]
    board = ["10S", "JD", "QC", "2H", "3D"]
    assert is_straight(hand, board) is True


def test_straight_with_ace_high():
    """Test quinte haute avec 10-J-Q-K-A."""
    hand = ["AS", "KH"]
    board = ["QS", "JD", "10C", "2H", "3D"]
    assert is_straight(hand, board) is True


def test_straight_with_ace_low():
    """Test quinte basse avec A-2-3-4-5 (wheel)."""
    hand = ["AS", "2H"]
    board = ["3S", "4D", "5C", "KH", "QD"]
    assert is_straight(hand, board) is True


def test_not_straight_missing_one():
    """Test qu'une suite incomplète (manque une carte) n'est PAS une quinte."""
    hand = ["8S", "9H"]
    board = ["10S", "JD", "KC", "2H", "3D"]
    assert is_straight(hand, board) is False


def test_not_straight_random_cards():
    """Test que des cartes aléatoires sans suite ne forment PAS une quinte."""
    hand = ["2S", "7H"]
    board = ["9S", "JD", "KC", "3H", "5D"]
    assert is_straight(hand, board) is False


def test_straight_with_duplicates():
    """Test quinte avec des doublons (7 cartes dont 2 paires)."""
    hand = ["8S", "8H"]
    board = ["9S", "10D", "JC", "QH", "KD"]
    assert is_straight(hand, board) is True


def test_straight_using_both_hole_cards():
    """Test quinte utilisant les 2 cartes de la main."""
    hand = ["6S", "7H"]
    board = ["8S", "9D", "10C", "2H", "3D"]
    assert is_straight(hand, board) is True


def test_straight_using_one_hole_card():
    """Test quinte utilisant 1 seule carte de la main."""
    hand = ["5S", "2H"]
    board = ["6S", "7D", "8C", "9H", "KD"]
    assert is_straight(hand, board) is True


def test_straight_using_no_hole_cards():
    """Test quinte entièrement sur le board."""
    hand = ["2S", "3H"]
    board = ["8S", "9D", "10C", "JH", "QD"]
    assert is_straight(hand, board) is True


def test_straight_six_consecutive():
    """Test avec 6 cartes consécutives (doit détecter la quinte)."""
    hand = ["7S", "8H"]
    board = ["9S", "10D", "JC", "QH", "2D"]
    assert is_straight(hand, board) is True


def test_straight_seven_consecutive():
    """Test avec 7 cartes consécutives (doit détecter la quinte)."""
    hand = ["7S", "8H"]
    board = ["9S", "10D", "JC", "QH", "KD"]
    assert is_straight(hand, board) is True
