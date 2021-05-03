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
    
    return 6371 * (
        acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2)))

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
    returns the distance associated with a proposed solution
        input:
            points[array]: coordinates of the places to be visited
            random_sol[list]: a random route solution
        output:
            distance[float]: the distance cover by the proposed random solution
    """
    distance = 0
    for i in range(len(random_sol)):
        distance += great_circle(points[random_sol[i]][0], points[random_sol[i]][1], points[random_sol[i-1]][0], points[random_sol[i-1]][1])
    return distance

def getNeighbours(solution):
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

def getBestNeighbour(points, neighbours):
    """
    finds the best neighbour from a list of neighbours
        input:
            points[list]: coordinates of the places to be visited
            neighbours[list]: contains the neighbours of the current solution 
        output:
            bestNeighbour[list]: the nearest neighbiur if the current solution 
            bestRouteLength[float]: the distance cover in the bestNeighbour route  
    """
    bestRouteLength = calculate_distance(points, neighbours[0])
    bestNeighbour = neighbours[0]
    for neighbour in neighbours:
        currentRouteLength = calculate_distance(points, neighbour)
        if currentRouteLength < bestRouteLength:
            bestRouteLength = currentRouteLength
            bestNeighbour = neighbour
    return bestNeighbour, bestRouteLength

    
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
    neighbours = getNeighbours(best_sol)
    bestNeighbour, bestNeighbourRouteLength = getBestNeighbour(points, neighbours)
    #pos_sol = [best_sol]
    #solution = other_solution(points, pos_sol, initial_point)
    #pos_sol.append(solution)
    #distance  = calculate_distance(points, solution)
    while abs(bestNeighbourRouteLength - best_distance) > tolerance:
        if best_distance > bestNeighbourRouteLength:
            best_distance = bestNeighbourRouteLength
            best_sol = bestNeighbour
        #solution = other_solution(points, pos_sol, initial_point)
        #pos_sol.append(solution)
        neighbours = getNeighbours(best_sol)
        bestNeighbour, bestNeighbourRouteLength = getBestNeighbour(points, neighbours)
        
    return best_distance, best_sol, time.time() - start_time