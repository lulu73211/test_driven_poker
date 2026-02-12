from src.poker.hands import parse_card, evaluate_hand


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
