import copy
from operator import attrgetter

# CSP variables
domain = ['R', 'G', 'B']

# Map input as adjacency matrix
# WA, NT, SA, Q, NSW, V, T
map = [[0, 1, 1, 0, 0, 0, 0],
       [1, 0, 1, 1, 0, 0, 0],
       [1, 1, 0, 1, 1, 1, 0],
       [0, 1, 1, 0, 1, 0, 0],
       [0, 0, 1, 1, 0, 1, 0],
       [0, 0, 1, 0, 1, 0, 0],
       [0, 0, 0, 0, 0, 0, 0]]

states = {
  0: 'WA', 1: 'NT', 2: 'SA', 3: 'Q', 4: 'NSW', 5: 'V', 6: 'T'
}

# List of not yet assigned states
unassigned = []
# List of already assigned states
assigned = []
# Conflic domain fo currently inspected vertex
conflictDomain = []

class Vertex:
    def __init__(self, id, degree, constraints, domain):
        self.id = id
        self.degree = degree
        self.constraints = constraints
        self.domain = domain
        self.color = None

## Function to load vertices from adjacency matrix
def loadMap():
    for index, row in enumerate(map):
        constraints = [i for i, val in enumerate(row) if val == 1]
        unassigned.append(Vertex(index, len(constraints), constraints, copy.deepcopy(domain)))

## Function to check if all of the constraints are satisfied
def constraintsSatisfied(constraints, color):
    for constraintId in constraints:
        if [x for x in assigned if x.id == constraintId and x.color == color]:
            conflictDomain.append(constraintId)
            return False

    return True

## Function to assign color to given state
def assignColor(vertex, color, index):
    vertex.color = color
    vertex.domain.pop(index)
    assigned.append(vertex)

## Function to find possible color
def findColor(vertex):
    for index, color in enumerate(vertex.domain):
        if vertex.constraints:
            if constraintsSatisfied(vertex.constraints, color):
                assignColor(vertex, color, index)
                return color
        else:
            assignColor(vertex, color, index)
            return color

    return None

## Tries to reassign last color, if unable to returns false
def reassignLast():
    last = assigned[len(assigned) - 1]

    for index, color in enumerate(last.domain):
        if last.constraints:
            if constraintsSatisfied(last.constraints, color):
                last.domain.pop(index)
                last.color = color
                return True
        else:
            last.domain.pop(index)
            last.color = color
            return True

    assigned.pop(len(assigned) - 1)
    unassigned.append(last)

    last.domain = copy.deepcopy(domain)
    last.color = None

    return False

## Backjumping loop, tries to backjump until a change is possible, if no change is possible and we reach the index 0, the problem does not have a solution
def backjump():
    global assigned

    # Backjump the conflict domain one by one, if not possible return failure
    while conflictDomain:
        index = conflictDomain.pop(len(conflictDomain) - 1)

        # If we already backjumped to the beginning of assigned vertices and there is no other solution, return failure
        if assigned:
            conflictIndex = [i for i, val in enumerate(assigned) if val.id == index][0]
        else:
            return False
        
        newlyUnassigned = assigned[conflictIndex + 1:]
        assigned = assigned[:conflictIndex + 1]

        # Append newly unassigned vertices and reset their domains
        for entry in newlyUnassigned:
            entry.domain = copy.deepcopy(domain)
            entry.color = None
        
        unassigned.extend(newlyUnassigned)

        # Try to reassign last vertex in assigned to a new color
        if reassignLast():
            return True

    return False

## Helper function to print the solution if found
def printSolution():
    for state in assigned:
        print(states[state.id] + ': ' + state.color)

## Constraint satisfaction problem solver main loop
def CSP():
    global conflictDomain

    while unassigned:
        # Pick next state based on max degree heuristic
        maxIndex = max(unassigned, key=attrgetter('degree'))
        vertex = unassigned.pop(unassigned.index(maxIndex))

        # Clear the conflict domain
        conflictDomain = []
        color = findColor(vertex)

        # If coloring was successful, filter domains
        if color:
            continue
        # If coloring was not successful, backjump
        else:
            if not backjump():
                break


## MAIN
if __name__ == '__main__':
    loadMap()
    
    CSP()

    if not unassigned:
        print('\nSOLUTION FOUND\n')
        printSolution()
    else:
        print('\nTHIS CSP DOES NOT HAVE A VALID SOLUTION\n')
