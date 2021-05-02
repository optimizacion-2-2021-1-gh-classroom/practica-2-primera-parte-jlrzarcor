import time 
import numpy as np
import pandas as pd


def len_points(points):
    return points.shape[0]

def distance_matrix(points):
    """
    calculate the distance among each suggest solution points

    input:
        points: array containig the points to be visited
    outputs:
        matrix: nxn array with distances among solution points
    """
    coordinates = points
    matrix = []
    for i in range(len(coordinates)):
        for j in range(len(coordinates)):
            p = np.linalg.norm(coordinates[i] - coordinates[j])
            matrix.append(p)
    return np.reshape(matrix, (len(coordinates), len(coordinates)))

def random_solution(points, initial_point):
    """
    create a random solution with the places to be visited
    input:
        points[array]: coordinates of the places to be visited
        initial_point[integer]: number of the place to be visited first
    output:
        temp_solution[list]: creates random solution
    """
    number_points = len_points(points)
    points_order = list(range(0, number_points))
    points_order.remove(initial_point)
    temp_solution = [initial_point]
    for i in range(number_points-1):
        random_point = np.random.choice(points_order)
        temp_solution.append(random_point)
        points_order.remove(random_point)
    temp_solution.append(temp_solution[0])
    return temp_solution

def calculate_distance(points, random_sol):
    """
    returns the distance associated with a proposed solution
        input:
            points[array]: coordinates of the places to be visited
            random_sol[list]: a random route solution
        output:
            distance[float]: the distance cover by the proposed random solution
    """
    matrix = distance_matrix(points)
    distance = 0
    for i in range(len(random_sol)):
        distance += matrix[random_sol[i]][random_sol[i - 1]]
    return distance


def other_solution(points, pos_sol, initial_point):
    """
    creates route solutions not visited before
        input:
            points[array]: coordinates of the places to be visited
            pos_sol[list]: list of posible solution routes
            initial_point[integer]: number of the place to be visited first
        output:
            temp_sol[list]: a new route solution for visiting  
    """
    temp_sol = random_solution(points, initial_point)

    if temp_sol in pos_sol:
        temp_sol = other_solution(points, pos_sol, initial_point)
    else:
        temp_sol        
    return temp_sol


def best_solution(points, initial_point = 0, tolerance=1e-7):
    """
    finds an optimal solution for the TSP problem using hill climbing algorithm
        input:
            points: coordinates of the places to be visited 
            initial_point[integer]: number of the place to be visited first
            tolerance[float]: value that indicates the solution is not improving
        outputs:
            bst_distance[float]: distance of the best route 
            best_sol[list]: order the places to be visted in the optimal solution
            pos_sol[list]: list of the routes that were tested    
    """
    start_time = time.time()
    best_sol = random_solution(points, initial_point)
    best_distance = calculate_distance(points, best_sol)
    pos_sol = [best_sol]
    solution = other_solution(points, pos_sol, initial_point)
    pos_sol.append(solution)
    distance  = calculate_distance(points, solution)
    while abs(distance - best_distance) > tolerance:
        if best_distance > distance:
            best_distance = distance
            best_sol = solution
        solution = other_solution(points, pos_sol, initial_point)
        pos_sol.append(solution)
        distance  = calculate_distance(points, solution)
        
    return best_distance, best_sol, pos_sol
