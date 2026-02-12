"""Tests pour la comparaison de deux mains de poker."""
from src.poker.game import best_five, compare_hands


def test_compare_hands_returns_1_when_hand1_wins():
    """compare_hands retourne 1 quand la main 1 gagne."""
    # Hand 1: Straight Flush
    hand1 = best_five(["8S", "9S"], ["10S", "JS", "QS", "2H", "3D"])
    # Hand 2: Four of a Kind
    hand2 = best_five(["KS", "KH"], ["KD", "KC", "AS", "7H", "3D"])

    assert compare_hands(hand1, hand2) == 1


def test_compare_hands_returns_2_when_hand2_wins():
    """compare_hands retourne 2 quand la main 2 gagne."""
    # Hand 1: One Pair
    hand1 = best_five(["KS", "2H"], ["KD", "4C", "3S", "7H", "9D"])
    # Hand 2: Two Pair
    hand2 = best_five(["KS", "QH"], ["KD", "QC", "3S", "7H", "9D"])

    assert compare_hands(hand1, hand2) == 2


def test_compare_hands_returns_0_on_tie():
    """compare_hands retourne 0 en cas d'égalité."""
    # Même main exacte
    hand1 = best_five(["AS", "KH"], ["QD", "JC", "10S", "2H", "3D"])
    hand2 = best_five(["AD", "KC"], ["QH", "JS", "10D", "4H", "5D"])

    assert compare_hands(hand1, hand2) == 0


# Tests de tie-break pour High Card
def test_compare_high_card_first_card_decides():
    """Quand deux High Card, la plus haute carte décide."""
    # Hand 1: A high
    hand1 = best_five(["AS", "KH"], ["QD", "JC", "9S", "2H", "3D"])
    # Hand 2: K high (pas de suite)
    hand2 = best_five(["KS", "QH"], ["JD", "9C", "7D", "2C", "3H"])

    assert compare_hands(hand1, hand2) == 1


def test_compare_high_card_second_card_decides():
    """Si la première carte est égale, la deuxième décide."""
    # Hand 1: A, K, Q, J, 9
    hand1 = best_five(["AS", "KH"], ["QD", "JC", "9S", "2H", "3D"])
    # Hand 2: A, K, Q, J, 8
    hand2 = best_five(["AD", "KC"], ["QH", "JS", "8D", "2C", "3H"])

    assert compare_hands(hand1, hand2) == 1


# Tests de tie-break pour One Pair
def test_compare_one_pair_by_pair_rank():
    """Quand deux paires, comparer d'abord le rang de la paire."""
    # Hand 1: Pair of Kings
    hand1 = best_five(["KS", "KH"], ["QD", "JC", "9S", "2H", "3D"])
    # Hand 2: Pair of Queens
    hand2 = best_five(["QS", "QH"], ["KD", "JD", "9D", "2C", "3H"])

    assert compare_hands(hand1, hand2) == 1


def test_compare_one_pair_by_first_kicker():
    """Si les paires sont égales, comparer le premier kicker."""
    # Hand 1: Pair of Kings, A kicker
    hand1 = best_five(["KS", "KH"], ["AD", "JC", "9S", "2H", "3D"])
    # Hand 2: Pair of Kings, Q kicker
    hand2 = best_five(["KD", "KC"], ["QD", "JD", "9D", "2C", "3H"])

    assert compare_hands(hand1, hand2) == 1


# Tests de tie-break pour Two Pair
def test_compare_two_pair_by_higher_pair():
    """Quand deux double-paires, comparer d'abord la paire la plus haute."""
    # Hand 1: KK and QQ
    hand1 = best_five(["KS", "KH"], ["QD", "QC", "9S", "2H", "3D"])
    # Hand 2: QQ and JJ
    hand2 = best_five(["QS", "QH"], ["JD", "JC", "AS", "2C", "3H"])

    assert compare_hands(hand1, hand2) == 1


def test_compare_two_pair_by_lower_pair():
    """Si les paires hautes sont égales, comparer la paire basse."""
    # Hand 1: KK and QQ
    hand1 = best_five(["KS", "KH"], ["QD", "QC", "9S", "2H", "3D"])
    # Hand 2: KK and JJ
    hand2 = best_five(["KD", "KC"], ["JD", "JC", "AS", "2C", "3H"])

    assert compare_hands(hand1, hand2) == 1


def test_compare_two_pair_by_kicker():
    """Si les deux paires sont égales, comparer le kicker."""
    # Hand 1: KK and QQ, A kicker
    hand1 = best_five(["KS", "KH"], ["QD", "QC", "AS", "2H", "3D"])
    # Hand 2: KK and QQ, J kicker
    hand2 = best_five(["KD", "KC"], ["QS", "QH", "JS", "2C", "3H"])

    assert compare_hands(hand1, hand2) == 1


# Tests de tie-break pour Straight
def test_compare_straight_by_high_card():
    """Quand deux suites, comparer la carte la plus haute."""
    # Hand 1: 9-high straight
    hand1 = best_five(["8S", "9H"], ["10D", "JC", "QS", "2H", "3D"])
    # Hand 2: 8-high straight
    hand2 = best_five(["7S", "8H"], ["9D", "10C", "JS", "2C", "3H"])

    assert compare_hands(hand1, hand2) == 1


