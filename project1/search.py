# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    @Return
        actions: a list of actions to reach solution
    """
    "*** YOUR CODE HERE ***"
    searchAgent = GraphSearch(problem, util.Stack())
    actions = searchAgent.search()
    costs = searchAgent.getCostOfActionSequence(actions)
    print(f"DFS found a path of {len(actions)} moves with {costs} costs")
    return actions

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    searchAgent = GraphSearch(problem, util.Queue())
    actions = searchAgent.search()
    costs = searchAgent.getCostOfActionSequence(actions)
    print(f"BFS found a path of {len(actions)} moves with {costs} costs")
    return actions

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch

class Node:
    def __init__(self, state, parent, action, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost

class GraphSearch(SearchProblem):
    def __init__(self, problem, fringe, heuristic=nullHeuristic):
        self.problem = problem
        self.fringe = fringe
        self.explored = set()
        self.heuristic = heuristic
    
    def search(self):
        start_node = Node(state=self.getStartState(), parent=None, action=None)
        self.fringe.push(start_node)

        while not self.fringe.isEmpty():
            node = self.fringe.pop()

            if self.isGoalState(node.state):
                actions = []
                while node.parent is not None:
                    actions.append(node.action)
                    node = node.parent

                actions.reverse()
                return actions
            
            self.explored.add(node.state)
            for child, action, cost in self.expand(node.state):
                if child not in self.explored:
                    child_node = Node(state=child, parent=node, action=action, cost=cost)
                    self.fringe.push(child_node)
        return []

    def getStartState(self):
        return self.problem

    def isGoalState(self, state):
        return state.isGoal()

    def expand(self, state):
        child = []
        for action in self.getActions(state):
            next_state = self.getNextState(state, action)
            child.append((next_state, action, self.getActionCost(state, action, next_state)))
        return child

    def getActions(self, state):
        return state.legalMoves()

    def getActionCost(self, state, action, next_state):
        assert next_state == state.result(action), (
            "getActionCost() called on incorrect next state.")
        return action.cost

    def getNextState(self, state, action):
        assert action in self.getActions(state), (
            "getNextState() called on incorrect action")
        return state.result(action)

    def getCostOfActionSequence(self, actions):
        costs = 0
        cur = self.problem
        for action in actions:
            costs += self.getActionCost(cur, action, self.getNextState(cur, action))
            cur = self.getNextState(cur, action)
        return costs