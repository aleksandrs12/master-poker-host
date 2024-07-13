import subprocess
import random
import secrets
from evaluate_hands import evaluate_hand, find_winning_hand, HAND_RANKS


debug = True


notable_history = []
river = []
player_start = 2

pot = 0
highest_bet = 0
dealer = 1
min_bet = 200
class Player:
    def __init__(self, process, id) -> None:
        self.id = id
        self.process = process
        self.bet = 0
        self.bank = 3000
        self.folded = False
        self.hand = [[0, 0], [0, 0]]
        
    def call(self, toCall):
        global pot
        if self.bank == 0:
            if debug:
                print('cant call, have to check', self.bank)
            self.check(toCall)
            return False
        elif toCall <= self.bank:
            pot += toCall
            self.bank -= toCall
            self.bet += toCall
        else:
            pot += self.bank
            self.bet += self.bank
            self.bank = 0
        return True
            
    def check(self, toCall):
        if toCall == 0 or self.bank == 0:
            return True
        else:
            if debug:
                print('cant check have to call')
                print(self.bank, self.id, toCall)
                self.call(toCall)
            return False
        
    def raise_by(self, toCall, n):
        global pot
        global highest_bet
        if n >= min_bet:
            if toCall + n <= self.bank:
                pot += toCall+n
                self.bank -= toCall+n
                self.bet += toCall+n
                highest_bet += n
            else:
                if debug:
                    print('cant raise, not enough money')
                return False
        else:
            if debug:
                print('cant raise by '+str(n))
            return False
        return True
    
    def fold(self):
        self.folded = True
    
    def take_input(self):
        return self.process.stdout.readline().strip()

    def write_output(self, txt):
        self.process.stdin.write(txt+"\n")
        self.process.stdin.flush()
        
    def make_hand(self):
        self.hand = [pick_card(), pick_card()]
        
    def deduct(self, n):
        global pot
        global highest_bet
        if self.bank >= n:
            pot += n
            self.bet += n
            self.bank -= n
        else:
            pot += self.bank
            self.bet += self.bank
            self.bank = 0
        if self.bet > highest_bet:
            highest_bet = self.bet
        
        
