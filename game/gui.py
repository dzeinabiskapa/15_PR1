import tkinter as tk
from tkinter import ttk, messagebox

from game_logic import gameLogic

class CiparuSpele:
    def __init__(self, root):
        self.root = root
        self.root.title("CIPARU SPĒLE")  #Loga virsraksts
        self.root.geometry("1000x500")  #Loga izmērs
        self.selected_ai_algorithm = tk.StringVar(value="Minimax")  #Default algo
        self.start_screen()  #Atver sākuma ekrānu

    def start_screen(self): #Notīra iepriekšējos elementus
        for widget in self.root.winfo_children():
            widget.destroy()

        #Konteiners sākuma elementiem
        container = tk.Frame(self.root)
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        tk.Label(container, text="CIPARU SPĒLE", font=("Arial", 24, "bold")).pack()

        #Cik ciparus iekļaut spēlē
        frame = tk.Frame(container)
        frame.pack(pady=20)
        tk.Label(frame, text="Ievadiet ciparu skaitu:", font=("Arial", 14)).pack(side=tk.LEFT, padx=5)
        self.sequence_length_var = tk.StringVar(value="15")
        self.sequence_dropdown = ttk.Combobox(frame, textvariable=self.sequence_length_var, values=[str(i) for i in range(15, 21)], state='readonly')
        self.sequence_dropdown.pack(side=tk.LEFT)

        #Kurš sāk spēli
        turn_frame = tk.Frame(container)
        turn_frame.pack(pady=10)
        tk.Label(turn_frame, text="Izvēlieties gājienu secību:", font=("Arial", 14)).pack(side=tk.LEFT, padx=5)
        self.player_first_var = tk.StringVar(value="Spēlētājs pirmais")
        ttk.Combobox(turn_frame, textvariable=self.player_first_var, values=["Spēlētājs pirmais", "AI pirmais"], state='readonly').pack(side=tk.LEFT)

        #Kurš algoritms tiks izmantots
        algo_frame = tk.Frame(container)
        algo_frame.pack(pady=10)
        tk.Label(algo_frame, text="Izvēlieties algoritmu:", font=("Arial", 14)).pack(side=tk.LEFT, padx=5)
        ttk.Combobox(algo_frame, textvariable=self.selected_ai_algorithm, values=["Minimax", "Alpha-Beta"], state='readonly').pack(side=tk.LEFT)

        #Poga spēles sākšanai
        tk.Button(container, text="SĀKT SPĒLI", font=("Arial", 14, "bold"), command=self.start_game).pack(pady=20)

    def start_game(self):
        #Iegūst izvēlēto algoritmu un izveido jaunu spēli
        selected_algo = self.selected_ai_algorithm.get()
        self.game_logic = gameLogic(self.update_ui, selected_algo)
        self.game_logic.start_game(int(self.sequence_length_var.get()))

        #Kurš spēlētājs sāk pirmais
        self.game_logic.player_turn = 0 if self.player_first_var.get() == "Spēlētājs pirmais" else 1

        self.game_screen() #Spēles ekrāns

    def game_screen(self):
        #Notīra ekrānu
        for widget in self.root.winfo_children():
            widget.destroy()

        #Galvenais konteiners
        container = tk.Frame(self.root)
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(container, text="CIPARU SPĒLE", font=("Arial", 24, "bold")).pack()

        #Kura gājiens
        self.turn_label = tk.Label(container, text=self.get_turn_text(), font=("Arial", 14))
        self.turn_label.pack(pady=10)

        #Ciparu pogas
        self.selected_number = tk.IntVar(value=-1)
        self.sequence_frame = tk.Frame(container)
        self.sequence_frame.pack(pady=10)

        #Pogas paņemt / dalīt
        tk.Button(container, text="DALĪT SKAITLI", font=("Arial", 14), command=self.split_number).pack(pady=10)
        tk.Button(container, text="PAŅEMT SKAITLI", font=("Arial", 14), command=self.take_number).pack(pady=5)

        #Punkti
        score_frame = tk.Frame(container)
        score_frame.pack(pady=20)

        self.player_score_label = tk.Label(score_frame, text="", font=("Arial", 12))
        self.player_score_label.pack(side=tk.LEFT, padx=20)

        self.ai_score_label = tk.Label(score_frame, text="", font=("Arial", 12))
        self.ai_score_label.pack(side=tk.LEFT)

        #Atjauno UI
        self.update_ui(self.game_logic.sequence, self.game_logic.scores, self.game_logic.player_turn)

    def update_ui(self, sequence, scores, player_turn):
        #Ja ekrāns ir aizvērts, neko nedara
        if not hasattr(self, 'sequence_frame') or not self.sequence_frame.winfo_exists():
            return

        #Iztīra iepriekšējos ciparu pogu elementus
        for widget in self.sequence_frame.winfo_children():
            widget.destroy()

        self.selected_number.set(-1) #Noņem to, ka ir izvēlēts cipars

        #Izveido ciparu pogas
        for index, num in enumerate(sequence):
            btn = tk.Radiobutton(self.sequence_frame, text=str(num), variable=self.selected_number, value=index, indicatoron=0, font=("Arial", 12), padx=5, pady=5)
            btn.pack(side=tk.LEFT, padx=2)

        #Atjauno informāciju par kārtu un punktiem
        self.turn_label.config(text="Spēlētāja gājiens" if player_turn == 0 else "AI gājiens")
        self.player_score_label.config(text=f"Spēlētāja punktu skaits: {scores[0]}")
        self.ai_score_label.config(text=f"AI punktu skaits: {scores[1]}")

        #Ja nav cipari, beidz spēli
        if not sequence:
            self.end_game()

        # Nobremzē ai ātrumu atbildē
        if player_turn == 1:
            self.root.after(1000, self.game_logic.ai_move)
    #Paņem izvēlēto ciparu no virknes
    def take_number(self):
        index = self.selected_number.get()
        if index == -1:
            messagebox.showerror("Kļūda", "Izvēlieties derīgu ciparu.")
            return
        self.game_logic.take_number(index)

    #Dalīt izvēlēto ciparu
    def split_number(self):
        index = self.selected_number.get()
        if index == -1:
            messagebox.showerror("Kļūda", "Izvēlieties derīgu ciparu.")
            return
        if not self.game_logic.split_number(index):
            messagebox.showerror("Kļūda", "Šo ciparu nevar dalīt.")

    #Kam gājiens
    def get_turn_text(self):
        return "Spēlētāja gājiens" if self.game_logic.player_turn == 1 else "AI gājiens"

    #Notīra ekrānu un parāda rezultātus
    def end_game(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        container = tk.Frame(self.root)
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(container, text="CIPARU SPĒLE", font=("Arial", 20, "bold"), justify="center").pack(pady=10)
        tk.Label(container, text="SPĒLE BEIGUSIES", font=("Arial", 18, "bold"), justify="center").pack()

        #Rezultāta noteikšana
        if self.game_logic.scores[0] > self.game_logic.scores[1]:
            winner_text = "Uzvar: Spēlētājs"
        elif self.game_logic.scores[1] > self.game_logic.scores[0]:
            winner_text = "Uzvar: AI"
        else:
            winner_text = "Neizšķirts"

        tk.Label(container, text=winner_text, font=("Arial", 14), justify="center").pack(pady=5)

        #Jaunas spēles sākšanas poga
        tk.Button(container, text="SPĒLĒT VĒLREIZ", font=("Arial", 14, "bold"), command=self.start_screen).pack(pady=20)

        #Gala rezultāts
        score_frame = tk.Frame(container)
        score_frame.pack(pady=10)
        tk.Label(score_frame, text=f"Spēlētāja punktu skaits: {self.game_logic.scores[0]}", font=("Arial", 12)).pack(side=tk.LEFT, padx=20)
        tk.Label(score_frame, text=f"AI punktu skaits: {self.game_logic.scores[1]}", font=("Arial", 12)).pack(side=tk.LEFT)
