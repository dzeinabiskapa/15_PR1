class GameTreeNode:
    # Spēles koka mezglu klase, katrs mezgls atspoguļo vienu spēles stāvokli
    def __init__(self, sequence, scores, player_turn, parent=None, depth=0):
        self.sequence = sequence  # Saraksts ar atlikušajiem skaitļiem spēlē
        self.scores = scores   # Saraksts ar spēlētāju punktiem [P1 punkti, P2 punkti]
        self.player_turn = player_turn  # Kura spēlētāja gājiens ir pašlaik (0 - P1, 1 - P2)
        self.children = [] # Saraksts ar bērnu mezgliem (iespējamiem nākamajiem gājieniem)
        self.parent = parent  # Atsauce uz vecāku mezglu (iepriekšējo stāvokli)
        self.depth = depth  # Mezglu dziļums kokā (palīdz ierobežot rekursiju)

    def generate_children(self, max_depth=3):
        # Ģenerē visus iespejamos gājienus, ko abi spēletaji var izdarīt līdz max_depth
        if self.depth >= max_depth: # Neģenerējam dziļāk par noteikto dziļumu
            return

        for i, num in enumerate(self.sequence):
            new_sequence = self.sequence[:i] + self.sequence[i+1:] # Noņemot skaitli no secības izvedo jaunu secibu
            new_scores = self.scores[:] # Atjauno punktu sakitu
            new_scores[self.player_turn] += num

            child_node = GameTreeNode(new_sequence, new_scores, 1 - self.player_turn, self, self.depth + 1) 	# Izveido jaunus bērnu mezglus 
            self.children.append(child_node) # Pievieno mezglu 
            child_node.generate_children(max_depth) # Rekursīvi ģenerē nākamos gājienus

            # Dalīšana
            if num == 2:
                split_sequence = self.sequence[:i] + [1, 1] + self.sequence[i+1:]  # Sadala “2” divos “1”
    
                split_node = GameTreeNode(split_sequence, new_scores, 1 - self.player_turn, self, self.depth + 1) # Izveido jaunu Mezglu no dalīšanas 
                self.children.append(split_node) #Pievieno sadalīšanas gājiena mezglu kā bērnu
                split_node.generate_children(max_depth) #Pārbauda dziļumu bērnam
    
            if num == 4:
                split_sequence = self.sequence[:i] + [2, 2] + self.sequence[i+1:] # Sadala “4” divos “2”
                split_scores = new_scores[:]
                split_scores[self.player_turn] += 1 # Pieskaita 1 punktu par dalīšanu
    
                split_node = GameTreeNode(split_sequence, split_scores, 1 - self.player_turn, self, self.depth + 1) # Izveido jaunu Mezglu no dalīšanas
                self.children.append(split_node) #Pievieno sadalīšanas gājiena mezglu kā bērnu
                split_node.generate_children(max_depth) #Pārbauda dziļumu bērnam