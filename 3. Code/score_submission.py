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
def parse_in(i_name, s_name):
    # 1. We create the output variable
    res = {}

    # 2. We open the instance file for reading
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

    # 6. We open the solution file for reading
    my_input_file = codecs.open(s_name, "r", encoding='utf-8')

    # 7. We fill each car journey
    res["car_jouneys"] = []

    for line in my_input_file:
        # 7.1. We parse the line
        journeys = line.split()

        # 7.2. We turn these values into integers
        i_journeys = []
        for e in journeys:
            i_journeys.append(int(e))

        # 7.2. We append it to car journeys
        res["car_jouneys"].append(i_journeys)

    # 8. We close the file
    my_input_file.close()

    # 9. We return res
    return res

# ------------------------------------------
# 2.1. FUNCTION distance
# ------------------------------------------
def distance(x1, y1, x2, y2):
    # 1. We create the output variable
    res = 0

    # 2. We assign res
    res = abs(x2-x1) + abs(y2-y1)

    # 3. We return res
    return res

# ------------------------------------------
# 2.2. FUNCTION is_valid_solution
# ------------------------------------------
def is_valid_solution(input_info):
    # 1. We create the output variable
    res = True

    # 2. Condition 1. All cars have an output line
    if (len(input_info["car_jouneys"]) == input_info["num_cars"]):
        # 2.1. We compute the rides assigned so far
        assigned_rides = []

        # 2.2. We traverse the journeys of each car
        index = 0

        while (index < input_info["num_cars"]) and (res == True):
            # 2.2.1. We compute the car journey info
            car_info = input_info["car_jouneys"][index]

            # 2.2.2. Condition 2. line[0] states the right amount of rides taken by the car
            if (car_info[0] == (len(car_info) - 1)):
                # 2.2.2.1. We append the rest of elements as rides assigned
                assigned_rides = assigned_rides + car_info[1:]
            # 2.2.3. Otherwise, non-valid solution
            else:
                res = False

            # 2.2.4. We check the next car
            index = index + 1

        # 2.3. If the assigned rides are equal to the number of rides
        if (len(assigned_rides) == input_info["num_rides"]):
            # 2.3.1. We sort the asssigned rides
            assigned_rides.sort()

            # 2.3.2. We traverse them all, to see each ride has been assigned just one
            index = 0

            while (index < input_info["num_rides"]) and (res == True):
                # 2.3.2.1. If the ride was assigned, we continue
                if assigned_rides[index] == index:
                    index = index + 1
                # 2.3.2.2. Otherwise, non-valid solution
                else:
                    res = False

        # 2.4. Otherwise, non-valid solution
        else:
            res = False

    # 3. Otherwise, non-valid solution
    else:
        res = False

    # 4. We return res
    return res

# ------------------------------------------
# 2.3. FUNCTION get_solution_points
# ------------------------------------------
def get_solution_points(input_info):
    # 1. We create the output variable
    res = 0

    # 2. We traverse the cars, computing their points
    for c_index in range(input_info["num_cars"]):
        # 2.1. We initialise the state of the car
        car_state = [0, 0, 0]

        # 2.2. We get the info of the car
        car_rides = input_info["car_jouneys"][c_index][1:]

        # 2.3. We traverse all the rides of the car
        for ride_index in car_rides:
            # 2.3.1. We get the info of the ride we are serving
            ride_info = input_info["rides"][ride_index]

            # 2.3.2. We get the distance between car's current position and departure
            j_1_steps = distance(car_state[1], car_state[2], ride_info[0], ride_info[1])
            departure_time = car_state[0] + j_1_steps

            # 2.3.3. We get the distance between departure and arrival
            j_2_steps = distance(ride_info[0], ride_info[1], ride_info[2], ride_info[3])

            # 2.3.4. Max departure time
            max_departure_time = ride_info[5] - j_2_steps

            # 2.3.5. If departure time is smaller than max departure time, we take the points
            if (departure_time <= max_departure_time):
                res = res + j_2_steps

            # 2.3.6. If departure time is equal to start time, we also take the bonus
            if (departure_time <= ride_info[4]):
                res = res + input_info["bonus"]

            # 2.3.7. We update the car status
            car_state[0] = car_state[0] + j_1_steps + j_2_steps
            if (departure_time < ride_info[4]):
                car_state[0] = car_state[0] + (ride_info[4] - departure_time)

            car_state[1] = ride_info[2]
            car_state[2] = ride_info[3]

    # 3. We return res
    return res

# ------------------------------------------
# 2. FUNCTION evaluate_solution
# ------------------------------------------
def evaluate_solution(input_info):
    # 1. We compute the output variable
    res = ()

    # 2. We compute if the solution is valid
    is_valid = is_valid_solution(input_info)

    # 3. We compute the number of points
    points = 0
    if (is_valid == True):
        points = get_solution_points(input_info)

    # 4. We assign res accordingly
    res = (is_valid, points)

    # 5. We return res
    return res

# ------------------------------------------
# 3. FUNCTION get_instance_score
# ------------------------------------------
def get_instance_score(i_name, s_name):
    # 1. We compute the output variable
    res = ()
    is_valid = True
    points = 0

    # 1. We do the parseIn from the input files
    input_info = parse_in(i_name, s_name)

    # 2. We evaluate the solution
    (is_valid, points) = evaluate_solution(input_info)

    # 3. We assign res accordingly
    res = (is_valid, points)

    # 4. We return res
    return res

#------------------------------------------
# FUNCTION 4.1. get_parent_directory
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
# 4. FUNCTION get_submission_score
# ------------------------------------------
def get_submission_score():
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

    # 6. We open the file for writing the overall submission score
    my_output_file = codecs.open(s_dir + "\\submission_score.txt", "w", encoding='utf-8')

    # 7. We compute the total score
    total_score = 0

    # 8. We solve the benchmark
    for name in instances:
        # 8.1. Get the full name of the input file
        i_name = i_dir + "\\" + name + ".in"
        s_name = s_dir + "\\" + name + ".out"

        # 8.2. We solve the instance
        (is_valid, points) = get_instance_score(i_name, s_name)

        # 8.3. If the instance is valid, we add the result
        if (is_valid == True):
            my_output_file.write("Valid Solution. " + name + ".out" + " = " + str(points) + "\n")
            total_score = total_score + points
        # 8.4. Otherwise, we inform of it and compute 0 points
        else:
            my_output_file.write("Non-Valid Solution. " + name + ".out" + "\n")
    my_output_file.write("------------\nTotal Score = " + str(total_score) + "\n")

    # 9. We close the file
    my_output_file.close()

# ---------------------------------------------------------------
#           PYTHON EXECUTION
# This is the main entry point to the execution of our program.
# It provides a call to the 'main function' defined in our
# Python program, making the Python interpreter to trigger
# its execution.
# ---------------------------------------------------------------
if __name__ == '__main__':
    # 1. We set a variable for debug
    debug = False

    # 2. If we are debugging we solve the example instance
    if debug == True:
        i_name = "C://Users//Ignacio.Castineiras//Desktop//IEEE Society//6. Google Hash Code'18//2. Online Qualification Round//2. Instances//a_example.in"
        s_name = "C://Users//Ignacio.Castineiras//Desktop//IEEE Society//6. Google Hash Code'18//2. Online Qualification Round//4. Solutions//a_example.out"
        (is_valid, points) = get_instance_score(i_name, s_name)
        print(is_valid)
        print(points)
    # 3. If we are ok, we solve the entire benchmark
    else:
        get_submission_score()
