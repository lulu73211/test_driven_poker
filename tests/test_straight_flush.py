from src.poker.hands import is_straight_flush


def test_straight_flush():
    """Test qu'une main + board formant une quinte flush est détectée."""
    hand = ["8S", "9S"]
    board = ["10S", "JS", "QS", "2H", "3D"]
    assert is_straight_flush(hand, board) is True


def test_not_straight_flush_different_suits():
    """Test qu'une suite avec des couleurs différentes n'est PAS une quinte flush."""
    hand = ["8S", "9H"]
    board = ["10S", "JS", "QS", "2H", "3D"]
    assert is_straight_flush(hand, board) is False


def test_not_straight_flush_no_straight():
    """Test qu'une flush sans suite n'est PAS une quinte flush."""
    hand = ["2S", "9S"]
    board = ["10S", "JS", "QS", "4H", "3D"]
    assert is_straight_flush(hand, board) is False


def test_straight_flush_ace_low():
    """Test quinte flush basse avec A-2-3-4-5 (wheel)."""
    hand = ["AS", "2S"]
    board = ["3S", "4S", "5S", "KH", "QD"]
    assert is_straight_flush(hand, board) is True


def test_royal_flush():
    """Test quinte flush royale (10-J-Q-K-A même couleur)."""
    hand = ["AS", "KS"]
    board = ["QS", "JS", "10S", "2H", "3D"]
    assert is_straight_flush(hand, board) is True
