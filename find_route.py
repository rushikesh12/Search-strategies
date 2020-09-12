#Author - Rushikesh Sureshkumar Patel

import sys

# This function is used to read the cost function/heuristic
# It returns a (n , m) list
def read_file(filename):
    list = []
    file = open(filename,"r")
    # This loop creates a list of strings for every line
    for line in file:
        # Here we strip the "\n" from the back and splits the strings based on whitespace
        fields = line.rstrip('\n').split(" ")
        if fields == ['END', 'OF', 'INPUT']:
            return list
        list.append(fields)
    
    return list

# This is the main function for uninformed problem
# The parameters are cost_function(retrived from read_file function), start_start, goal_state 

def uninformed_solution(cost_data,start_state,goal_state):

    # We first create the data structures required
    # closed_set: set, to track the visited states
    # fringe: list of lists, to store the generated nodes
    # memory: list of lists, the main memory where each state is stored for tracing the route afterwards
    # nodes_expanded: list, to track the expanded nodes

    #Then append the first state to memory and fringe
    # fringe and memory elements represent [[state, parent, cumulative_cost, depth]]

    closed_set = set()
    nodes_generated = 1
    fringe = [] 
    memory = []
    nodes_expanded = []
    fringe.append([start_state, None, 0.0, 0])
    memory.append([start_state, None, 0.0, 0])
    state = start_state
    done = False
    while not done:
        if not fringe:
            return False
        # To get the cumulative cost and depth, parent's cumulative cost and depth are stored
        nodes_expanded.append(state)
        parent_cost = float(fringe[0][2])
        prev_depth = fringe[0][3]
        # We remove the first node, before expanding it
        fringe.pop(0)
        # This condition checks if the state has been visited or not
        if str(state) not in closed_set:
            # This loop finds the state and generates the succeeding nodes by looking up the n * 3 cost_data list
            # It first finds the index of the state and using that index to find the index of succeeding node it gets the name of the that state
            # The generated state's list also has the cost and it is added to the parent's cost to make it cumulative
            # the nodes_generated keeps the count of number of nodes generated 
            #  depth is incremented by 1
            for i in cost_data:
                if state in i:
                    nodes_generated+=1
                    a =[cost_data.index(i),i.index(state)]
                    if a[1] == 0:
                        generated_state = cost_data[cost_data.index(i)][1]
                        parent = state
                        depth = prev_depth +1
                        cumulative_cost = parent_cost + float(cost_data[cost_data.index(i)][2])  
                        fringe.append([generated_state, parent, cumulative_cost, depth])
                        memory.append([generated_state, parent, cumulative_cost, depth])
                    elif a[1] == 1:
                        generated_state = cost_data[cost_data.index(i)][0]
                        parent = state
                        depth = prev_depth +1
                        cumulative_cost = parent_cost + float(cost_data[cost_data.index(i)][2])
                        fringe.append([generated_state, parent, cumulative_cost, depth])
                        memory.append([generated_state, parent, cumulative_cost, depth])
        
        # The state is then added to the closed_set
        # Then, the fringe is sorted based on the 3rd element of each list, it being the cumulative cost
        closed_set.add(state)
        fringe = sorted(fringe,key=lambda x: x[2])

        # This condition check if all nodes have been traversed or not
        # If they have been, then the route does not exist and distance is set to "infinity"
        # otherwise next state is the first element of fringe(sorted)
        # and likewise its distance and nodes_expanded are counted and stored

        if not fringe:
            distance = "infinity"
            count_nodes_expanded = len(nodes_expanded)
        else:
            state = str(fringe[0][0])
            distance = fringe[0][2]
            count_nodes_expanded = len(nodes_expanded) + 1

        # This condition check whether the state is goal state or not
        # If it is, then results are displayed using the show_results function and done is set to true, ending the loop
        # Otherwise the loop continues to expand the next state
        if state == goal_state or distance == "infinity":
            show_results(count_nodes_expanded,nodes_generated,distance, memory, start_state, goal_state)
            done = True
        
        

# This function is used to display the results in correct format
# Parameters are the count of nodes expanded & generated, distance, memory(list), start state and destination
def show_results(nodes_expanded,nodes_generated,distance, memory, start, end):
    
    # If distance distance is infinity it is printed as the given format using the parameters
    # Otherwise it prints count of nodes expanded and generated as well distance and call the pathway function to print the route
    if distance == "infinity":
        print("nodes expanded:", nodes_expanded)
        print("nodes generated:", nodes_generated)
        print("distance:", distance)
        print("route:\nnone")
    else:
        print("nodes expanded:", nodes_expanded)
        print("nodes generated:", nodes_generated)
        print("distance:", distance, "km")
        pathway(memory, start, end, distance)
        
# This function prints the route
# Parameters are memory(list), start state, destination and distance

