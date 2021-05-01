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
        points: array with the places for visiting
    output:
        array: input randomly rearrange
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
    returns the distance associated with a solution
    input:
        points:
    """
    matrix = distance_matrix(points)
    distance = 0
    for i in range(len(random_sol)):
        distance += matrix[random_sol[i]][random_sol[i - 1]]
    return distance


def other_solution(points, pos_sol, initial_point):
    temp_sol = random_solution(points, initial_point)

    if temp_sol in pos_sol:
        temp_sol = other_solution(points, pos_sol, initial_point)
    else:
        temp_sol        
    return temp_sol


def best_solution(points, initial_point = 0, tolerance=1e-7):
    start_time = time.time()
    best_sol = random_solution(points, initial_point)
    best_distance = calculate_distance(points, best_sol)
    pos_sol = [best_sol]
    solution = other_solution(points, pos_sol, initial_point)
    pos_sol.append(solution)
    distance  = calculate_distance(points, solution)
    while abs(distance - best_distance) > tolerance:
        print(best_distance, distance)
        if best_distance > distance:
            best_distance = distance
            best_sol = solution
        solution = other_solution(points, pos_sol, initial_point)
        pos_sol.append(solution)
        distance  = calculate_distance(points, solution)
        
    return best_distance, best_sol, pos_sol
