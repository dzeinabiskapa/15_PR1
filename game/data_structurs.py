class GameTreeNode:
    """Represents a node in the game tree."""
    def __init__(self, sequence, scores, player_turn, parent=None, depth=0):
        self.sequence = sequence  # Saraksts ar atlikušajiem skaitļiem spēlē
        self.scores = scores   # Saraksts ar spēlētāju punktiem [P1 punkti, P2 punkti]
        self.player_turn = player_turn  # Kurš spēlētājs ir pie gājiena (0 - P1, 1 - P2)
        self.children = [] # Saraksts ar bērnu mezgliem (iespējamiem nākamajiem gājieniem)
        self.parent = parent  # Atsauce uz vecāku mezglu (iepriekšējo stāvokli)
        self.depth = depth  # Mezglu dziļums kokā (palīdz ierobežot rekursiju)

    def generate_children(self, max_depth=3):
        """Uztaisa visus iespejamos gajienus ko abi spēletaji var izdarit lidz max_depth"""
        if self.depth >= max_depth:
            return

        for i, num in enumerate(self.sequence):
            # paņemšans gajienu
            new_sequence = self.sequence[:i] + self.sequence[i+1:] # noņema skaitli no no secības
            new_scores = self.scores[:] # atjaunina punktu sakitu
            new_scores[self.player_turn] += num
    
            child_node = GameTreeNode(new_sequence, new_scores, 1 - self.player_turn, self, self.depth + 1) # izveido jaunus bernu mezglus
            self.children.append(child_node) # pievieno mezglu 
            child_node.generate_children(max_depth)
    
            # dališanas gajiens
            if num == 2:
                split_sequence = self.sequence[:i] + [1, 1] + self.sequence[i+1:]
    
                split_node = GameTreeNode(split_sequence, new_scores, 1 - self.player_turn, self, self.depth + 1)
                self.children.append(split_node)
                split_node.generate_children(max_depth)
    
            if num == 4:
                split_sequence = self.sequence[:i] + [2, 2] + self.sequence[i+1:]
                split_scores = new_scores[:]
                split_scores[self.player_turn] += 1
    
                split_node = GameTreeNode(split_sequence, split_scores, 1 - self.player_turn, self, self.depth + 1)
                self.children.append(split_node)
                split_node.generate_children(max_depth)