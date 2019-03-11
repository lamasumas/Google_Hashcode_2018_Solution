# --------------------------------------------------------
#           PYTHON PROGRAM
# Here is where we are going to define our set of...
# - Imports
# - Global Variables
# - Functions
# ...to achieve the functionality required.
# When executing > python 'this_file'.py in a terminal,
# the Python interpreter will load our program,
# but it will execute nothing yet.
# --------------------------------------------------------

import os
import codecs

# ------------------------------------------
# 1. FUNCTION parse_in
# ------------------------------------------
def parse_in(i_name):
    # 1. We create the output variable
    res = {}

    # 2. We open the file for reading
    my_input_file = codecs.open(i_name, "r", encoding='utf-8')

    # 3. We read the first line of the file
    res["num_rows"], res["num_columns"], res["num_cars"], res["num_rides"], res["bonus"], res["timeline"] = map(int, my_input_file.readline().strip().split())

    # 4. We read the rest of lines of the file

    # 4.1. We use a list of lists of boolean to represent the pizza content
    res["rides"] = []

    # 4.2. We fill each row of the pizza
    for line in my_input_file:
        # 4.2.1. We parse the line
        a, b, c, d, e, f = map(int,line.strip().split())

        # 4.2.2. We append it to rides
        res["rides"].append([a,b,c,d,e,f])

    # 5. We close the file
    my_input_file.close()

    # 6. We return res
    return res

# ------------------------------------------
# 2. FUNCTION parse_out
# ------------------------------------------
def parse_out(o_name, res):
    # 1. We open the file for reading
    my_output_file = codecs.open(o_name, "w", encoding='utf-8')

    # 2. We print the result for each car
    size = len(res["num_rides"])

    for index in range(size):
        # 2.1. We print the number of rides of the car
        my_output_file.write(str(res["num_rides"][index]))

        # 2.2. We get the list of rides the car is involved into
        for r in res["rides"][index]:
            my_output_file.write(" " + str(r))

        # 2.3. We print the end of line
        my_output_file.write("\n")

    # 3. We close the file
    my_output_file.close()

# ------------------------------------------
# 3.1. FUNCTION distance
# ------------------------------------------
def distance(x1, y1, x2, y2):
    # 1. We create the output variable
    res = 0

    # 2. We assign res
    res = abs(x2-x1) + abs(y2-y1)

    # 3. We return res
    return res

# ------------------------------------------
# 3.2. FUNCTION assign_ride
# ------------------------------------------
def assign_ride(ride_info, cars_state, num_cars):
    # 1. We create the output_variable
    res = num_cars

    # 2. We get the starting time
    start_time = ride_info[4]

    # 3. We get the maximum starting time
    max_start_time = ride_info[5] - distance(ride_info[0], ride_info[1], ride_info[2], ride_info[3])

    # 4. We compute when does everybody arrive
    car_arrivals = []
    for car_index in range(num_cars):
        # 4.1. We get the state of the car_index
        car_st = cars_state[car_index]

        # 4.2. We append the estimated time
        arrival_time = car_st[0] + distance(car_st[1], car_st[2], ride_info[0], ride_info[1])
        car_arrivals.append(arrival_time)

    # 5. We apply the hierarchy of preference
    best_value = -1000000
    candidate_index = 0

    # 5.1. We traverse all cars
    while (candidate_index < num_cars):
        # 5.1.1. If the new car is perfect, I take it
        if (car_arrivals[candidate_index] == start_time):
            # 5.1.1.1. We take it
            res = candidate_index

            # 5.1.1.2. We end the loop
            candidate_index = num_cars

        # 5.1.2. If the new car serves the job
        else:
            if (car_arrivals[candidate_index] <= max_start_time):
                # 5.1.2.1. We give the car a value
                new_value = car_arrivals[candidate_index] - start_time

                # 5.1.2.2. If this is the best value so far, we update
                if new_value > best_value:
                    res = candidate_index
                    best_value = new_value

        # 5.1.3. We try the next car
        candidate_index = candidate_index + 1

    # 6. Update the state of the selected car
    if (res < num_cars):
        # 6.1. We pick the current state of the car
        car_st = cars_state[res]

        # 6.2. We update the time
        car_st[0] = car_st[0] + \
                    distance(car_st[1], car_st[2], ride_info[0], ride_info[1]) + \
                    distance(ride_info[0], ride_info[1], ride_info[2], ride_info[3])

        # And, if I had to wait, then I count it as well
        if (best_value < 0):
            car_st[0] = car_st[0] + abs(best_value)

        # 6.3. We update the end position
        car_st[1] = ride_info[2]
        car_st[2] = ride_info[3]

    # We return res
    return res

