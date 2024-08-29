from hand_ranking import generate_ranks
from evaluate_hands import evaluate_hand

class Player_logic_default:
    def __init__(self, bank, id):
        self.my_bank = bank
        
        self.RANKS = generate_ranks()

        self.my_id = id

        self.history = {
            0: [],       # [[['c', 'k', 'r200'], [[9, 2], [8, 1]], [river]]]
            1: [],
            2: []
        }
        self.my_cards = []
        self.river = []

        self.my_bank = 3000
        self.banks = {
            0: 3000,
            1: 3000,
            2: 3000
        }

    def raise_by(self, toCall, n):
        self.my_bank -= toCall+n
        
    def raise_by_total(self, toCall, n):
        if n < 0:
            if toCall == 0:
                return 'c'
            else:
                return 'f'
        if self.my_bank >= toCall+n:
            self.raise_by(toCall, n)
            return 'r'+str(n)
        elif self.my_bank > toCall:
            s = 'r'+str(self.my_bank)
            self.raise_by(toCall, self.my_bank)
            return s
        else:
            if toCall == 0 or self.my_bank == 0:
                return 'c'
            else:
                return 'k'
            
    def descission_pre_flop(self, toCall, iteration):
        if iteration == 0:
            if toCall == 0:
                return 'c'
            else:
                return 'f'
                
        else:
            if toCall == 0:
                return 'c'
            else:
                return 'f'


    def descission_flop(self, toCall, river, iteration):
        hand_eval = evaluate_hand([self.my_cards[0], self.my_cards[1], river[0], river[1], river[2]])    # evaluates your current combination
        river_eval = evaluate_hand(river)   # evaluates the combinations on the river
        if iteration == 0:
            if toCall == 0:
                return 'c'
            else:
                return 'f'
                
        else:
            if toCall == 0:
                return 'c'
            else:
                return 'f'
                
    def descission_4th_card(self, toCall, river, iteration):
        hand_eval = evaluate_hand([self.my_cards[0], self.my_cards[1], river[0], river[1], river[2]])    # evaluates your current combination
        river_eval = evaluate_hand(river)   # evaluates the combinations on the river
        if iteration == 0:
            if toCall == 0:
                return 'c'
            else:
                return 'f'
                
        else:
            if toCall == 0:
                return 'c'
            else:
                return 'f'
                
    def descission_5th_card(self, toCall, river, iteration):
        hand_eval = evaluate_hand([self.my_cards[0], self.my_cards[1], river[0], river[1], river[2]])    # evaluates your current combination
        river_eval = evaluate_hand(river)   # evaluates the combinations on the river
        if iteration == 0:
            if toCall == 0:
                return 'c'
            else:
                return 'f'
                
        else:
            if toCall == 0:
                return 'c'
            else:
                return 'f'