def test_compare_straight_ace_high_vs_king_high():
    """A-high straight gagne contre K-high straight."""
    # Hand 1: A-high straight (10, J, Q, K, A)
    hand1 = best_five(["AS", "KH"], ["QD", "JC", "10S", "2H", "3D"])
    # Hand 2: K-high straight (9, 10, J, Q, K)
    hand2 = best_five(["9S", "10H"], ["JD", "QC", "KS", "2C", "3H"])

    assert compare_hands(hand1, hand2) == 1


def test_compare_straight_six_high_vs_wheel():
    """6-high straight gagne contre wheel (5-high)."""
    # Hand 1: 6-high straight (2, 3, 4, 5, 6)
    hand1 = best_five(["2S", "3H"], ["4D", "5C", "6S", "KH", "QD"])
    # Hand 2: Wheel (A, 2, 3, 4, 5) - 5-high
    hand2 = best_five(["AS", "2H"], ["3D", "4C", "5S", "KD", "QC"])

    assert compare_hands(hand1, hand2) == 1


# Tests de tie-break pour Flush
def test_compare_flush_by_highest_card():
    """Quand deux flush, comparer la carte la plus haute."""
    # Hand 1: A-high flush
    hand1 = best_five(["AS", "KS"], ["QS", "JS", "9S", "2H", "3D"])
    # Hand 2: K-high flush (pas de suite)
    hand2 = best_five(["KH", "QH"], ["JH", "9H", "7H", "2S", "3S"])

    assert compare_hands(hand1, hand2) == 1


# Tests de tie-break pour Full House
def test_compare_full_house_by_triplet():
    """Quand deux full house, comparer d'abord le brelan."""
    # Hand 1: KKK + QQ
    hand1 = best_five(["KS", "KH"], ["KD", "QC", "QS", "2H", "3D"])
    # Hand 2: QQQ + KK
    hand2 = best_five(["QD", "QH"], ["QC", "KS", "KD", "2C", "3H"])

    assert compare_hands(hand1, hand2) == 1


def test_compare_full_house_by_pair():
    """Si les brelans sont égaux, comparer la paire."""
    # Hand 1: KKK + QQ
    hand1 = best_five(["KS", "KH"], ["KD", "QC", "QS", "2H", "3D"])
    # Hand 2: KKK + JJ
    hand2 = best_five(["KD", "KC"], ["KH", "JS", "JD", "2C", "3H"])

    assert compare_hands(hand1, hand2) == 1


# Tests de tie-break pour Four of a Kind
def test_compare_four_of_kind_by_quads():
    """Quand deux carrés, comparer d'abord le rang du carré."""
    # Hand 1: KKKK + A
    hand1 = best_five(["KS", "KH"], ["KD", "KC", "AS", "2H", "3D"])
    # Hand 2: QQQQ + A
    hand2 = best_five(["QS", "QH"], ["QD", "QC", "AS", "2C", "3H"])

    assert compare_hands(hand1, hand2) == 1


def test_compare_four_of_kind_by_kicker():
    """Si les carrés sont égaux, comparer le kicker."""
    # Hand 1: KKKK + A
    hand1 = best_five(["KS", "KH"], ["KD", "KC", "AS", "2H", "3D"])
    # Hand 2: KKKK + Q
    hand2 = best_five(["KD", "KC"], ["KH", "KS", "QS", "2C", "3H"])

    assert compare_hands(hand1, hand2) == 1


# Tests de tie-break pour Three of a Kind
def test_compare_three_of_kind_by_triplet():
    """Quand deux brelans, comparer d'abord le rang du brelan."""
    # Hand 1: KKK + A, Q
    hand1 = best_five(["KS", "KH"], ["KD", "AC", "QS", "2H", "3D"])
    # Hand 2: QQQ + A, K
    hand2 = best_five(["QS", "QH"], ["QD", "AC", "KS", "2C", "3H"])

    assert compare_hands(hand1, hand2) == 1


def test_compare_three_of_kind_by_first_kicker():
    """Si les brelans sont égaux, comparer le premier kicker."""
    # Hand 1: KKK + A, Q
    hand1 = best_five(["KS", "KH"], ["KD", "AC", "QS", "2H", "3D"])
    # Hand 2: KKK + Q, J
    hand2 = best_five(["KD", "KC"], ["KH", "QD", "JS", "2C", "3H"])

    assert compare_hands(hand1, hand2) == 1


# Tests de tie-break pour Straight Flush
def test_compare_straight_flush_by_high_card():
    """Quand deux quintes flush, comparer la carte la plus haute."""
    # Hand 1: 9-high straight flush
    hand1 = best_five(["8S", "9S"], ["10S", "JS", "QS", "2H", "3D"])
    # Hand 2: 8-high straight flush
    hand2 = best_five(["7H", "8H"], ["9H", "10H", "JH", "2S", "3S"])

    assert compare_hands(hand1, hand2) == 1
