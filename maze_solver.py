# How to generate new mazes: http://www.delorie.com/game-room/mazes/genmaze.cgi
# Arguments: mazefile, walking speed

# Imported Libraries
import copy
import sys
import os
import time

# method: create a maze grid, 2d array
# input: filename
# output: 2d array
# effects: none
def create_maze(filename):
  f = open(filename)
  maze = [[char for char in line if char != '\n'] for line in f.readlines()]
  f.close()
  return maze

# method: recursive method to find the optimal path through a maze
# input: 2d array, x,y (current position), list (backtracked path)
# output: Boolean, if a path is found
# effects: Maze is updated with every tried position, path contains optimal route
def solve_maze(maze, x, y, path):

  # If an exit is found, a solution is found
  if x >= len(maze) or y >= len(maze[x]) or x < 0 or y < 0:
    return True
  
  # If a wall or previous position is found, try another route
  if maze[x][y] == '|' or maze[x][y] == '+' or maze[x][y] == '-' or maze[x][y] == '#':
    return False
  
  maze[x][y] = '#'

  # Check all four options for continuing the path
  if solve_maze(maze, x + 1, y, path):
    path.append((x, y))
    return True
  if solve_maze(maze, x, y + 1, path):
    path.append((x, y))
    return True
  if solve_maze(maze, x - 1, y, path):
    path.append((x, y))
    return True
  if solve_maze(maze, x, y - 1, path):
    path.append((x, y))
    return True
  
  return False

# method: print a maze
# input: 2d array (maze)
# output: none
# effects: none
def print_maze(maze):
  for line in maze:
    for char in range(len(line)):
      print(line[char], end=" ")
    print()

# method: Print a maze repeatedly with an updating path, simulates movement
# input: 2d array (maze), path (optimal route), speed (how fast the path should develop)
# output: none
# effects: none
def print_maze_graphic(maze, path, speed):

  # Create replacement for maze and path
  temp_maze = copy.deepcopy(maze)
  temp_path = []
  for move in path[::-1]:

    # Clear temp_maze, add next step to path, and inject 3 steps into maze,
    temp_path.append(move)
    temp_maze = copy.deepcopy(maze)
    temp_maze = fill_solution(temp_maze, temp_path[-3:])
    print_maze(temp_maze)

    # pause maze update, then clear screen
    time.sleep(speed/100)
    os.system('cls||clear')
  
  # Print final, full path
  temp_path.append(move)
  temp_maze = fill_solution(temp_maze, temp_path)
  print_maze(temp_maze)

# method: Fill an empty maze with a given path
# input: maze, path
# output: maze
# effects: none
def fill_solution(maze, path):
  for coor in path:
    maze[coor[0]][coor[1]] = 'x'
  return maze

# Main
if __name__ == "__main__":
  maze_name = "Sample_Mazes/" + sys.argv[1]
  maze = create_maze(maze_name)
  path = []

  # find if maze is solvable, if so print out simulation
  out = solve_maze(maze, 1, 0, path)
  print_maze_graphic(create_maze(maze_name), path, int(sys.argv[2]))