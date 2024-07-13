from hand_ranking import generate_ranks
from evaluate_hands import evaluate_hand
import random
from resources.script1.logic import Player_logic




player = Player_logic(3000, 0)
player_n = 3

player_id = int(input())
toCall = int(input())

while True:
    for n in range(player_n):
        player.history[n].append([[], [[0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]])
    
    river = []
    player.my_cards.append([0, 0])
    player.my_cards.append([0, 0])
    player.my_cards[0][0], player.my_cards[0][1], player.my_cards[1][0], player.my_cards[1][1] = input().split(' ')
    player.my_cards[0][0], player.my_cards[0][1], player.my_cards[1][0], player.my_cards[1][1] = int(player.my_cards[0][0]), int(player.my_cards[0][1]), int(player.my_cards[1][0]), int(player.my_cards[1][1])
    
    if player.my_cards[1][0] > player.my_cards[0][0]:
        player.my_cards[0][0], player.my_cards[0][1], player.my_cards[1][0], player.my_cards[1][1] = player.my_cards[1][0], player.my_cards[1][1], player.my_cards[0][0], player.my_cards[0][1]
    
    input()
    input()
    player.banks[0], player.banks[1], player.banks[2] = input().split()
    player.banks[0], player.banks[1], player.banks[2] = int(player.banks[0]), int(player.banks[1]), int(player.banks[2])
    player.my_bank = player.banks[player.my_id]
    
    player_id = -2
    iteration = 0
    while player_id != -1:
        player_id = int(input())
        toCall = int(input())
        if player_id == player.my_id:
            print(player.descission_pre_flop(toCall, iteration))
            input()
            iteration += 1
        elif player_id != -1:
            action = input()
            player.history[player_id][-1][0].append(action)
          
    river.append([0, 0])
    river.append([0, 0])
    river.append([0, 0])
    river[0][0], river[0][1], river[1][0], river[1][1], river[2][0], river[2][1] = input().split(' ')
    river[0][0], river[0][1], river[1][0], river[1][1], river[2][0], river[2][1] = int(river[0][0]), int(river[0][1]), int(river[1][0]), int(river[1][1]), int(river[2][0]), int(river[2][1])
    
    player_id = -2
    iteration = 0
    while player_id != -1:
        player_id = int(input())
        toCall = int(input())
        if player_id == player.my_id:
            print(player.descission_flop(toCall, river, iteration))
            input()
            iteration += 1
        elif player_id != -1:
            action = input()
            player.history[player_id][-1][0].append(action)
        
            
    river.append([0, 0])
    river[-1][0], river[-1][1] = input().split(' ')
    river[-1][0], river[-1][1] = int(river[-1][0]), int(river[-1][1])
    
    player_id = -2
    iteration = 0
    while player_id != -1:
        player_id = int(input())
        toCall = int(input())
        if player_id == player.my_id:
            print(player.descission_4th_card(toCall, river, iteration))
            input()
            iteration += 1
        elif player_id != -1:
            action = input()
            player.history[player_id][-1][0].append(action)
            
    river.append([0, 0])
    river[-1][0], river[-1][1] = input().split(' ')
    river[-1][0], river[-1][1] = int(river[-1][0]), int(river[-1][1])
    
    player_id = -2
    iteration = 0
    while player_id != -1:
        player_id = int(input())
        toCall = int(input())
        if player_id == player.my_id:
            print(player.descission_5th_card(toCall, river, iteration))
            input()
            iteration += 1
        elif player_id != -1:
            action = input()
            player.history[player_id][-1][0].append(action)
            
    for n in range(player_n):
        for i in range(5):
            player.history[n][-1][2][i][0], player.history[n][-1][2][i][1] = river[i][0], river[i][1]
            
    
    s = input()
    ar = s.split(' ')
    
    for n in range(player_n):
        player.history[n][-1][1][0][0], player.history[n][-1][1][0][1], player.history[n][-1][1][1][0], player.history[n][-1][1][1][1] = int(ar[4*n]), int(ar[4*n+1]), int(ar[4*n+2]), int(ar[4*n+3])
    
    input()
    input()
            
    