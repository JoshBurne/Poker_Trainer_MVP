import random

def deal_deck():
    suits = ["♠", "♥", "♦", "♣"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    deck = [rank + suit for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

def deal_cards(deck, count):
    """Draw `count` cards from the deck and return (cards, updated deck)."""
    drawn = deck[:count]
    remaining = deck[count:]
    return drawn, remaining

def deal_hand(num_opponents=0):
    """
    Returns a dictionary with:
    - player: list of 2 cards
    - opponents: list of N opponent hands (each 2 cards)
    - flop, turn, river
    """
    deck = deal_deck()
    result = {}

    result["player"], deck = deal_cards(deck, 2)

    result["opponents"] = []
    for _ in range(num_opponents):
        opp, deck = deal_cards(deck, 2)
        result["opponents"].append(opp)

    result["flop"], deck = deal_cards(deck, 3)
    result["turn"], deck = deal_cards(deck, 1)
    result["river"], deck = deal_cards(deck, 1)

    return result
