import time

hand = [[0, 0], [0, 0]]
hand[0][0], hand[0][1], hand[1][0], hand[1][1] = map(int, input().split(' '))

toCall = int(input()) #any input here - your turn 
# toCall p1Actions p2Actions p3Actions p4Actions
# 123456 f-fold    c-check   r-raise   k-call    
# i - none

if toCall == 0:
    print('c')
else:
    if hand[0][0] + hand[1][0] // 2 > 7:
        print('call')
    else:
        print('fold')
