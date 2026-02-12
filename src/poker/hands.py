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
