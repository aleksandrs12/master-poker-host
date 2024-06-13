import time

file_object = open('logs3.txt', 'a')


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

    '''s = input()
    river = [[0, 0], [0, 0], [0, 0]]
    river[0][0], river[0][1], river[1][0], river[1][1], river[2][0], river[2][1] = s.split(' ')
    file_object.write(s)'''

    if toCall != 0:
        print('r200')
        file_object.write('k'+'\n')
    else:
        print('c')
        file_object.write('c'+'\n')
        
file_object.close()






# input 2 hand cards
# input other player actions
# input toCall
# output descission

# input new card
# input actions
# input toCall
# output descission
