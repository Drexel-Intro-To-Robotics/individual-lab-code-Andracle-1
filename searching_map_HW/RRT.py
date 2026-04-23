import sys
from PIL import Image
import copy
import queue as Queue
import math
import matplotlib.pyplot as plt
import time
import random
import statistics
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
def euclidean(node, goal):
    return math.sqrt((node[0] - goal[0])**2 + (node[1] - goal[1])**2)

def is_collision_free(map_pixels, pt1, pt2, steps=10):
    #Check line between starting point and end point to see if a wall is there
    for i in range(steps + 1):
        # Interpolate between pt1 and pt2
        t = i / steps
        x = int(pt1[0] + t * (pt2[0] - pt1[0]))
        y = int(pt1[1] + t * (pt2[1] - pt1[1]))
        
        try:
            if map_pixels[x, y] == (0,0,0):  #wall
                return False
        except IndexError:
            return False #out of bounds
    return True

def search(map, width, height):
    """
    This function is meant to use the global variables [start, end, path, expanded, frontier] to search through the
    provided map.
    :param map: A '1-concept' PIL PixelAccess object to be searched. (basically a 2d boolean array)
    """
    #start_time = time.time() #Start Timer
    step_size = 1
    path.clear()        #Need to clear since this will be repeated 100 times
    expanded.clear()
    frontier.clear()
    came_from.clear()

    nodes = [start]
    came_from[start] = None #Started at start

    for _ in range(30000): # number of iterations
        #sampling
        if random.random() < 0.06:
            rand_pt = end
        else:
            rand_pt = (random.randint(0, width - 1), random.randint(0, height - 1))
            
        #Find nearby node
        nearest_node = min(nodes, key=lambda n: euclidean(n, rand_pt))
        
       #calculate next node
        theta = math.atan2(rand_pt[1] - nearest_node[1], rand_pt[0] - nearest_node[0])
        new_node = (int(nearest_node[0] + step_size * math.cos(theta)),
                    int(nearest_node[1] + step_size * math.sin(theta)))
                    
        #Check for collisions
        if 0 <= new_node[0] < width and 0 <= new_node[1] < height:
            if is_collision_free(map, nearest_node, new_node):
                if new_node not in came_from:
                    nodes.append(new_node)
                    came_from[new_node] = nearest_node
                
                #tree branches
                    frontier[new_node] = (0, nearest_node)
                
                #check if near goal
                    if euclidean(new_node, end) <= step_size:
                    #check if collision free to goal
                        if is_collision_free(map, new_node, end):
                            if new_node != end:
                                came_from[end] = new_node
                        #remake path again
                            curr = end
                            while curr is not None:
                                path.append(curr)
                                curr = came_from[curr]
                            path.reverse()
                        
                        #number of nodes it took
                            return len(path) 
                        
    return None # Failed to find path within max_iter
            

    
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
    #search(im.load())
    #visualize_search(f"{difficulty[:-4]}RRTSolved.png")

    im = Image.open(f"maps/"+difficulty).convert("RGB")

    width, height = im.size
    pixel_access = im.load()

    costs = []
    for i in range(100): #The 100 attempts
        cost = search(pixel_access, width, height)
        if cost is not None:
            costs.append(cost)
            
    if costs:
        mean_cost = statistics.mean(costs)
        std_dev = statistics.stdev(costs)
        print(f"RRT Statistical Results (100 runs):")
        print(f"Mean Path Cost (nodes): {mean_cost:.2f}")
        print(f"Standard Deviation: {std_dev:.2f}")
        
        # Visualize the last run
        visualize_search(f"{difficulty[:-4]}_RRT_Solved.png")
    else:

        print("RRT failed to find a path in 100 runs.")
    