# ------------------------------------------
# 3.3. FUNCTION choose_pivot
# ------------------------------------------
def choose_pivot(content, left_index, right_index, pivot_policy):
    # ---------------------------------
    # Output Variable -> InitialValue
    # ---------------------------------
    res = 0

    # -----------------------------
    # SET OF OPS
    # -----------------------------
    # OP1. Auxiliary variables
    l = left_index
    r = right_index
    m = (right_index + left_index) // 2

    # OP1. We use the pivot_policy to select the right one

    # 1. We make 1 for left_index policy
    if pivot_policy == 1:
        res = l
    else:
        # 2. We make 2 for right_index policy
        if pivot_policy == 2:
            res = r
        else:
            # 3. We make 3 for median_of_three policy
            if pivot_policy == 3:
                #Three indexes: l, m, r. We do the reasoning with the letters but, instead, we must play with content[l], content[m] and content[r]

                # 1. We compute the median of the three numbers
                value = 0

                # Reasoning:
                # a < b --> 1
                # a < c --> 2
                # b < c --> 4

                if content[l] < content[m]:
                    value = value + 1

                if content[l] < content[r]:
                    value = value + 2

                if content[m] < content[r]:
                    value = value + 4

                # 6 Scenarios:
                # a < b < c --> 1 + 2 + 4 = 7
                # c < b < a --> 0 + 0 + 0 = 0

                # a < c < b --> 2 + 1 + 0 = 3
                # b < c < a --> 4 + 0 + 0 = 4

                # b < a < c --> 4 + 0 + 2 = 6
                # c < a < b --> 0 + 0 + 1 = 1

                if (value == 7) or (value == 0):
                    res = m

                if (value == 3) or (value == 4):
                    res = r

                if (value == 6) or (value == 1):
                    res = l

    # ---------------------------------
    # Output Variable -> FinalValue
    # ---------------------------------
    return res

# ------------------------------------------
# 3.4. FUNCTION partition_arount_pivot
# ------------------------------------------
def partition_arount_pivot(content, indexes, left_index, right_index):
    # ---------------------------------
    # Output Variable -> InitialValue
    # ---------------------------------
    res = 0

    # -----------------------------
    # SET OF OPS
    # -----------------------------
    # OP1. Auxiliary variables
    p = content[left_index]
    res = left_index + 1
    j = left_index + 1

    # OP1. We partition the list
    while j <= right_index:
        # 1.1. If the new position we are checking is to be in the smaller set
        if content[j] < p:
            # 1.1.1. We place it there
            aux = content[res]
            content[res] = content[j]
            content[j] = aux

            aux = indexes[res]
            indexes[res] = indexes[j]
            indexes[j] = aux

            # 1.2. We increase the value of res
            res = res + 1

        # 1.2. We adjust the j
        j = j + 1

    # OP2. We swap the first position with the pivot one
    aux = content[left_index]
    content[left_index] = content[res-1]
    content[res-1] = aux

    aux = indexes[left_index]
    indexes[left_index] = indexes[res-1]
    indexes[res-1] = aux

    # ---------------------------------
    # Output Variable -> FinalValue
    # ---------------------------------
    return res

# ------------------------------------------
# 3.5. FUNCTION quick_sort_count_comparissons
# ------------------------------------------
def quick_sort_count_comparissons(content, indexes, left_index, right_index, pivot_policy):
    # ---------------------------------
    # Output Variable -> InitialValue
    # ---------------------------------
    res_comparisons = 0

    # -----------------------------
    # SET OF OPS
    # -----------------------------

    # -----------------------------
    # OP1. SCENARIO IDENTIFICATION
    # -----------------------------
    length = (right_index - left_index) + 1

    scenario = 0

    # Case 1: Base Case. List has 0 or 1 elements
    if length <= 1:
        scenario = 1
    # Case 2: Recursive Case. List has more than 1 element
    else:
        scenario = 2

    # -----------------------------
    # OP2. SCENARIO IMPLEMENTATION
    # -----------------------------
    # Case 1: Base Case. We do nothing
    if scenario == 1:
        res_comparisons = 0

    # Case 2: Recursive Case. List has more than 1 element
    else:
        # 1. We choose a pivot according to the policy and place it in the first position of content
        pivot_index = choose_pivot(content, left_index, right_index, pivot_policy)

        aux = content[left_index]
        content[left_index] = content[pivot_index]
        content[pivot_index] = aux

        aux = indexes[left_index]
        indexes[left_index] = indexes[pivot_index]
        indexes[pivot_index] = aux

        # 2. We partition content around the selected pivot
        pivot_fp = partition_arount_pivot(content, indexes, left_index, right_index)

        # 3. We recursively solve the two subproblems
        res_1 = quick_sort_count_comparissons(content, indexes, left_index, pivot_fp - 2, pivot_policy)
        res_2 = quick_sort_count_comparissons(content, indexes, pivot_fp, right_index, pivot_policy)

        # 4. We merge the results: Comparisons of the current call + comparissons of sub-problems 1 and 2.
        res_comparisons = (right_index - left_index) + res_1 + res_2

    # ---------------------------------
    # Output Variable -> FinalValue
    # ---------------------------------
    return res_comparisons