player_n = 3
players = [Player(subprocess.Popen(['python3', 'script1.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True), 0),
           Player(subprocess.Popen(['python3', 'script2.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True), 1),
           Player(subprocess.Popen(['python3', 'script3.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True), 2)]


deck = []
winner_id = 0
players_in_hand = player_n
def generate_deck():
    global deck
    deck = []
    for n in range(2, 15):
        deck.append([n, 1])
        deck.append([n, 2])
        deck.append([n, 3])
        deck.append([n, 4])
        
def pick_card():
    global deck
    cryptogen = random.SystemRandom()
    id = cryptogen.randrange(len(deck)-1)
    output = [deck[id][0], deck[id][1]]
    deck.pop(id)
    return output

def announce_everyone(txt):
    for player in players:
        player.write_output(txt)
        
def equal_stakes(players):
    stake = 0
    for player in players:
        if not player.folded and player.bet > stake:
            stake = player.bet
    for pl in players:
        if pl.bet != stake and not pl.folded and pl.bank > 0:
            return False
    return True

def sidepot_needed(players, highest_bet):
    for player in players:
        if not player.folded:
            if player.bet < highest_bet:
                return True
    return False

def eligable_to_win(players, id, highest_bet):  # do i need this?
    total = 0
    for player in players:
        if player.bet <= players[id].bet:
            total += player.bet
        else:
            total += players[id].bet

def take_bets():
    global players_in_hand
    global winner_id
    global player_start
    for n in range(player_start, len(players)+player_start):
        player = players[n%len(players)]
        announce_everyone(str(player.id))
        announce_everyone(str(highest_bet-player.bet))
        action = player.take_input()
        announce_everyone(action)
        if not player.folded:
            if debug:
                print(action)
            if action == 'f':
                player.fold()
                players_in_hand -= 1
                if players_in_hand == 1:
                    for player in players:
                        if not player.folded:
                            winner_id = player.id
            elif action == 'c':
                player.check(highest_bet-player.bet)
            elif action == 'k':
                player.call(highest_bet-player.bet)
            elif action[0] == 'r':
                player.raise_by(highest_bet-player.bet, int(action[1:]))
                
        
            
    while not equal_stakes(players):
        for n in range(player_start, len(players)+player_start):
            player = players[n%len(players)]
            for player in players:
                if equal_stakes(players):
                    break
                announce_everyone(str(player.id))
                announce_everyone(str(highest_bet-player.bet))
                action = player.take_input()
                announce_everyone(action)
                if not player.folded:
                    if debug:
                        print(action)
                    if action == 'f':
                        player.fold()
                        players_in_hand -= 1
                        if players_in_hand == 1:
                            for player in players:
                                if not player.folded:
                                    winner_id = player.id
                    elif action == 'c':
                        player.check(highest_bet-player.bet)
                    elif action == 'k':
                        player.call(highest_bet-player.bet)
                    elif action[0] == 'r':
                        player.raise_by(highest_bet-player.bet, int(action[1:]))
                    
                    
def players_on_table(players):
    n = 0
    for player in players:
        if player.bank > 0:
            n += 1
    return n

def player_remaining(players):
    for player in players:
        if player.bank > 0:
            return player.id
        
def next_dealer(players, dealer):
    for i in range(dealer+1, dealer+player_n+1):
        if not players[i%player_n].folded and players[i%player_n].bank > 0:
            return i%player_n
        
def bets_at_zero(players):
    for player in players:
        if player.bet != 0:
            return False
    return True



def start_hand():
    global players
    global highest_bet
    global dealer
    global river
    global players_in_hand
    global pot
    global player_start
    players_in_hand = player_n
    river = []
    highest_bet = min_bet
    pot = 0
    
    for player in players:
        player.bet = 0
        player.folded = False
        if player.bank == 0:
            player.folded = True
            
    
            
    if debug:
        for player in players:
            print(player.bank, end='   ')
        print()
    
    players[dealer].deduct(min_bet)
    players[next_dealer(players, dealer)].deduct(min_bet//2)
    dealer = next_dealer(players, dealer)
    player_start = next_dealer(players, dealer)
    if debug:
        print('starts off with player ' + str(player_start))
    highest_bet = min_bet
    
    s = ''
    for player in players:
        s += str(player.bank) + ' '
    s = s.strip()
    
    announce_everyone('-1')
    announce_everyone(' ')
    announce_everyone(s)
    
    if debug:
        print()
        print()
        for player in players:
            print(player.hand, end='   ')
        print()
        for player in players:
            print(player.bank, end='   ')
        print()
    
            
    
    


        

win_count = [0]*player_n
hand_count = [0]*player_n
total_hands_won = [0]*player_n
for i in range(3000):
    for player in players:
        player.bank = 2000
        dealer = 0
    while players_on_table(players) != 1:
        #pre flop
        action = ''
        generate_deck()
        for player in players:
            player.make_hand()
            player.write_output('-1')
            player.write_output('0')
            player.write_output(str(player.hand[0][0]) + ' ' + str(player.hand[0][1]) + ' ' + str(player.hand[1][0]) + ' ' + str(player.hand[1][1]))
        start_hand()
        take_bets()
                    
        #flop
        river.append(pick_card())
        river.append(pick_card())
        river.append(pick_card())
        
        announce_everyone('-1')
        announce_everyone('0')
        announce_everyone(str(river[0][0])+' '+str(river[0][1])+' '+str(river[1][0])+' '+str(river[1][1])+' '+str(river[2][0])+' '+str(river[2][1]))
        take_bets()
        
        #4th card
        river.append(pick_card())
        announce_everyone('-1')
        announce_everyone('0')
        announce_everyone(str(river[3][0])+' '+str(river[3][1]))
        take_bets()
        
        #5th card
        river.append(pick_card())
        announce_everyone('-1')
        announce_everyone('0')
        announce_everyone(str(river[4][0])+' '+str(river[4][1]))
        take_bets()
        
        player_hands = []
        is_playing = []
        for player in players:
            player_hands.append(player.hand)
            is_playing.append(player.folded == False)
        
        if debug:
            print(is_playing)
            
        for i in range(len(players)):
            if not players[i].folded:
                if debug:
                    print('player', i, 'played')
                hand_count[i] += 1
        all_ids = [1]
        river = [[2, 1], [5, 4], [7, 2], [10, 3], [3, 2]]
        player_hands = [[[14, 1], [14, 2]], [[11, 3], [14, 4]], [[11, 1], [13, 3]]]
        players[0].bet = 200
        players[1].bet = 500
        players[2].bet = 500
        players[0].bank = 0
        players[1].bank = 0
        players[2].bank = 0
        pot = 1200
        for player in players:
            player.folded = False
        
        
        is_playing = [True, True, True]
        players_in_hand = 3
        if players_in_hand != 1 and players_in_hand != 0:
            winner_id, all_ids = find_winning_hand(river, player_hands, is_playing)
            
        s = ''
        for player in players:
            if not player.folded:
                s += str(player.hand[0][0]) + ' ' + str(player.hand[0][1]) + ' ' + str(player.hand[1][0]) + ' ' + str(player.hand[1][1]) + ' '
            else:
                s += '0 0 0 0 '
        announce_everyone('-1')
        announce_everyone('0')
        announce_everyone(s)
        if debug:
            print(s)
            
        print('pot: ', pot)
        print('banks before: ', end = '')
        for player in players:
            print(player.bank, end=' ')
        print()
        while pot != 0:
            if players_in_hand != 1 and players_in_hand != 0:
                winner_id, all_ids = find_winning_hand(river, player_hands, is_playing)
            if len(all_ids) == 1:
                if not sidepot_needed(players, highest_bet):
                    players[winner_id].bank += pot
                    total_hands_won[winner_id]+=1
                    pot = 0
                    is_playing[winner_id] = False
                    if debug:
                        print(winner_id)
                else:
                    total_win = 0
                    player_bet = players[winner_id].bet
                    for player in players:
                        if player.bet > player_bet:
                            total_win += player_bet
                            player.bet -= player_bet
                        else:
                            total_win += player.bet
                            player.bet = 0
                    players[winner_id].bank += total_win
                    pot -= total_win
                    players[winner_id].folded = True
                    is_playing[winner_id] = False
                    print(river, winner_id)
            else:
                
                for id in all_ids:
                    players[id].bank += pot // len(all_ids)
                    total_hands_won[id]+=1
                    if debug:
                        print(id, end=' ')
                pot = 0
                print()
            
            
        if not players[1].folded and players[1].hand[1][0] == 14 and players[1].hand[0][0] == 14:
            notable_history.append([river, player_hands, all_ids])
            
        
        if debug:
            print(river)
            
        print('banks after: ', end = '')
        for player in players:
            print(player.bank, end=' ')
        print()
        1/0
    win_count[player_remaining(players)] += 1
    
if debug: 
    for i in notable_history:
        print(i)
print(len(notable_history))
print(win_count)
print(hand_count)
print(total_hands_won)
    
        
    
    
    
    
    
    
            
            