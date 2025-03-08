import random

def sequence_generation(sequence_len):
    num_list = [1,2,3,4]
    return random.choices(num_list, k = sequence_len)

def take_number(sequence, i, scores, player_turn):
    scores[player_turn] += sequence[i]
    del sequence[i]

def split_number(sequence, i, scores, player_turn):
    if sequence[i] == 2:
        sequence[i:i+1] = [1,1]
    elif sequence[i] == 4:
        sequence[i:i+1] = [2,2]
        scores[player_turn] += 1
    else:
        print("Invalid split")

#
# pievienot ievades pārbaudi
#
def game_logic():
    try:
        sequence_len = int(input("Enter sequence length 15-20: "))
        if sequence_len < 15 or sequence_len > 20:
            raise ValueError
    except ValueError:
        print("Invalid input")
        return

    sequence = sequence_generation(sequence_len)
    scores = [0,0]
    player_turn = 0
    
    while sequence:
        #first_turn = input("Who starts? Player or AI: ") # Kaut-ko izdomāt ar gājieniem?
        
        print(f"Sequence: {sequence}")
        print(f"Player's {player_turn+1} turn! Score: {scores[player_turn]}")
        action = input("Choose action - [t] Take a number or [s] Split  (2 or 4): ").strip().lower()
        
        if action == 't':
            i = int(input(f"Choose index of number (1-{len(sequence)}): "))
            if i-1 >= 0 and i-1 < len(sequence):
                take_number(sequence, i-1, scores, player_turn)
            else:
                print("Invalid index.")
        elif action == 's':
            i = int(input(f"Choose index of number (1-{len(sequence)}): "))
            if i-1 >= 0 and i-1 < len(sequence) and sequence[i-1] in [2, 4]:
                split_number(sequence, i-1, scores, player_turn)
            else:
                print("Invalid split")
        else:
            print("Invalid action. Choose again")
            continue
    
        player_turn = 1 - player_turn  # Switch turn

    print("Game is over!")
    print(f"Final scores: Player 1 - {scores[0]}, Player 2 - {scores[1]}")
    winner = "Player 1" if scores[0] > scores[1] else " Player 2" if scores[1] > scores[0] else "Tie"
    print(f"Winner: {winner}")
    restart = input("Restart? [Y/N]: ").strip().lower()
    if restart == 'y':
        game_logic()
    else:
        exit()
game_logic()
        