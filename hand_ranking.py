def generate_ranks():
    file = open('hand_rankings.txt') 
    
    convert = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'T': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14,
        's': True,
        'o': False
    }
  
    ranks = {}
    content = file.readlines() 
    for i in range(169):
        s = content[i].strip()
        l = list(s)
        ranks[(convert[l[0]], convert[l[1]], convert[l[2]])] = i
    return ranks

    
    
    

    
    
    
    
