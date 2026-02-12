CARD_VALUES = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
    "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13, "A": 14,
}


def parse_card(card: str) -> tuple[int, str]:
    """Parse une carte '10S' -> (10, 'S'), 'AH' -> (14, 'H')."""
    suit = card[-1]
    value = card[:-1]
    return CARD_VALUES[value], suit



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

    # Vérifier s'il y a au moins une valeur présente 3 fois ou plus
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

    # Vérifier s'il y a au moins une valeur présente 2 fois ou plus
    return any(count >= 2 for count in value_counts.values())


def is_high_card(hand: list[str], board: list[str]) -> bool:
    """Vérifie si la main n'a aucune combinaison (toujours vrai si aucune autre main)."""
    # Une main a toujours au moins une carte haute
    # Cette fonction retourne True si aucune autre combinaison n'est présente
    return not (
        is_one_pair(hand, board)
        or is_two_pair(hand, board)
        or is_three_of_a_kind(hand, board)
        or is_straight(hand, board)
        or is_straight_flush(hand, board)
    )
