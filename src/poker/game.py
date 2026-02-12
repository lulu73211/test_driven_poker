from src.poker.hands import parse_card, evaluate_hand

# Rang des catégories de mains (plus élevé = meilleur)
HAND_RANKINGS = {
    "High Card": 1,
    "One Pair": 2,
    "Two Pair": 3,
    "Three of a Kind": 4,
    "Straight": 5,
    "Flush": 6,
    "Full House": 7,
    "Four of a Kind": 8,
    "Straight Flush": 9,
}


def _group_by_value(all_cards: list[str]) -> dict[int, list[str]]:
    """Groupe les cartes par valeur, en préservant l'ordre d'apparition."""
    groups: dict[int, list[str]] = {}
    for card in all_cards:
        value, _ = parse_card(card)
        groups.setdefault(value, []).append(card)
    return groups


def _group_by_suit(all_cards: list[str]) -> dict[str, list[str]]:
    """Groupe les cartes par couleur."""
    groups: dict[str, list[str]] = {}
    for card in all_cards:
        _, suit = parse_card(card)
        groups.setdefault(suit, []).append(card)
    return groups


def _sort_descending(cards: list[str]) -> list[str]:
    """Trie les cartes par valeur décroissante."""
    return sorted(cards, key=lambda c: parse_card(c)[0], reverse=True)


def _find_best_straight(cards: list[str]) -> list[str]:
    """Trouve la meilleure quinte parmi les cartes données.
    Retourne les 5 cartes dans l'ordre croissant, ou une liste vide."""
    card_values = [(parse_card(c)[0], c) for c in cards]

    # Gérer l'As comme valeur basse (1)
    ace_entries = [(1, c) for v, c in card_values if v == 14]
    card_values = card_values + ace_entries

    # Trier par valeur croissante
    card_values.sort(key=lambda x: x[0])

    # Garder une seule carte par valeur (la première rencontrée)
    seen: set[int] = set()
    unique: list[tuple[int, str]] = []
    for v, c in card_values:
        if v not in seen:
            seen.add(v)
            unique.append((v, c))

    # Trouver la plus longue suite consécutive
    best_run: list[tuple[int, str]] = []
    current_run: list[tuple[int, str]] = [unique[0]]
    for i in range(1, len(unique)):
        if unique[i][0] == unique[i - 1][0] + 1:
            current_run.append(unique[i])
        else:
            if len(current_run) > len(best_run):
                best_run = list(current_run)
            current_run = [unique[i]]
    if len(current_run) > len(best_run):
        best_run = current_run

    if len(best_run) >= 5:
        # Prendre les 5 plus hautes de la suite
        return [c for _, c in best_run[-5:]]
    return []


def _pick_straight_flush(all_cards: list[str]) -> list[str]:
    suit_groups = _group_by_suit(all_cards)
    for suit, cards in suit_groups.items():
        if len(cards) >= 5:
            result = _find_best_straight(cards)
            if result:
                return result
    return []


def _pick_four_of_a_kind(all_cards: list[str]) -> list[str]:
    groups = _group_by_value(all_cards)
    four: list[str] = []
    kickers: list[str] = []
    for value in sorted(groups.keys(), reverse=True):
        cards = groups[value]
        if len(cards) >= 4 and not four:
            four = cards[:4]
        else:
            kickers.extend(cards)
    kickers = _sort_descending(kickers)
    return four + [kickers[0]]


def _pick_full_house(all_cards: list[str]) -> list[str]:
    groups = _group_by_value(all_cards)
    three: list[str] = []
    pair: list[str] = []
    for value in sorted(groups.keys(), reverse=True):
        cards = groups[value]
        if len(cards) >= 3 and not three:
            three = cards[:3]
        elif len(cards) >= 2 and not pair:
            pair = cards[:2]
    return three + pair


def _pick_flush(all_cards: list[str]) -> list[str]:
    suit_groups = _group_by_suit(all_cards)
    for suit, cards in suit_groups.items():
        if len(cards) >= 5:
            # Trier par valeur croissante et prendre les 5 plus hautes
            sorted_asc = sorted(cards, key=lambda c: parse_card(c)[0])
            return sorted_asc[-5:]
    return []


def _pick_straight(all_cards: list[str]) -> list[str]:
    return _find_best_straight(all_cards)


def _pick_three_of_a_kind(all_cards: list[str]) -> list[str]:
    groups = _group_by_value(all_cards)
    three: list[str] = []
    kickers: list[str] = []
    for value in sorted(groups.keys(), reverse=True):
        cards = groups[value]
        if len(cards) >= 3 and not three:
            three = cards[:3]
        else:
            kickers.extend(cards)
    kickers = _sort_descending(kickers)
    return three + kickers[:2]


def _pick_two_pair(all_cards: list[str]) -> list[str]:
    groups = _group_by_value(all_cards)
    pairs: list[list[str]] = []
    kickers: list[str] = []
    for value in sorted(groups.keys(), reverse=True):
        cards = groups[value]
        if len(cards) >= 2 and len(pairs) < 2:
            pairs.append(cards[:2])
        else:
            kickers.extend(cards)
    kickers = _sort_descending(kickers)
    return pairs[0] + pairs[1] + [kickers[0]]


