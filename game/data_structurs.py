




class GameTreeNode:
    """Represents a node in the game tree."""
    def __init__(self, sequence, scores, player_turn, parent=None):
        self.sequence = sequence  # Current sequence
        self.scores = scores  # Player scores [P1, P2]
        self.player_turn = player_turn  # 0 for P1, 1 for P2
        self.children = []  # nakamie gajieni
        self.parent = parent  # Backtracking
  
    def generate_children(self):
        """Generates all possible next game states."""
        for i, num in enumerate(self.sequence):
            # Copy game state
            new_sequence = self.sequence[:i] + self.sequence[i+1:]
            new_scores = self.scores[:]
            new_scores[self.player_turn] += num  # Taking the number

            # izveido bērnus
            child_node = GameTreeNode(new_sequence, new_scores, 1 - self.player_turn, self)
            self.children.append(child_node)

            # Handle splitting rules
            if num == 2:
                split_sequence = self.sequence[:i] + [1, 1] + self.sequence[i+1:]
                split_node = GameTreeNode(split_sequence, new_scores, 1 - self.player_turn, self)
                self.children.append(split_node)

            if num == 4:
                split_sequence = self.sequence[:i] + [2, 2] + self.sequence[i+1:]
                split_scores = new_scores[:]
                split_scores[self.player_turn] += 1  # Gain 1 point for splitting 4
                split_node = GameTreeNode(split_sequence, split_scores, 1 - self.player_turn, self)
                self.children.append(split_node)

    def print_tree(self, depth=0):
        """Recursively prints the tree for debugging."""
        print(" " * depth * 4, f"Player {self.player_turn + 1}, Scores: {self.scores}, Sequence: {self.sequence}")
        for child in self.children:
            child.print_tree(depth + 1)

# Example usage: Generate tree from an initial state
#initial_scores = [0, 0]
#root = GameTreeNode(initial_sequence, initial_scores, 0)
#root.generate_children()

# Print the tree
#root.print_tree()