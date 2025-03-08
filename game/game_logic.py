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

#def validate_action():   // Nezinu vai šo vajag, jau ir vieglāk uzrakstīts 74.rindā
#    while True:
#        action = input("Choose action - [t] Take a number or [s] Split  (2 or 4): ").strip().lower()
#        if action == 't' or action == "s":
#            return action
#        print("Invalid action")
        
def validate_index(sequence):
    while True:
        try:
            i = int(input(f"Choose index of number (1-{len(sequence)}): "))
            if i-1 >= 0 and i-1 < len(sequence):
                return i
            else:
                print("Invalid index")
        except ValueError:
            print("Invalid input")
def validate_sequence():
    while True:
        try:
            sequence_len = int(input("Enter sequence length 15-20: "))
            if sequence_len >= 15 and sequence_len <= 20:
                return sequence_len 
            else:
                print("Invalid sequence length")
        except ValueError:
            print("Invalid input")
            
def game_logic():
    sequence_length = validate_sequence()
    sequence = sequence_generation(sequence_length)
    scores = [0,0]
    player_turn = 0
    
    while sequence:
        #first_turn = input("Who starts? Player or AI: ") # Kaut-ko izdomāt ar gājieniem
        
        print(f"Sequence: {sequence}")
        print(f"Player's {player_turn+1} turn! Score: {scores[player_turn]}")
        #action = validate_action()
        action = input("Choose action - [t] Take a number or [s] Split  (2 or 4): ").strip().lower()
        
        if action == 't':
            i = validate_index(sequence)
            take_number(sequence, i-1, scores, player_turn)
        elif action == 's':
            while True:
                i = validate_index(sequence)
                if sequence[i-1] in [2, 4]:
                    split_number(sequence, i-1, scores, player_turn)
                    break
                else:
                    print("Invalid split")
                    continue
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
        