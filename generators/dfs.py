from random import shuffle
import numpy as np 

class Node:
    """ Node class for graph generation

    Attributes:
        x: X-Coordinate of the Node for later array transformation
        y: Y-Coordinate of the Node for later array transformation
        neighbors: A set of nodes that are connecting to this node
        start: A boolean inicating to starting node
        goal: A boolean indicating the goal node
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.neighbors = set()
        self.start = False
        self.goal = False

    def compare(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def print(self):
        print("X:{} Y:{}".format(self.x,self.y))
        print("Neighbors:")
        for elem in self.neighbors:
            print("Xn:{},Yn:{}".format(elem.x,elem.y)) 
    
    def removeEdge(self, node):
        for elem in self.neighbors:
            if node.compare(elem):
                self.neighbors.remove(elem)
                elem.neighbors.remove(self)
                return
        return NotImplemented

def __createEdge(node1, node2):
    node1.neighbors.add(node2)
    node2.neighbors.add(node1)
    

def __delEdgeFromGraph(graph, node1, node2):
    for r in graph:
        for e in r:
            if e.compare(node1):
                e.removeEdge(node2)
                
def __graph(x: int, y: int):
    """ Graph creator

    Generates a graph in array form with edges.

    Args: 
        x: An integer value for the graph width
        y: An integer value for the graph height

        Values must be uneven.

    Returns:
        A list containing rows of a connected maze graph
    """

    above = []
    left = None
    graph = []
    for j in range(1,y+1,2):
        row = []
        tmp = []
        for i in range(1,x+1,2):
            n = Node(i,j)
            # save start/goal nodes
            if i == 1 and j == 1:
                    n.start = True
            if i == x and j == y:
                n.goal = True
            # connect to the node on the left
            if left is not None:
                __createEdge(left,n)
            # connect to the node above
            if j > 1:
                __createEdge(above[(i//2)],n)
            # update temp variables
            tmp.append(n)
            if i < x:
                left = n
            else:
                left = None
            if i == x:
                above = tmp
                tmp = []
            row.append(n)
        graph.append(row)
    return graph

def __rndDFS(start: Node, visited: list, wallGraph: list):
    """ Randomized Depth First Search implementation

    Traverses a graph recursively from a starting node while deleting edges from a secondary graph
    represented in array form. 

    Attributes:
        start: Starting node of the traversal graph
        visited: List of nodes already traversed
        wallGraph: Graph array from which edges are deleted
    """

    if start.goal:
        return visited
    stack = list(start.neighbors)
    shuffle(stack)
    if visited is None:
        visited = []
    visited.append(start)
    for node in stack:
        if node not in visited:
            __delEdgeFromGraph(wallGraph, start, node)
            __rndDFS(node, visited, wallGraph)
            visited.append(node)
    return visited

def generateDFS(x: int,y: int):
    """ Maze generator function based on depth first search

    Args: 
        x: An integer value for the graph width
        y: An integer value for the graph height

    Returns:
        A 2D numpy array containing ones and zeros. Ones represent walls, while 0 marks a traversable field
    
    """
    graph_width = x - 2 - (1 - x%2)
    graph_height = y - 2 - (1 - y%2)
    travGraph = __graph(graph_width,graph_height)
    wallGraph = __graph(graph_width,graph_height)
    __rndDFS(travGraph[0][0], None, wallGraph)
    maze = []
    maze = np.full((x,y),0)
   
    for i in range(2,y,2):
        for j in range(2,x,2):
            maze[j,i] = 1
    
    for r in wallGraph:
        for e in r:
            maze[e.x,e.y] = 0
            for n in e.neighbors:
                maze[(e.x+n.x)//2][(e.y+n.y)//2] = 1
    # fills borders and unaccessable fields
    maze[[0,-1],:] = 1
    maze[:,[0,-1]] = 1
    if x%2==0:
        maze[[0,-2],:] = 1
    if y%2==0:
        maze[:,[0,-2]] = 1
    # set entrance and exit 
    maze[0][1] = 0  
    maze[x-1][y-2] = 0
    if x%2==0:
        maze[x-2,y-2] = 0
        if y%2==0:
            maze[x-2,y-3] = 0
    if y%2==0:
        maze[x-2,y-2] = 0
    return maze
