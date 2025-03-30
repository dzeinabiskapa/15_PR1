from collections import Counter
from data_structurs import GameTreeNode
from ai_func import AiFunc

class AlphaBetaAI(AiFunc):
    def __init__(self, game_logic, max_depth=3):
        self.game_logic = game_logic
        self.max_depth = max_depth

    def getBestMove(self):
        #print("Alpha-Beta")
        print(f"Current Sequence: {self.game_logic.sequence}")  # for debug
        print(f"Current Scores: {self.game_logic.scores}")  # for debug
        print(f"Player Turn: {self.game_logic.player_turn}")  # for debug
        root = GameTreeNode(
            sequence = self.game_logic.sequence,
            scores = self.game_logic.scores,
            player_turn = self.game_logic.player_turn,
            depth = 0
        )

        root.generate_children(max_depth = self.max_depth)

        bestValue = -float('inf')
        bestMove = None
        alpha = -float('inf')
        beta = float('inf')

        for child in root.children:
            value = self._alphabeta(child, depth = 1, alpha=alpha, beta=beta, isMaximizing = True)
            if value > bestValue:
                bestValue = value
                bestMove = self._getMoveFromChild(root, child)
            alpha = max(alpha, bestValue)

        print(f"Best Move: {bestMove}")
        return bestMove

    def _alphabeta(self, node, depth, alpha, beta, isMaximizing):
        if depth == self.max_depth or not node.sequence:
            return self._evaluate(node, isMaximizing)

        if isMaximizing:
            value = -float('inf')

            for child in node.children:
                value = max(value, self._alphabeta(child, depth + 1, alpha, beta, False))
                alpha = max(alpha, value)
                if alpha >= beta: #beta nogriezšana
                    break

            return value
        else:
            value = float('inf')

            for child in node.children:
                value = min(value, self._alphabeta(child, depth + 1, alpha, beta, True))
                beta = min(beta, value)
                if beta <= alpha: #alpha nogriezšana
                    break

            return value