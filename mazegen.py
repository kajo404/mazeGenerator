"""Maze Generator

This module allows the creation of mazes. The Maze has one guaranteed path from start to goal, with walls surrounding
the maze area. 

    Typical usage example:
    import mazeGen
    maze = mazeGen.generateMaze(45,45,'dfs')
    mazeGen.savePNG(maze,'path')

Creates a file called path.png containing a 45 x 45 maze.

"""

from random import shuffle
import numpy as np 
import png
import generators.dfs as dfs


def generateMaze(x: int, y:int, strategy='dfs'):
    """ Maze generator function

    Args:
        x: An integer value for the graph width
        y: An integer value for the graph height
        strategy: A string containing the strategy to use for maze generation. See below for available strategies.
    
    Returns:
        A 2D numpy array containing ones and zeros. Ones represent walls, while 0 marks a traversable field

    Strategies:
        dfs: Uses Depth First Search to generate the maze. Path from start to goal is generally quite long with few branches
    """

    if strategy == "dfs":
        return dfs.generateDFS(x,y)
    else:
        raise ValueError("Invalid strategy: " + strategy)

def savePNG(maze, fileName: str):
    """ Maze generator that saves result as PNG
    
    Args:
        maze: Numpy array containing a maze.
        fileName: String for the filename to save the maze under.
    """
    # make pathways white and walls black
    maze = maze.astype(np.uint8)
    maze[maze==0] = 255
    maze[maze==1] = 0
    png.from_array(maze,'L').save(fileName + ".png")

    