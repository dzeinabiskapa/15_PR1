from data_structurs import GameTreeNode
from ai_func import AiFunc

class AlphaBetaAI(AiFunc):
    def __init__(self, game_logic, max_depth=3):
        self.game_logic = game_logic
        self.max_depth = max_depth

    def getBestMove(self):
        # print("Alpha-Beta")  # Debug 
        # print(f"Current Sequence: {self.game_logic.sequence}")  # Pašreizējā secība (virkne ar skaitļiem)
        # print(f"Current Scores: {self.game_logic.scores}")  # Pašreizējie rezultāti (abiem spēlētājiem)
        # print(f"Player Turn: {self.game_logic.player_turn}")  # Kurš spēlētājs ir pie gājiena

        # Izveido saknes mezglu spēles kokam
        root = GameTreeNode(
            sequence = self.game_logic.sequence,
            scores = self.game_logic.scores,
            player_turn = self.game_logic.player_turn,
            depth = 0
        )

        # Ģenerē visus iespējamos nākamos gājienus līdz noteiktam dziļumam
        root.generate_children(max_depth = self.max_depth)

        bestValue = -float('inf')  # Sākotnēji – vissliktākais iespējamais rezultāts
        bestMove = None
        alpha = -float('inf')  # Alfa sākuma vērtība (maksimizētājs)
        beta = float('inf')    # Beta sākuma vērtība (minimizētājs)

        # Apskata visus bērnus (iespējamos gājienus)
        for child in root.children:
            value = self._alphabeta(child, depth = 1, alpha=alpha, beta=beta, isMaximizing = True)
            if value > bestValue:
                bestValue = value
                bestMove = self._getMoveFromChild(root, child)  # Atrod, kāds gājiens veda pie šī stāvokļa
            alpha = max(alpha, bestValue)  # Atjauno alfa vērtību (labākā zināmā vērtība maksimizētājam)

        #print(f"Best Move: {bestMove}")  # Izvade: labākais atrastais gājiens
        return bestMove

    def _alphabeta(self, node, depth, alpha, beta, isMaximizing):
        # Sasniegts maksimālais dziļums vai vairs nav pieejamu skaitļu (gājienu)
        if depth == self.max_depth or not node.sequence:
            return self._evaluate(node, isMaximizing)  # heiristiskā vērtība attiecīgajam mezglam

        if isMaximizing:
            value = -float('inf')  # Sākuma vērtība maksimizētājam

            for child in node.children:
                # Rekursīvi izsauc algoritmu nākamajam līmenim (minimizētājs būs nākamais)
                value = max(value, self._alphabeta(child, depth + 1, alpha, beta, False))
                alpha = max(alpha, value)  # Atjauno alfa vērtību
                if alpha >= beta:
                    break  # Beta nogriešana – nav jēgas turpināt, jo minimizētājs šo ceļu neizvēlēsies

            return value
        else:
            value = float('inf')  # Sākuma vērtība minimizētājam

            for child in node.children:
                # Rekursīvi izsauc algoritmu nākamajam līmenim (maksimizētājs būs nākamais)
                value = min(value, self._alphabeta(child, depth + 1, alpha, beta, True))
                beta = min(beta, value)  # Atjauno beta vērtību
                if beta <= alpha:
                    break  # Alfa nogriešana – nav jēgas turpināt, jo maksimizētājs šo ceļu neizvēlēsies

            return value
