import time

file_object = open('logs2.txt', 'a')


def what_to_do(toCall):
    if toCall != 0:
        return 'k'
    else:
        return 'c'


while True:
    s = input()
    if s != 'i':
        cards = map(int, s.split(' '))
    file_object.write(s+'\n')

    s = input()
    file_object.write(s+'\n')

    s = input()
    toCall = int(s)
    file_object.write(s+'\n')

    action = what_to_do(toCall)
    print(action)
    file_object.write(action+'\n')
    
    card_input = 'i'
    while card_input == 'i':
        card_input = input()
        file_object.write(card_input+'\n')
        if card_input != 'i':
            river = [[0, 0], [0, 0], [0, 0]]
            river[0][0], river[0][1], river[1][0], river[1][1], river[2][0], river[2][1] = card_input.split(' ')
        s = input()
        file_object.write(s+'\n')

        s = input()
        toCall = int(s)
        file_object.write(s+'\n')

        action = what_to_do(toCall)
        print(action)
        file_object.write(action+'\n')
        
    
    card_input = 'i'
    while card_input == 'i':
        card_input = input()
        file_object.write(card_input+'\n')
        if card_input != 'i':
            river.append(card_input.split(' '))
        s = input()
        file_object.write(s+'\n')

        s = input()
        toCall = int(s)
        file_object.write(s+'\n')

        action = what_to_do(toCall)
        print(action)
        file_object.write(action+'\n')
        
    card_input = 'i'
    while card_input == 'i':
        card_input = input()
        file_object.write(card_input+'\n')
        if card_input != 'i':
            river.append(card_input.split(' '))
        s = input()
        file_object.write(s+'\n')

        s = input()
        toCall = int(s)
        file_object.write(s+'\n')

        action = what_to_do(toCall)
        print(action)
        file_object.write(action+'\n')
    
        
file_object.close()






# input 2 hand cards
# input other player actions
# input toCall
# output descission

# input new card
# input actions
# input toCall
# output descission
