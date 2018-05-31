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

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
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

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())

    visited = dict()
    state = problem.getStartState()
    action = []
    if DFS(problem, state, action, visited):
        return action

def DFS(problem, state, action, visited):
  if problem.isGoalState(state):
    return True

  for child in problem.getSuccessors(state):
      current_state = child[0]
      if not visited.has_key(hash(current_state)):
          visited[hash(current_state)] = current_state
          action.append(child[1])
          if DFS(problem, current_state, action, visited) == True:
              return True
          action.pop()
  return False

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())

    visited = dict()
    state = problem.getStartState()
    actions = []
    myQueue = util.Queue()
    node = {}
    node["state"] = state
    node["action"] = None
    node["parent"] = None

    myQueue.push(node)

    while myQueue.isEmpty != True:
        node = myQueue.pop()
        state = node["state"]
        action = node["action"]

        if problem.isGoalState(state) == True:
            break
        if not visited.has_key(state):
            visited[state] = True
            for child in problem.getSuccessors(state):
                    if not visited.has_key(child[0]):
                        new_node = {}
                        new_node["parent"] = node
                        new_node["state"] = child[0]
                        new_node["action"] = child[1]
                        myQueue.push(new_node)

    while node["action"] != None:
        actions.insert(0, node["action"])
        node = node["parent"]

    return actions


    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

#     Insert the root into the queue
# While the queue is not empty
#       Dequeue the maximum priority element from the queue
#       (If priorities are same, alphabetically smaller path is chosen)
#       If the path is ending in the goal state, print the path and exit
#       Else
#             Insert all the children of the dequeued element, with the cumulative costs as priority
    myQueue = util.PriorityQueue()
    state = problem.getStartState()
    visited = dict()
    actions = []

    node = {}
    node["parent"] = None
    node["state"] = state
    node["action"] = None
    node["cost"] = 0

    myQueue.push(node, node["cost"])

    while myQueue.isEmpty != True:
        node = myQueue.pop()
        state = node["state"]
        action = node["action"]
        cost = node["cost"]

        if problem.isGoalState(state) == True:
            break

        if not visited.has_key(state):
            visited[state] = True
            for child in problem.getSuccessors(state):
                    if not visited.has_key(child[0]):
                        new_node = {}
                        new_node["parent"] = node
                        new_node["state"] = child[0]
                        new_node["action"] = child[1]
                        new_node["cost"] = child[2]
                        myQueue.push(new_node, new_node["cost"]) #priority queue from util handles the cost calculation for us

    while node["action"] != None:
            actions.insert(0, node["action"])
            node = node["parent"]

    return actions



    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    myQueue = util.PriorityQueue()
    visited = dict()
    actions = []
    state = problem.getStartState()
    node = {}
    node["parent"] = None
    node["action"] = None
    node["state"] = state
    node["cost"] = 0
    node["eval"] = heuristic(state, problem) #heuristic passed in will be manhattanHeuristic from
    #A* use f(n) = g(n) + h(n)
    myQueue.push(node, node["cost"] + node["eval"]) #the PriorityQueue will take care of evaluating the highest cost

    while myQueue.isEmpty() != True:
            node = myQueue.pop()
            state = node["state"]
            cost = node["cost"]
            v = node["eval"]

            if visited.has_key(state):
              continue

            if problem.isGoalState(state) == True:
              break

            for child in problem.getSuccessors(state):
                    visited[state] = True
                    if not visited.has_key(child[0]):
                        sub_node = {}
                        sub_node["parent"] = node
                        sub_node["state"] = child[0]
                        sub_node["action"] = child[1]
                        sub_node["cost"] = child[2] + cost
                        sub_node["eval"] = heuristic(sub_node["state"], problem) #manhattanHeuristic will be passed in place which will compute cost to goal.
                        myQueue.push(sub_node, sub_node["cost"] + node["eval"])


    while node["action"] != None:
            actions.insert(0, node["action"])
            node = node["parent"]

    return actions

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
