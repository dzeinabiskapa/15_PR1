from data_structurs import GameTreeNode
from ai_func import AiFunc

class MinimaxAI(AiFunc):
    def __init__(self, game_logic, max_depth=3):
        self.game_logic = game_logic
        self.max_depth = max_depth

    def getBestMove(self):
        # izveidojam spēles koka saknes mezglu ar pašreizējo spēles stāvokli
        root = GameTreeNode(
            sequence = self.game_logic.sequence, # spēles ciparu virkne
            scores = self.game_logic.scores, # abu spēlētāju punkti
            player_turn = self.game_logic.player_turn, # kura spēlētāja kārta
            depth = 0 # saknes dziļums ir 0 (sākuma stāvoklis)
        )

        # ģenerē visus iespējamos turpmākos gājienus (bērnus) līdz maksimālajam dziļumam (3)
        root.generate_children(max_depth = self.max_depth) 
        
        bestValue = -float('inf') # sākotnējā labākā vērtība (mazākā iespējamā, lai atrastu maksimālo, jo jebkura vērtība būs par to lielāka)
        bestMove = None # labākais gājiens, pašlaik nav atrasts

        # ejam cauri katram iespējamam gājienam (bērnu mezglam)
        for child in root.children:
            # rekursīvi izsaucam minimax, nākamais līmenis pēc saknes būs 1 (dziļums 1) 
            # isMaximising nosaka, ka pirmais līmenis vienmēr ir MAX, t.i., AI ir maksimizētājs,
            # kas būs patiesi, jo minimax tiek palaistss uz katru AI gājienu
            value = self._minimax(child, depth = 1, isMaximizing = True)

            # gājiena vērtējuma salīdzināšana
            if value > bestValue: # ja pašreizējais gājiens ir labāks par iepriekšējo labāko, tad
                bestValue = value # tas kļūst par labāko gājienu (pārrakstīšana)
                bestMove = self._getMoveFromChild(root, child) # atrodam atbilstošo gājienu (mezgls pārtop par gājienu spēlē)

        return bestMove

    def _minimax(self, node, depth, isMaximizing):
        # algoritma beigu nosacījum, t.i., beigt, ja sasniegts maksimālais dziļums vai beidzas spēles stāvoklis
        if depth == self.max_depth or not node.sequence:
            return self._evaluate(node, isMaximizing) # heiristiskā vērtība attiecīgajam mezglam

        if isMaximizing: # maksimizētāja (AI) kārta
            value = -float('inf') # sākotnējā vērtība

            # visu iespējamo gājienu (bērnu) analīze:
            for child in node.children:
                # rekursīvi iegūst bērna vērtību 
                # katrs rekursīvais izsaukums pārvietojas vienu līmeni dziļāk spēles kokā (depth +1)
                # nākamais spēlētājs būs minimizētājs - False
                # izvēlamies labāko (maksimālo) vērtību no visiem iespējamiem bērniem
                value = max(value, self._minimax(child, depth + 1, False))

            return value
        else: # minimizētāja (cilvēka) kārta
            value = float('inf') # sākotnējā vērtība ir +bezgalība, t.i., meklējot mazāko vērtību, jebkas būs mazāks par to

            # pretinieka gājienu analīze
            for child in node.children:
                # rekursīvi iegūst bērna vērtību 
                # katrs rekursīvais izsaukums pārvietojas vienu līmeni dziļāk spēles kokā (depth +1)
                # nākamais spēlētājs būs maksimizētājs - True
                # pieņemam, ka pretinieks izvēlēsies priekš AI nelabvēlīgāko (minimālo) gājienu
                value = min(value, self._minimax(child, depth + 1, True))

            return value