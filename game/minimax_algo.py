from collections import Counter
from data_structurs import GameTreeNode
from ai_func import AiFunc

class MinimaxAI(AiFunc):
    def __init__(self, game_logic, max_depth=3):
        self.game_logic = game_logic
        self.max_depth = max_depth

    def getBestMove(self):
        #print("Minimax")
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
        print(f"Generated {len(root.children)} possible moves")

        bestValue = -float('inf')
        bestMove = None

        for child in root.children:
            value = self._minimax(child, depth = 1, isMaximizing = True)
            if value > bestValue:
                bestValue = value
                bestMove = self._getMoveFromChild(root, child)

        print(f"Best Move: {bestMove}")
        return bestMove

    def _minimax(self, node, depth, isMaximizing):
        if depth == self.max_depth or not node.sequence:
            return self._evaluate(node, isMaximizing)

        if isMaximizing:
            value = -float('inf')

            for child in node.children:
                value = max(value, self._minimax(child, depth + 1, False))

            return value
        else:
            value = float('inf')

            for child in node.children:
                value = min(value, self._minimax(child, depth + 1, True))

            return value