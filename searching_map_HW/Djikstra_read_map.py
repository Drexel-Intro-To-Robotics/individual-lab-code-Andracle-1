import sys
from PIL import Image
import copy
import queue as Queue
import math
import matplotlib.pyplot as plt

'''
These variables are determined at runtime and should not be changed or mutated by you
'''
start = (0, 0)  # a single (x,y) tuple, representing the start position of the search algorithm
end = (0, 0)  # a single (x,y) tuple, representing the end position of the search algorithm
difficulty = ""  # a string reference to the original import file
G = 0
E = 0
e_list = []
'''
These variables determine display coler, and can be changed by you, I guess
'''
NEON_GREEN = (0, 255, 0)
PURPLE = (85, 26, 139)
LIGHT_GRAY = (50, 50, 50)
DARK_GRAY = (100, 100, 100)

'''
These variables are determined and filled algorithmically, and are expected (and required) be mutated by you
'''
path = []  # an ordered list of (x,y) tuples, representing the path to traverse from start-->goal
expanded = {}  # a dictionary of (x,y) tuples, representing nodes that have been expanded
frontier = {}  # a dictionary of (x,y) tuples, representing nodes to expand to in the future

open = Queue.PriorityQueue()
came_from = {}
cost_so_far = {}

def search(map):
    """
    This function is meant to use the global variables [start, end, path, expanded, frontier] to search through the
    provided map.
    :param map: A '1-concept' PIL PixelAccess object to be searched. (basically a 2d boolean array)
    """
    move = [(1,0), (0,1), (-1,0), (0,-1)] #Move right, down, left, up (Top left corner is (0,0), bottom right is (max,max))

    open.put((0,start))     #Insert 0 cost, start tile into queue.
    came_from[start] = None #Started at start
    cost_so_far[start] = 0  #No cost yet
    frontier[start] = (0, None) #Need to explore start tile first

    while not open.empty(): #While there are still tiles in the queue
        cost, node = open.get() #get the tile

        frontier.pop(node)  #Take tile out of "need to explore"
        expanded[node] = (cost, came_from[node])    #Put into "explored"

        if node == end:     #If tile is last tile
            prev = node     #set prev to last node
            while prev is not None: #and go through all nodes in the path from end to beginning
                path.append(prev)  
                prev = came_from[prev]
            path.reverse()      #reverse it so it actually is the path
            #print(path)
            print(f"Total Cost: {cost_so_far[end]}")
            return

        for x,y in move:    #For the four directions
            next = (node[0] + x, node[1] + y)
            #print(next)
            if next[0] < 0 or next[1] < 0:  #skip if negative
                continue
            try:
                pixel = map[next[0], next[1]]   #set pixel to tile
            except IndexError:  #If pixel is past the limits, fail and continue.
                continue

            if pixel != 0: #Check if wall or not
                next_cost = cost_so_far[node] + 1 #increase cost

                if next not in cost_so_far: #If not discovered
                    cost_so_far[next] = next_cost   #Set current cost
                    came_from[next] = node  #Set as explored

                    open.put((next_cost, next))     #Insert into queue

                    frontier[next] = (next_cost, node) 

            

    
def visualize_search(save_file="do_not_save.png"):
    """
    :param save_file: (optional) filename to save image to (no filename given means no save file)
    """
    im = Image.open(f"maps/"+difficulty).convert("RGB")
    pixel_access = im.load()

    # draw frontier pixels
    for pixel in frontier.keys():
        pixel_access[pixel[0], pixel[1]] = LIGHT_GRAY

    # draw expanded pixels
    for pixel in expanded.keys():
        pixel_access[pixel[0], pixel[1]] = DARK_GRAY
    
    for pixel in path:      #Moved this after because expanded pixels kept over writing it
        #print(pixel)
        pixel_access[pixel[0], pixel[1]] = PURPLE

    pixel_access[start[0], start[1]] = NEON_GREEN   #Moved this after as well because expanded and path pixels kept overwriting.
    pixel_access[end[0], end[1]] = NEON_GREEN
    # display and (maybe) save results
    im.show()
    if (save_file != "do_not_save.png"):
        im.save(save_file)

    im.close()

if __name__ == "__main__":
    # Throw Errors && Such
    # global difficulty, start, end
    # assert sys.version_info[0] == 2  # require python 2 (instead of python 3)
    # assert len(sys.argv) == 2, "Incorrect Number of arguments"  # require difficulty input

    # Parse input arguments
    function_name = str(sys.argv[0])
    difficulty = str(sys.argv[1])
    print("running " + function_name + " with " + difficulty + " difficulty.")

    # Hard code start and end positions of search for each difficulty level
    if difficulty == "trivial.gif":
        start = (8, 1)
        end = (20, 1)
    elif difficulty == "medium.gif":
        start = (8, 201)
        end = (110, 1)
    elif difficulty == "super_hard.gif": #This said hard.gif, but there was no hard.gif, so I changed it so super_hard
        start = (10, 1)
        end = (401, 220)
    elif difficulty == "very_hard.gif":
        start = (1, 324)
        end = (580, 1)
    elif difficulty == "my_maze.gif":
        start = (0, 0)
        end = (500, 205)
    elif difficulty == "my_maze2.gif":
        start = (0, 0)
        end = (599, 350)
    else:
        assert False, "Incorrect difficulty level provided"
    G = 1000000000000000000
    E = 1000000000000000000
    #open.put((start, 0))
    came_from[start] = None
    cost_so_far[start] = 0
    # Perform search on given image
    im = Image.open(f'maps/' + difficulty)
    im = im.convert('1')
    search(im.load())
    visualize_search(f"{difficulty[:-4]}Solved.png")
    