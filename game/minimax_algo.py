from data_structurs import GameTreeNode

class MinimaxAI:
    def __init__(self, game_logic, max_depth=3):
        self.game_logic = game_logic
        self.max_depth = max_depth

    def getBestMove(self):
        root = GameTreeNode(
            sequence = self.game_logic.sequence,
            scores = self.game_logic.scores,
            player_turn = self.game_logic.player_turn,
            depth = 0
        )

        root.generate_children(max_depth = self.max_depth)

        bestValue = -float('inf')
        bestMove = None

        for child in root.children:
            value = self._minimax(child, depth = 1, isMaximizing = False)
            if value > bestValue:
                bestValue = value
                bestMove = self._getMoveFromChild(root, child)

        return bestMove

    def _minimax(self, node, depth, isMaximizing):
        if depth == self.max_depth or not node.sequence:
            return self._evaluate(node)

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

    def _evaluate(self, node):
        delta = node.scores[1] - node.scores[0]

        # Check for the presence of '4' in the sequence
        fourExists = 4 in node.sequence
        aN4 = 1 if fourExists else 0

        # Check for the presence of '3' in the sequence (only if there is no '4')
        threeExists = 3 in node.sequence and not fourExists
        aN3 = 1 if threeExists else 0

        # Find the highest number in the sequence
        highestFigure = max(node.sequence) if node.sequence else 0
        aHighest = highestFigure

        # Check for the presence of '2' in the sequence (only if there are no '3' or '4')
        twoExists = 2 in node.sequence and not (threeExists or fourExists)
        aN2 = 1 if twoExists else 0

        # Calculate the heuristic value
        fN = delta + 0.5 * aN4 + 0.4 * aN3 + 0.3 * aHighest + 0.15 * aN2
        return fN

    def _getMoveFromChild(self, parent, child):
        for i, num in enumerate(parent.sequence):
            if num not in child.sequence:
                return ("take", i)
            elif num == 2 and child.sequence.count(1) == 2:
                return ("split", i)
            elif num == 4 and child.sequence.count(2) == 2:
                return ("split", i)
            
        return None
    