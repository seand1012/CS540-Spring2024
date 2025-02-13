import heapq

moves = [(1, 0), (-1, 0), (0, 1), (0, -1)] # right, left, up, down

def count_inversions(state):
    inversions = 0
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i] != 0 and state[j] != 0 and state[i] > state[j]:
                inversions += 1
    return inversions

def is_solvable(state):
    inversions = count_inversions(state)
    return inversions % 2 == 0
        

def get_manhattan_distance(from_state, to_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: implement this function. This function will not be tested directly by the grader. 

    INPUT: 
        Two states (if second state is omitted then it is assumed that it is the goal state)

    RETURNS:
        A scalar that is the sum of Manhattan distances for all tiles.
    """
    distance = 0

    # for index in range(len(from_state)-1):
    #     number = from_state[index]
    #     if number != 0:
            
    #         tile_index = from_state.index(index)
    #         #tile_index = index
    #         goal_index = to_state.index(index)
    #         tile_coord = (tile_index // 3, tile_index % 3)
    #         goal_coord = (goal_index // 3, goal_index % 3)
    #         distance += (abs(tile_coord[0] - goal_coord[0]) + abs(tile_coord[1] - goal_coord[1]) )
    for index, number in enumerate(from_state):
        if number == 0:  # Skip empty slots
            continue
        tile_coord = divmod(index, 3)  # Convert index to (row, col)
        goal_index = to_state.index(number)  # Find the goal position of the tile
        goal_coord = divmod(goal_index, 3)  # Convert goal index to (row, col)
        # Calculate Manhattan distance for the tile
        distance += abs(tile_coord[0] - goal_coord[0]) + abs(tile_coord[1] - goal_coord[1])
    #print("manny dist:", distance)    
    return distance

def print_succ(state):
    """
    TODO: This is based on get_succ function below, so should implement that function.

    INPUT: 
        A state (list of length 9)

    WHAT IT DOES:
        Prints the list of all the valid successors in the puzzle. 
    """
    succ_states = get_succ(state)

    for succ_state in succ_states:
        print(succ_state, "h={}".format(get_manhattan_distance(succ_state)))


def get_succ(state):
    """
    TODO: implement this function.

    INPUT: 
        A state (list of length 9)

    RETURNS:
        A list of all the valid successors in the puzzle (don't forget to sort the result as done below). 
    """
    index_of_zero = 0
    # for index in range(len(state)):
    #     if state[index] == 0:
    #         index_of_zero = index
    empty_indices = [i for i, tile in enumerate(state) if tile == 0]
    
    succ_states = []
    for empty_index in empty_indices:
        row, col = empty_index // 3, empty_index % 3
        for dr, dc in moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_index = new_row * 3 + new_col
                new_state = state[:]
                new_state[empty_index], new_state[new_index] = new_state[new_index], new_state[empty_index]
                if new_state not in succ_states and new_state != state:
                    succ_states.append(new_state)
   
    return sorted(succ_states)


def solve(state, goal_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: Implement the A* algorithm here.

    INPUT: 
        An initial state (list of length 9)

    WHAT IT SHOULD DO:
        Prints a path of configurations from initial state to goal state along  h values, number of moves, and max queue number in the format specified in the pdf.
    """
    # if not is_solvable(state):
    #     return
    
    pq = []
    state_info_list = []
    closed = []
    init_state = state
    heapq.heappush(pq, (0, state, (0, get_manhattan_distance(state, to_state=goal_state), -1)))
    max_length = len(pq)
    while pq:
        cost, current_state, info = heapq.heappop(pq)
        closed.append((cost, current_state, info))
        parent_index = len(closed)-1
        
        if current_state == goal_state:
            # while parent_index != -1:
                
            #     new_info = (state, info[1], info[0]) # info[1] = h, info[0] = g, info[2] = parent
                
            #     state_info_list.append(new_info)
            #     parent_index = info[2]
            #     _, state, info = closed[parent_index]
            # state_info_list.reverse()
            # break
           
            while parent_index != -1:
                state_info_list.append((state, info[1], info[0]))
                
                #print("my state:",my_moves)
                #print("state info:", state_info_list[len(state_info_list)-1])
                parent_index = info[2]
                if parent_index != -1:
                    _, state, info = closed[parent_index]
                    
            
            state_info_list.reverse()
            holder = state_info_list.pop()
            state_info_list.append((goal_state, holder[1], holder[2]))
            break
        else:
            succ_states = get_succ(current_state)
            for succ in succ_states:
                if succ not in [s for _, s, _ in closed]:
                    g = info[0] + 1
                    h = get_manhattan_distance(succ)
                    priority = g + h
                    heapq.heappush(pq, (priority, succ, (g, h, len(closed) - 1)))
                    #if(len(pq) > max_length):
                    max_length = max(max_length, len(pq))
            
            
           
    # This is a format helper，which is only designed for format purpose.
    # build "state_info_list", for each "state_info" in the list, it contains "current_state", "h" and "move".
    # define and compute max length
    # it can help to avoid any potential format issue.
    for state_info in state_info_list:
        current_state = state_info[0]
        h = state_info[1]
        move = state_info[2]
        print(current_state, "h={}".format(h), "moves: {}".format(move))
    print("Max queue length: {}".format(max_length))

    
if __name__ == "__main__":
    """
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    """
    # print_succ([2,5,1,4,0,6,7,0,3])
    # print()
    
    # print(get_manhattan_distance([2,5,1,4,0,6,7,0,3], [1, 2, 3, 4, 5, 6, 7, 0, 0]))
    # print()

    # solve([2,5,1,4,0,6,7,0,3])
    # print()
#print_succ([2,5,1,4,0,6,7,0,3])
#solve([4,3,0,5,1,6,7,2,0])