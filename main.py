import random
import subprocess
from evaluate_hands import evaluate_hand, find_winning_hand, HAND_RANKS
from itertools import combinations
from collections import Counter
import sys
import os

player_n = 4
player_hands = []
river = []
start_stack = 10000
player_stacks = [start_stack]*player_n
deck = []


pot = 0
dealer = 1
min_bet = 200

player_bets = [0]*player_n
to_call = min_bet
is_playing = [1]*player_n
river = []

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
    id = random.randint(0, len(deck)-1)
    output = [deck[id][0], deck[id][1]]
    deck.pop(id)
    return output

def deduct_chips(id, n): #places chips into middle
    global pot
    global player_stacks
    if player_stacks[id] > n:
        player_stacks[id] -= n
        pot += n
        player_bets[id] += n
    else:
        pot += player_stacks[id]
        player_bets[id] += player_stacks[id]
        player_stacks[id] = 0
        
    

def start_hand():
    global dealer
    global player_hands
    global player_bets
    global to_call
    global is_playing
    global river
    global pot
    
    player_bets = [0]*player_n
    to_call = min_bet
    is_playing = [1]*player_n
    
    river = []
    pot = 0
    
    deduct_chips(dealer, min_bet)
    deduct_chips(dealer-1, min_bet // 2)
    dealer += 1
    dealer %= player_n
    
    player_hands = []
    generate_deck()
    for n in range(player_n):
        player_hands.append([pick_card(), pick_card()])
        
        
processes = [subprocess.Popen(['python3', 'script1.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True),
             subprocess.Popen(['python3', 'script2.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True),
             subprocess.Popen(['python3', 'script3.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True),
             subprocess.Popen(['python3', 'script4.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)]



def take_input(id):
    return processes[id].stdout.readline().strip()

def write_output(id, text):
    processes[id].stdin.write(text+"\n")
    processes[id].stdin.flush()
    
    
def write_hands():
    for i in range(player_n):
        s = str(player_hands[i][0][0])+' '+str(player_hands[i][0][1])+' '+str(player_hands[i][1][0])+' '+str(player_hands[i][1][1])
        write_output(i, s)
        
# toCall p1Actions p2Actions p3Actions p4Actions
# 123456 f-fold    c-check   r-raise   k-call    
# i - first turn of the game so no actions

def calls_equal():
    for i in range(player_n):
        if player_bets[i] != to_call and is_playing[i] == 1:
            if player_stacks != 0:
                return False
    return True


def take_bets():
    global to_call
    global last_actions
    
    for i in range(player_n):
        print('taking input from ' + str(i))
        
        s = ''
        for action in last_actions:
            s += action
            s += ' '
        write_output(i, s)
        
        write_output(i, str(to_call-player_bets[i]))
        
        s = take_input(i)
        print('to call', end=' ')
        print(str(to_call-player_bets[i]))
        last_actions.pop(0)
        last_actions.append(s)
        print(s)
        if s[0] == 'f':
            is_playing[i] = 0
            continue
        elif s[0] == 'c':
            print(to_call, player_bets[i])
            if to_call-player_bets[i] != 0:
                print('Player '+str(i+1)+': Error Player checked while having to call a bet')
            continue
        elif s[0] == 'k':
            deduct_chips(i, to_call-player_bets[i])
            #player_bets[i] = to_call
        elif s[0] == 'r':
            if int(s[1:]) < min_bet:
                print('Player '+str(i+1)+': Error a raise has to be at least 1 min_bet more than the current bet')
                break
            print(int(s[1:]), to_call-player_bets[i]+int(s[1:-1]))
            deduct_chips(i, to_call-player_bets[i]+int(s[1:]))
            to_call+=int(s[1:])
            #player_bets[i] = to_call+int(s[1:-1])
        else:
            print('Invalid command symbol')
            
            
    while not calls_equal():
        for i in range(player_n):
            if calls_equal():
                break
            print('to call', end=' ')
            print(str(to_call-player_bets[i]))
            write_output(i, 'i')
            s = ''
            for action in last_actions:
                s += action
                s += ' '
            write_output(i, s)
            write_output(i, str(to_call-player_bets[i]))
            s = take_input(i).strip()
            last_actions.pop(0)
            last_actions.append(s)
            print(s)
            if s[0] == 'f':
                is_playing[i] = 0
                continue
            elif s[0] == 'c':
                continue
            elif s[0] == 'k':
                deduct_chips(i, to_call-player_bets[i])
                #player_bets[i] = to_call
            elif s[0] == 'r':
                print(int(s[1:]), to_call-player_bets[i]+int(s[1:-1]))
                deduct_chips(i, to_call-player_bets[i]+int(s[1:]))
                to_call+=int(s[1:])
                #player_bets[i] = to_call+int(s[1:-1])
            else:
                print('Invalid command symbol')
                
last_actions = ['i']*player_n
    
while not input():
    start_hand()
        
    print(player_hands)
    print(player_stacks)
    print()
    write_hands()
    
    take_bets()
                
    river.append(pick_card())
    river.append(pick_card())
    river.append(pick_card())
    print(river)
    for i in range(player_n):
        s = str(river[0][0])+' '+str(river[0][1])+' '+str(river[1][0])+' '+str(river[1][1])+' '+str(river[2][0])+' '+str(river[2][1])
        write_output(i, s)
        
    take_bets()
    
    river.append(pick_card())
    for i in range(player_n):
        s = str(river[3][0])+' '+str(river[3][1])
        write_output(i, s)
    take_bets()
    
    river.append(pick_card())
    for i in range(player_n):
        s = str(river[4][0])+' '+str(river[4][1])
        write_output(i, s)
    take_bets()
    
    print(player_hands)
    player_stacks[find_winning_hand(river, player_hands, is_playing)] += pot
    
            
    print(player_stacks)





















''' 
proc1 = subprocess.Popen(['python3', 'script1.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
proc2 = subprocess.Popen(['python3', 'script2.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
# Send some data to the subprocesses
proc1.stdin.write("Hello from main to subprocess 1\n")
proc1.stdin.flush()
proc2.stdin.write("Hello from main to subprocess 2\n")
proc2.stdin.flush()
# Read the output from the subprocesses
output1 = proc1.stdout.readline().strip()
output2 = proc2.stdout.readline().strip()

print(output1)
print(output2)

proc1.stdin.write("14 1 9 1 8 3\n")
proc1.stdin.flush()
proc2.stdin.write("14 1 9 1 8 3\n")
proc2.stdin.flush()

output1 = proc1.stdout.readline().strip()
output2 = proc2.stdout.readline().strip()

print(output1)
print(output2)
'''

