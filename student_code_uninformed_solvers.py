
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        current = self.currentState
        if current.state == self.victoryCondition:
            return True

        else:
            poss_moves = self.gm.getMovables()
            if not current.children and poss_moves:
                for i in poss_moves:
                    self.gm.makeMove(i)
                    curr_depth = current.depth+1
                    next = GameState(self.gm.getGameState(), curr_depth, i)
                    current.children.append(next)
                    next.parent = current
                    self.gm.reverseMove(i)

        while len(current.children) > current.nextChildToVisit:
            next = current.children[current.nextChildToVisit]
            current.nextChildToVisit = current.nextChildToVisit + 1

            if next not in self.visited:
                self.go(next)
                if self.currentState.state == self.victoryCondition:
                    return True
                break
            self.back()
        return False

    def go(self, next):
        self.visited[next] = True
        self.gm.makeMove(next.requiredMovable)
        self.currentState = next

    def back(self):
        while self.currentState and self.currentState.nextChildToVisit == len(self.currentState.children):
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState - self.currentState.parent

class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        current = self.currentState
        if current.state == self.victoryCondition:
            return True
        self.visited[current] = True

        poss_moves = self.gm.getMovables()
        if poss_moves and not current.children:
            for i in poss_moves:
                self.gm.makeMove(i)
                state_new = GameState(self.gm.getGameState(), current.depth + 1, i)
                state_new.parent = current
                current.children.append(state_new)
                self.gm.reverseMove(i)

        self.search()
        return False

    def search(self):
        while self.currentState.parent and len(self.currentState.parent.children) - 1 == self.find(self.currentState):
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent

        if self.currentState.parent:
            self.gm.reverseMove(self.currentState.requiredMovable)
            index_new = self.find(self.currentState) + 1
            self.currentState = self.currentState.parent.children[index_new]
            self.gm.makeMove(self.currentState.requiredMovable)

        while self.visited.get(self.currentState, False) and self.currentState.children:
            child1 = 0
            self.currentState = self.currentState.children[child1]
            self.gm.makeMove(self.currentState.requiredMovable)

        if self.visited.get(self.currentState, False):
            self.search()
        return True

    def find(self, state):
        index = state.parent.children.index(state)
        return index
