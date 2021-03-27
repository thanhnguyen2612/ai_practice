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

REVERSE_PUSH = False

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
    graph = GraphSearch(problem, util.Stack())
    actions = graph.search()
    return actions


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    graph = GraphSearch(problem, util.Queue())
    actions = graph.search()
    return actions

def uniformCostSearch(problem):
    graph = GraphSearch(problem, util.PriorityQueue())
    actions = graph.search()
    return actions

def depthLimitSearch(problem, limit=3):
    graph = GraphSearch(problem, util.Stack())
    actions = graph.search(limit)
    return actions

def iterativeDeepeningSearch(problem):
    limit = 100
    for depth in range(limit):
        graph = GraphSearch(problem, util.Stack())
        actions = graph.search(depth)
        if actions:
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
    graph = GraphSearch(problem, util.PriorityQueue(), heuristic)
    actions = graph.aStarSearch()
    return actions

def bestFirstSearch(problem, heuristic=nullHeuristic):
    graph = GraphSearch(problem, util.PriorityQueue(), heuristic)
    actions = graph.bestFirstSearch()
    return actions

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
ucs = uniformCostSearch
dls = depthLimitSearch
ids = iterativeDeepeningSearch
astar = aStarSearch

class Node:
    def __init__(self, state, parent, action, depth=0, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
        self.cost = cost
    
    def __eq__(self, other):
        return self.state == other.state and self.parent == other.parent \
            and self.action == other.action and self.depth == other.depth \
            and self.cost == other.cost
    
    def __hash__(self):
        return hash(self.state) + hash(self.parent) + hash(self.action) + self.depth + self.cost
    
    def __str__(self):
        return f"{self.parent}->{self.state}"

# Generic graph search
class GraphSearch:
    def __init__(self, problem, fringe, heuristic=nullHeuristic):
        self.problem = problem
        self.fringe = fringe
        self.explored = set()
        self.heuristic = heuristic
        self.algorithm = None
    
    def search(self, limit=-1):
        start_node = Node(state=self.problem.getStartState(), parent=None, action=None)
        # self.fringe.push(start_node)
        self.pushFringe(start_node)

        while not self.fringe.isEmpty():
            node = self.fringe.pop()

            if self.problem.isGoalState(node.state):
                actions = []
                while node.parent is not None:
                    actions.append(node.action)
                    node = node.parent
                actions.reverse()
                return actions
            elif limit >= 0 and node.depth == limit:     # Cutoff
                self.explored.add(node.state)
                continue
            
            self.explored.add(node.state)
            for child, action, cost in self.problem.expand(node.state):
                if child not in self.explored:
                    child_node = Node(state=child, parent=node, action=action, 
                                            depth=node.depth + 1, cost=node.cost + cost)
                    self.pushFringe(child_node)
        return []
    
    def pushFringe(self, node):
        if isinstance(self.fringe, util.PriorityQueue):
            if self.algorithm == 'aStar':
                self.fringe.push(node, node.cost + self.heuristic(node.state, self.problem))
            elif self.algorithm == 'bfs':
                self.fringe.push(node, self.heuristic(node.state, self.problem))
            else:
                self.fringe.push(node, node.cost)
        else:
            self.fringe.push(node)
    
    def bestFirstSearch(self):
        self.algorithm = 'bfs'
        return self.search()

    def aStarSearch(self):
        self.algorithm = 'aStar'
        return self.search()