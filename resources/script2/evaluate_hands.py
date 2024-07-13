from itertools import combinations
from collections import Counter

# Define constants for hand ranks
HAND_RANKS = ("High Card", "One Pair", "Two Pair", "Three of a Kind", 
              "Straight", "Flush", "Full House", "Four of a Kind", "Straight Flush")

# Function to evaluate hand rank
def evaluate_hand(cards):
    values = sorted([card[0] for card in cards], reverse=True)
    suits = [card[1] for card in cards]
    value_counts = Counter(values)
    suit_counts = Counter(suits)

    is_flush = max(suit_counts.values()) >= 5
    unique_values = sorted(value_counts.keys(), reverse=True)
    
    is_straight = False
    straight_high = 0
    if len(unique_values) >= 5:
        for i in range(len(unique_values) - 4):
            if unique_values[i] - unique_values[i + 4] == 4:
                is_straight = True
                straight_high = unique_values[i]
                break
        if unique_values[:5] == [14, 5, 4, 3, 2]:
            is_straight = True
            straight_high = 5
    
    if is_straight and is_flush:
        return (8, straight_high)
    
    if 4 in value_counts.values():
        return (7, value_counts.most_common(1)[0][0], tuple(unique_values))

    if 3 in value_counts.values() and 2 in value_counts.values():
        return (6, value_counts.most_common(2)[0][0], value_counts.most_common(2)[1][0])

    if is_flush:
        return (5, tuple(unique_values))
    
    if is_straight:
        return (4, straight_high)

    if 3 in value_counts.values():
        return (3, value_counts.most_common(1)[0][0], tuple(unique_values))

    if 2 in value_counts.values():
        pair_values = [val for val, count in value_counts.items() if count == 2]
        if len(pair_values) > 1:
            return (2, tuple(sorted(pair_values, reverse=True)), tuple(unique_values))
        else:
            return (1, pair_values[0], tuple(unique_values))
    
    return (0, tuple(unique_values))

# Main function to determine the winning hand
def find_winning_hand(river, hands, is_playing):
    '''
    for i in range(len(hands)-1, -1, -1):
        if is_playing[i] == 0:
            hands.pop(i)
    '''
        
    best_rank = (-1,)
    best_hand_index = -1
    output = []
    
    for i, hand in enumerate(hands):
        if is_playing[i]:
            combined_cards = river + hand
            all_combinations = combinations(combined_cards, 5)
            best_hand_rank = max(evaluate_hand(combo) for combo in all_combinations)
            
            if best_hand_rank > best_rank:
                best_rank = best_hand_rank
                best_hand_index = i
                output = [i]
            elif best_hand_rank == best_rank:
                output.append(i)
            
    return best_hand_index, output
