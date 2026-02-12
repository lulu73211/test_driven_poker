from src.poker.hands import evaluate_hand


def test_evaluate_straight_flush():
    hand = ["8S", "9S"]
    board = ["10S", "JS", "QS", "2H", "3D"]
    assert evaluate_hand(hand, board) == "Straight Flush"


def test_evaluate_four_of_a_kind():
    hand = ["KS", "KH"]
    board = ["KD", "KC", "3S", "7H", "9D"]
    assert evaluate_hand(hand, board) == "Four of a Kind"


def test_evaluate_full_house():
    hand = ["KS", "KH"]
    board = ["KD", "7C", "7S", "2H", "9D"]
    assert evaluate_hand(hand, board) == "Full House"


def test_evaluate_flush():
    hand = ["2S", "9S"]
    board = ["10S", "JS", "QS", "4H", "3D"]
    assert evaluate_hand(hand, board) == "Flush"


def test_evaluate_straight():
    hand = ["8S", "9H"]
    board = ["10D", "JC", "QS", "2H", "3D"]
    assert evaluate_hand(hand, board) == "Straight"


def test_evaluate_three_of_a_kind():
    hand = ["KS", "KH"]
    board = ["KD", "4C", "3S", "7H", "9D"]
    assert evaluate_hand(hand, board) == "Three of a Kind"


def test_evaluate_two_pair():
    hand = ["KS", "QH"]
    board = ["KD", "QC", "3S", "7H", "9D"]
    assert evaluate_hand(hand, board) == "Two Pair"


def test_evaluate_one_pair():
    hand = ["KS", "2H"]
    board = ["KD", "4C", "3S", "7H", "9D"]
    assert evaluate_hand(hand, board) == "One Pair"


def test_evaluate_high_card():
    hand = ["2S", "7H"]
    board = ["10D", "JC", "QS", "4H", "3D"]
    assert evaluate_hand(hand, board) == "High Card"
