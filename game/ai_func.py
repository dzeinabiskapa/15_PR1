from collections import Counter
class AiFunc:
    def _evaluate(self, node, isMaximizing):
        delta = node.scores[1] - node.scores[0]

        if not isMaximizing:
            delta = -delta
    
        fourExists = 4 in node.sequence
        aN4 = 1 if fourExists else 0
    
        threeExists = 3 in node.sequence and not fourExists
        aN3 = 1 if threeExists else 0
    
        highestFigure = max(node.sequence) if node.sequence else 0
        aHighest = highestFigure
    
        twoExists = 2 in node.sequence and not (threeExists or fourExists)
        aN2 = 1 if twoExists else 0
    
        fN = delta + 0.7 * aN4 + 0.4 * aN3 + 0.3 * aHighest + 0.2 * aN2
        return fN

    def _getMoveFromChild(self, parent, child):
        parentCounts = Counter(parent.sequence)
        childCounts = Counter(child.sequence)
    
        for num in parentCounts:
            if parentCounts[num] == childCounts[num] + 1:
                for i in range(len(parent.sequence)):
                    if i >= len(child.sequence) or parent.sequence[i] != child.sequence[i]:
                        if parent.sequence[i] == num:
                            print(f"Move: Take number {num} at index {i}")  # for debug
                            return ("take", i)
    
        if childCounts[1] == parentCounts[1] + 2 and childCounts[2] == parentCounts[2] - 1:
            for i, num in enumerate(parent.sequence):
                if num == 2:
                    print(f"Move: Split number {num} at index {i}")  # for debug
                    return ("split", i)
        elif childCounts[2] == parentCounts[2] + 2 and childCounts[4] == parentCounts[4] - 1:
            for i, num in enumerate(parent.sequence):
                if num == 4:
                    print(f"Move: Split number {num} at index {i}")  # for debug
                    return ("split", i)
    
        print("No valid move found!")  # for debug
        return None  # Return None if no move is found 