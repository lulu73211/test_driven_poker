CARD_VALUES = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
    "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13, "A": 14,
}


def parse_card(card: str) -> tuple[int, str]:
    """Parse une carte '10S' -> (10, 'S'), 'AH' -> (14, 'H')."""
    suit = card[-1]
    value = card[:-1]
    return CARD_VALUES[value], suit


def is_straight_flush(hand: list[str], board: list[str]) -> bool:
    """Vérifie si parmi les 7 cartes (hand + board), il existe une quinte flush."""
    all_cards = hand + board
    parsed = [parse_card(c) for c in all_cards]

    # Grouper les cartes par couleur
    suits: dict[str, list[int]] = {}
    for value, suit in parsed:
        suits.setdefault(suit, []).append(value)

    # Pour chaque couleur ayant au moins 5 cartes, chercher une suite
    for suit, values in suits.items():
        if len(values) < 5:
            continue

        # Gérer l'As comme valeur basse (1) en plus de haute (14)
        if 14 in values:
            values.append(1)

        unique_values = sorted(set(values))

        # Chercher 5 valeurs consécutives
        consecutive = 1
        for i in range(1, len(unique_values)):
            if unique_values[i] == unique_values[i - 1] + 1:
                consecutive += 1
                if consecutive >= 5:
                    return True
            else:
                consecutive = 1

    return False


def is_four_of_a_kind(hand: list[str], board: list[str]) -> bool:
    """Vérifie si parmi les 7 cartes (hand + board), il existe un carré."""
    all_cards = hand + board
    parsed = [parse_card(c) for c in all_cards]

    # Compter les occurrences de chaque valeur
    value_counts: dict[int, int] = {}
    for value, _ in parsed:
        value_counts[value] = value_counts.get(value, 0) + 1

    return any(count >= 4 for count in value_counts.values())


def is_full_house(hand: list[str], board: list[str]) -> bool:
    """Vérifie si parmi les 7 cartes (hand + board), il existe un full house (brelan + paire)."""
    all_cards = hand + board
    parsed = [parse_card(c) for c in all_cards]

    # Compter les occurrences de chaque valeur
    value_counts: dict[int, int] = {}
    for value, _ in parsed:
        value_counts[value] = value_counts.get(value, 0) + 1

    has_three = False
    has_pair = False
    for count in value_counts.values():
        if count >= 3:
            has_three = True
        elif count >= 2:
            has_pair = True

    return has_three and has_pair


def is_flush(hand: list[str], board: list[str]) -> bool:
    """Vérifie si parmi les 7 cartes (hand + board), il existe une flush (5 cartes de même couleur)."""
    all_cards = hand + board
    parsed = [parse_card(c) for c in all_cards]

    # Compter les cartes par couleur
    suit_counts: dict[str, int] = {}
    for _, suit in parsed:
        suit_counts[suit] = suit_counts.get(suit, 0) + 1

    return any(count >= 5 for count in suit_counts.values())


def is_straight(hand: list[str], board: list[str]) -> bool:
    """Vérifie si parmi les 7 cartes, il existe une quinte (5 valeurs consécutives)."""
    all_cards = hand + board
    parsed = [parse_card(c) for c in all_cards]
    values = [value for value, _ in parsed]

    # Gérer l'As comme valeur basse (1) en plus de haute (14)
    if 14 in values:
        values.append(1)

    unique_values = sorted(set(values))

    # Chercher 5 valeurs consécutives
    consecutive = 1
    for i in range(1, len(unique_values)):
        if unique_values[i] == unique_values[i - 1] + 1:
            consecutive += 1
            if consecutive >= 5:
                return True
        else:
            consecutive = 1

    return False


def is_three_of_a_kind(hand: list[str], board: list[str]) -> bool:
    """Vérifie si parmi les 7 cartes, il existe un brelan (3 cartes de même valeur)."""
    all_cards = hand + board
    parsed = [parse_card(c) for c in all_cards]
    values = [value for value, _ in parsed]

    # Compter les occurrences de chaque valeur
    value_counts: dict[int, int] = {}
    for value in values:
        value_counts[value] = value_counts.get(value, 0) + 1

    return any(count >= 3 for count in value_counts.values())


def is_two_pair(hand: list[str], board: list[str]) -> bool:
    """Vérifie si parmi les 7 cartes, il existe au moins deux paires."""
    all_cards = hand + board
    parsed = [parse_card(c) for c in all_cards]
    values = [value for value, _ in parsed]

    # Compter les occurrences de chaque valeur
    value_counts: dict[int, int] = {}
    for value in values:
        value_counts[value] = value_counts.get(value, 0) + 1

    # Compter le nombre de paires (valeurs présentes au moins 2 fois)
    pairs = sum(1 for count in value_counts.values() if count >= 2)

    return pairs >= 2


def is_one_pair(hand: list[str], board: list[str]) -> bool:
    """Vérifie si parmi les 7 cartes, il existe au moins une paire."""
    all_cards = hand + board
    parsed = [parse_card(c) for c in all_cards]
    values = [value for value, _ in parsed]

    # Compter les occurrences de chaque valeur
    value_counts: dict[int, int] = {}
    for value in values:
        value_counts[value] = value_counts.get(value, 0) + 1

    return any(count >= 2 for count in value_counts.values())


def is_high_card(hand: list[str], board: list[str]) -> bool:
    """Vérifie si la main n'a aucune combinaison (toujours vrai si aucune autre main)."""
    return not (
        is_one_pair(hand, board)
        or is_two_pair(hand, board)
        or is_three_of_a_kind(hand, board)
        or is_straight(hand, board)
        or is_straight_flush(hand, board)
    )