# ------------------------------------------
# 3. FUNCTION strategy
# ------------------------------------------
def strategy(input_info):
    # 1. We create the output variable
    res = {}
    res["num_rides"] = []
    for c in range(input_info["num_cars"] + 1):
        res["num_rides"].append(0)

    res["rides"] = []
    for c in range(input_info["num_cars"] + 1):
        res["rides"].append([])

    # 2. Extra Info: Current state of the cars
    cars_state = []
    for c in range(input_info["num_cars"]):
        cars_state.append([0, 0, 0])

    # 3. Extra Info: The length of each ride
    rides_length = []
    for ride_index in range(input_info["num_rides"]):
        # 3.1. We get the ride info
        ride_info = input_info["rides"][ride_index]

        # 3.2. We append the length of the ride
        rides_length.append(distance(ride_info[0], ride_info[1], ride_info[2], ride_info[3]))

    # 4. We sort the rides by the length of their indexes
    rides_length_by_indexes = []
    for j in range(input_info["num_rides"]):
        rides_length_by_indexes.append(j)

    copy_rides_length = rides_length[:]
    swaps = quick_sort_count_comparissons(copy_rides_length, rides_length_by_indexes, 0, len(rides_length)-1, 1)

    # 4. We assign the rides by decreasing length
    for ride_index in reversed(range(input_info["num_rides"])):
        # 4.1. We get the information of the ride
        ride_info = input_info["rides"][rides_length_by_indexes[ride_index]]

        # 4.2. We assign the ride to a car
        car_index = assign_ride(ride_info,
                                cars_state,
                                input_info["num_cars"])

        # 4.3. We update the solution
        res["num_rides"][car_index] = res["num_rides"][car_index] + 1
        res["rides"][car_index].append(ride_index)

    # 5. We assign all uncomplete rides from the fake car to the car 0
    incomplete_rides = res["rides"][input_info["num_cars"]]

    for ride in incomplete_rides:
        # 5.1. We assign it to the car 0
        res["num_rides"][0] = res["num_rides"][0] + 1
        res["rides"][0].append(ride)

    # 6. We delete the fake car
    del res["num_rides"][input_info["num_cars"]]
    del res["rides"][input_info["num_cars"]]

    # 7. We return res
    return res

# ------------------------------------------
# 4. FUNCTION solve_instance
# ------------------------------------------
def solve_instance(i_name, o_name):
    # 1. We do the parseIn from the input file
    input_info = parse_in(i_name)

    # 2. We do the strategy to solve the problem
    output_info = strategy(input_info)

    # 3. We do the parse out to the output file
    parse_out(o_name, output_info)

#------------------------------------------
# FUNCTION 5.1. get_parent_directory
#------------------------------------------
def get_parent_directory(d):
    # 1. We create the output variable
    res = ""

    # 2. We reverse the string representing the path
    rev = d[::-1]

    # 3. We look for the '\\' character representing the parent folder
    if "\\" in rev:
        # 3.1. If there is, we take all the name of the directory until the last '\\', which turns to be the first one when the
        # folder string name has been reversed.
        i = rev.index("\\")
        sub_rev = rev[(i+1):len(rev)]

        # 3.2. We reverse the parent folder again so as to make the string going forward once again
        res = sub_rev[::-1]
    # 4. If there is no parent directory, we just return d
    else:
        res = d
        print("No posible to go one directory up")

    # 5. We return the output variable
    return res

# ------------------------------------------
# 5. FUNCTION solve_benchmark
# ------------------------------------------
def solve_benchmark():
    # 1. Get the current directory
    c_dir = os.getcwd()

    # 2. Get the instances directory
    i_dir = get_parent_directory(c_dir) + "\\2. Instances"

    # 3. Get the list of instances
    instances = os.listdir(i_dir)

    # 4. We remove their extension
    for index in range(len(instances)):
        name = instances[index]
        name = name[:-3]
        instances[index] = name

    # 5. Get the solution directory
    s_dir = get_parent_directory(c_dir) + "\\4. Solutions"

    # 6. We solve the benchmark
    for name in instances:
        # 6.1. Get the full name of the input file
        i_name = i_dir + "\\" + name + ".in"
        o_name = s_dir + "\\" + name + ".out"

        # 6.2. We solve the instance
        solve_instance(i_name, o_name)

# ---------------------------------------------------------------
#           PYTHON EXECUTION
# This is the main entry point to the execution of our program.
# It provides a call to the 'main function' defined in our
# Python program, making the Python interpreter to trigger
# its execution.
# ---------------------------------------------------------------
if __name__ == '__main__':
    # 1. We set a variable for debug
    debug = True

    # 2. If we are debugging we solve the example instance
    if debug == True:
        i_name = "..//2. Instances//a_example.in"
        o_name = "..//4. Solutions//a_example.out"
        solve_instance(i_name, o_name)
    # 3. If we are ok, we solve the entire benchmark
    else:
        solve_benchmark()


