import random
def deal_hand():
    # Creates a 52 card deck
    suits = ["Spades","Hearts","Diamonds", "Clubs"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    deck = [rank + suit for rank in ranks for suit in suits]

    # Shuffle
    random.shuffle(deck)

    # Deal a hand
    player_hand = deck[:2]
    

    # deal flop
    flop = deck[2:5]
    

    # deal turn
    turn = deck[5:6]

    # deal river
    river = deck [6:7]

    dealt_dict =  {
        "hand": player_hand, "flop": flop, "turn": turn, "river": river
    }

    return dealt_dict

hand = deal_hand()
for key,value in hand.items():
    print(f"{key}: {value}.\n")



    