def _pick_one_pair(all_cards: list[str]) -> list[str]:
    groups = _group_by_value(all_cards)
    pair: list[str] = []
    kickers: list[str] = []
    for value in sorted(groups.keys(), reverse=True):
        cards = groups[value]
        if len(cards) >= 2 and not pair:
            pair = cards[:2]
        else:
            kickers.extend(cards)
    kickers = _sort_descending(kickers)
    return pair + kickers[:3]


def _pick_high_card(all_cards: list[str]) -> list[str]:
    return _sort_descending(all_cards)[:5]


def best_five(hand: list[str], board: list[str]) -> tuple[str, list[str]]:
    """Retourne le nom de la meilleure main et les 5 cartes qui la composent.

    Returns:
        Un tuple (nom_de_la_main, [5 meilleures cartes dans l'ordre]).
    """
    hand_name = evaluate_hand(hand, board)
    all_cards = hand + board

    pickers = {
        "Straight Flush": _pick_straight_flush,
        "Four of a Kind": _pick_four_of_a_kind,
        "Full House": _pick_full_house,
        "Flush": _pick_flush,
        "Straight": _pick_straight,
        "Three of a Kind": _pick_three_of_a_kind,
        "Two Pair": _pick_two_pair,
        "One Pair": _pick_one_pair,
        "High Card": _pick_high_card,
    }

    cards = pickers[hand_name](all_cards)
    return (hand_name, cards)


def _get_card_values(cards: list[str]) -> list[int]:
    """Retourne la liste des valeurs des cartes."""
    return [parse_card(c)[0] for c in cards]


def _is_wheel(cards: list[str]) -> bool:
    """Vérifie si une suite est un wheel (A,2,3,4,5)."""
    values = sorted(_get_card_values(cards))
    return values == [1, 2, 3, 4, 5] or values == [2, 3, 4, 5, 14]


def _compare_straight(cards1: list[str], cards2: list[str]) -> int:
    """Compare deux suites.

    La suite la plus haute gagne. Le wheel (A,2,3,4,5) vaut 5-high.
    """
    # Vérifier si c'est un wheel
    is_wheel1 = _is_wheel(cards1)
    is_wheel2 = _is_wheel(cards2)

    if is_wheel1 and is_wheel2:
        return 0  # Les deux sont des wheels
    if is_wheel1:
        return -1  # Hand 1 est un wheel (5-high), donc plus faible
    if is_wheel2:
        return 1  # Hand 2 est un wheel (5-high), donc plus faible

    # Comparer la carte la plus haute de la suite (dernière carte)
    values1 = _get_card_values(cards1)
    values2 = _get_card_values(cards2)

    high1 = max(values1)
    high2 = max(values2)

    if high1 > high2:
        return 1
    elif high1 < high2:
        return -1
    return 0


def _compare_cards_descending(cards1: list[str], cards2: list[str]) -> int:
    """Compare deux listes de cartes en ordre décroissant de valeur."""
    values1 = sorted(_get_card_values(cards1), reverse=True)
    values2 = sorted(_get_card_values(cards2), reverse=True)

    for v1, v2 in zip(values1, values2):
        if v1 > v2:
            return 1
        elif v1 < v2:
            return -1
    return 0


def _compare_by_groups(cards1: list[str], cards2: list[str]) -> int:
    """Compare deux mains en respectant l'ordre d'importance des cartes.

    Pour Four of a Kind, Full House, Three of a Kind, Two Pair, One Pair:
    les cartes sont déjà ordonnées par importance dans best_five.
    On compare donc les valeurs dans l'ordre.
    """
    values1 = _get_card_values(cards1)
    values2 = _get_card_values(cards2)

    for v1, v2 in zip(values1, values2):
        if v1 > v2:
            return 1
        elif v1 < v2:
            return -1
    return 0


def compare_hands(hand1: tuple[str, list[str]], hand2: tuple[str, list[str]]) -> int:
    """Compare deux mains de poker.

    Args:
        hand1: tuple (nom_de_la_main, [5 cartes])
        hand2: tuple (nom_de_la_main, [5 cartes])

    Returns:
        1 si hand1 gagne, 2 si hand2 gagne, 0 en cas d'égalité.
    """
    name1, cards1 = hand1
    name2, cards2 = hand2

    rank1 = HAND_RANKINGS[name1]
    rank2 = HAND_RANKINGS[name2]

    # Comparer d'abord les catégories
    if rank1 > rank2:
        return 1
    elif rank1 < rank2:
        return 2

    # Même catégorie : tie-break
    if name1 in ["Straight", "Straight Flush"]:
        result = _compare_straight(cards1, cards2)
    elif name1 == "Flush" or name1 == "High Card":
        result = _compare_cards_descending(cards1, cards2)
    else:
        # Four of a Kind, Full House, Three of a Kind, Two Pair, One Pair
        result = _compare_by_groups(cards1, cards2)

    if result > 0:
        return 1
    elif result < 0:
        return 2
    return 0
