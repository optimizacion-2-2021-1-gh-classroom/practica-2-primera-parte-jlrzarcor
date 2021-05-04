import time 
import numpy as np
import pandas as pd
from math import radians, degrees, sin, cos, asin, acos, sqrt


def great_circle(lon1, lat1, lon2, lat2):
    """
    calculate the great circle distance of the coordinates points
        input:
            [float]the latitudes and longitudes to calculate the
            distance between two cordinates
        output:
            [float] distance between two cordinates
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])    
    
    return 6371000 * (
        acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(abs(lon1 - lon2))))

def len_points(points):
    return points.shape[0]

def distance_matrix(points):
    """
    calculate the distance among each suggest solution point

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
    returns the distance associated with a solution
    input:
        points[array]: coordinates of the places to be visited
        random_sol[list]: contains a random solution proposed
    """
    matrix = distance_matrix(points)
    distance = 0
    for i in range(len(random_sol)):
        distance += matrix[random_sol[i]][random_sol[i - 1]]
    return distance

def get_neighbours(solution):
    """
    generate neighbouring solutions to the current solution
        input:
            solution[list]: current solution
        output:
            neighbours: list containing neighbouring solutions

    """
    neighbours = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            neighbour = solution.copy()
            neighbour[i] = solution[j]
            neighbour[j] = solution[i]
            neighbours.append(neighbour)
    return neighbours

def get_best_neighbour(points, neighbours):
    """
    finds the best neighbour from a list of neighbours
        input:
            points[list]: coordinates of the places to be visited
            neighbours[list]: contains the neighbours of the current solution 
        output:
            best_neighbour[list]: the nearest neighbiur if the current solution 
            best_route_length[float]: the distance cover in the best_neighbour route  
    """
    best_route_length = calculate_distance(points, neighbours[0])
    best_neighbour = neighbours[0]
    for neighbour in neighbours:
        current_route_length = calculate_distance(points, neighbour)
        if current_route_length < best_route_length:
            best_route_length = current_route_length
            best_neighbour = neighbour
    return best_neighbour, best_route_length

    
def best_solution(points, initial_point = 1, tolerance=1e-7):
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
    neighbours = get_neighbours(best_sol)
    best_neighbour, best_neighbour_route_length = get_best_neighbour(points, neighbours)
    #pos_sol = [best_sol]
    #solution = other_solution(points, pos_sol, initial_point)
    #pos_sol.append(solution)
    #distance  = calculate_distance(points, solution)
    while abs(best_neighbour_route_length - best_distance) > tolerance:
        if best_distance > best_neighbour_route_length:
            best_distance = best_neighbour_route_length
            best_sol = best_neighbour
        #solution = other_solution(points, pos_sol, initial_point)
        #pos_sol.append(solution)
        neighbours = get_neighbours(best_sol)
        best_neighbour, best_neighbour_route_length = get_best_neighbour(points, neighbours)
        
    return best_distance, best_sol, time.time() - start_time