def pathway(memory, start ,end, distance):
    # First we create a empty list route and append the list having the destination and the calculated distance
    # Then we find its parent node using the depth and append it to route and reverse the whole list after the loop executes
    route = []
    for i in memory:
        if end in i and distance in i:
            route.append(i)
    for i in range(route[0][3]-1):
        for j in memory:
            if route:
                if route[-1][1] in j and route[-1][3] - 1 in j:
                    route.append(j)
    route.reverse()
    print("route:")

    # Depending on the number of arguments respective indexes are taken for calculating and printing the distance and names of the states
    # This is beacuse of difference in data structure for uninformed and informed
    if number_of_arguments == 4:
        for i in range(len(route)):
            if i > 0:
                print(route[i][1],"to",route[i][0],",",route[i][2] - route[i-1][2],"km")
            else:
                print(route[i][1],"to",route[i][0],",",route[i][2],"km")
    
    elif number_of_arguments == 5:
        for i in range(len(route)):
            if i > 0:
                print(route[i][1],"to",route[i][0],",",route[i][4] - route[i-1][4],"km")
            else:
                print(route[i][1],"to",route[i][0],",",route[i][4],"km")
    return None

# This is the main function for informed problem
# The parameters are cost_function(retrived from read_file function), start_start, goal_state and heuristic

def informed_solution(cost_data,start_state,goal_state, heuristic):

    # We first create the data structures required, similar to uninformed_solution function
    # fringe and memory elements here represent [[state, parent, cumulative_cost, depth, actual_cost]]
    # The method used is A* 
    # Hence cumulative_cost = g(n) + h(n) = additive cost + heuristic cost of the particular state
    # actual_cost is the additive cost to the state
    # The whole process is similar to uninformed_solution function with the exception of adding h(n) to cumulative cost

    closed_set = set()
    nodes_generated = 1
    fringe = [] 
    memory = []
    nodes_expanded = []
    fringe.append([start_state, None, 0.0, 0, 0.0])
    memory.append([start_state, None, 0.0, 0, 0.0])
    state = start_state
    done = False
    while not done:
        if not fringe:
            return False
        nodes_expanded.append(state)
        parent_cost = float(fringe[0][4])
        prev_depth = fringe[0][3]
        fringe.pop(0)
        if str(state) not in closed_set:
            for i in cost_data:
                if state in i:
                    nodes_generated+=1
                    a =[cost_data.index(i),i.index(state)]
                    if a[1] == 0:
                        generated_state = cost_data[cost_data.index(i)][1]
                        parent = state
                        depth = prev_depth +1
                        # This loop is used to find the h(n) for the respective state using the heuristic from the parameters
                        for j in heuristic:
                            if generated_state in j:
                                heuristic_value = float(heuristic[heuristic.index(j)][1])
                        actual_cost = parent_cost + float(cost_data[cost_data.index(i)][2])
                        cumulative_cost = heuristic_value + parent_cost + float(cost_data[cost_data.index(i)][2])
                        fringe.append([generated_state, parent, cumulative_cost, depth, actual_cost])
                        memory.append([generated_state, parent, cumulative_cost, depth, actual_cost])
                    elif a[1] == 1:
                        generated_state = cost_data[cost_data.index(i)][0]
                        parent = state
                        depth = prev_depth +1
                        for j in heuristic:
                            if str(generated_state) in j:
                                heuristic_value = float(heuristic[heuristic.index(j)][1])
                        actual_cost = parent_cost + float(cost_data[cost_data.index(i)][2])
                        cumulative_cost = heuristic_value + parent_cost + float(cost_data[cost_data.index(i)][2])
                        fringe.append([generated_state, parent, cumulative_cost, depth, actual_cost])
                        memory.append([generated_state, parent, cumulative_cost, depth, actual_cost])
        closed_set.add(state)
        fringe = sorted(fringe,key=lambda x: x[2])
        if not fringe:
            distance = "infinity"
            count_nodes_expanded = len(nodes_expanded)
        else:
            state = str(fringe[0][0])
            distance = fringe[0][2]
            count_nodes_expanded = len(nodes_expanded) + 1

        if state == goal_state or distance == "infinity":
            show_results(count_nodes_expanded,nodes_generated,distance, memory, start_state, goal_state)
            done = True

# We start by taking arguments from the command line
# Assign local variables
 
arguments = sys.argv
cost_data = read_file(str(arguments[1]))
origin = str(arguments[2])
destination = str(arguments[3])
number_of_arguments = len(arguments)

# Determining whether uninformed or informed based on number of arguments  

if number_of_arguments == 4:

    uninformed_solution(cost_data, origin, destination)

elif number_of_arguments == 5:
    # Heuristic is list of n * 2 shape
    heuristic = read_file(str(arguments[4]))
    informed_solution(cost_data, origin, destination, heuristic)

else:
    print("Wrong Input arguments!\nTry again.")


