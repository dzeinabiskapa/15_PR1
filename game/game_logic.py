import random
from minimax_algo import MinimaxAI
from alpha_beta_algo import AlphaBetaAI

class gameLogic:

    def __init__(self, update_ui, ai_algorithm="Minimax"):
        self.sequence = []  # Spēles virkne (skaitļi 1, 2, 3, 4)
        self.scores = [0, 0]  # Spēlētāju punkti: [cilvēks, dators]
        self.player_turn = 0  # Kurš spēlētājs tagad ir pie gājiena (0 - cilvēks, 1 - AI)
        self.update_ui = update_ui  # Funkcija, kas atjauno UI
        self.ai_algorithm = ai_algorithm  # Kurš AI algoritms tiek izmantots: "Minimax" vai "AlphaBeta"

    def start_game(self, sequence_length):
        # Sāk jaunu spēli ar ģenerētu virkni
        self.sequence = self.sequence_generation(sequence_length)
        self.scores = [0, 0]
        self.player_turn = 0  # Cilvēks sāk pirmais
        self.update_ui(self.sequence, self.scores, self.player_turn)

    def sequence_generation(self, sequence_len):
        # Ģenerē sākotnējo virkni ar nejaušiem skaitļiem (1, 2, 3, 4)
        return random.choices([1, 2, 3, 4], k=sequence_len)

    def take_number(self, i):
        # Spēlētājs izvēlas paņemt skaitli no virknes
        if 0 <= i < len(self.sequence):
            self.scores[self.player_turn] += self.sequence.pop(i)  # Pievieno punktus un izņem skaitli
            self.switch_turn()  # Pāriet nākamajam spēlētājam

    def split_number(self, i):
        # Spēlētājs sadala skaitli
        if 0 <= i < len(self.sequence):
            if self.sequence[i] == 2:
                self.sequence[i:i+1] = [1, 1]  # 2 tiek sadalīts divos 1
            elif self.sequence[i] == 4:
                self.sequence[i:i+1] = [2, 2]  # 4 → divi 2, +1 punkts spēlētājam
                self.scores[self.player_turn] += 1
            else:
                return False  # Nevar sadalīt citu skaitli
            self.switch_turn()
            return True
        return False

    def switch_turn(self):
        # Maina spēlētāja gājienu
        self.player_turn = 1 - self.player_turn
        self.update_ui(self.sequence, self.scores, self.player_turn)

    def ai_move(self):
        # Datora gājiens (ja tas ir viņa kārta)
        if self.player_turn == 1:
            if self.ai_algorithm == "Minimax":
                ai = MinimaxAI(self, max_depth=3)  # Izvēlas minimax algoritmu
            else:
                ai = AlphaBetaAI(self, max_depth=3)  # Vai alfa-beta algoritmu

            bestMove = ai.getBestMove()  # Atrod labāko gājienu
            if bestMove: # Ja labākais gājiens pastāv
                move_type, index = bestMove
                if move_type == "take":
                    self.take_number(index)  # Paņem skaitli
                elif move_type == "split":
                    self.split_number(index)  # Sadalīt skaitli
            self.update_ui(self.sequence, self.scores, self.player_turn)

    def game_over(self):
        # Spēle ir beigusies, ja vairs nav neviena skaitļa virknē
        return len(self.sequence) == 0
