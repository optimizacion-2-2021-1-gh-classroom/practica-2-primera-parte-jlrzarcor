import numpy as np
import pandas as pd

class HillClimbing:

    def __init__(self, points, random_solution, num):
        pass

    def distance_matrix(self, points):
        """
        calculate the distance among each suggest solution points
        input:
            points: array containig the points to be visited
        outputs:
                matrix: nxn array with distances among solution points
                :param self:
        """
        coordinates = points
        matrix = []
        for i in range(len(coordinates)):
            for j in range(len(coordinates)):
                p = np.linalg.norm(coordinates[i] - coordinates[j])
                matrix.append(p)
        return np.reshape(matrix, (len(coordinates), len(coordinates)))

    def random_solution(number_points):
        """
        create a random solution with the places to be visited
            input:
                points: array with the places for visiting
            output:
                array: input randomly rearrange
        """
        points_order = list(range(0, number_points))
        temp_solution = []
        # noinspection PyTypeChecker
        for i in range(number_points):
            random_point = np.random.choice(points_order)
            temp_solution.append(random_point)
            points_order.remove(random_point)
        temp_solution.append(temp_solution[0])
        return temp_solution


    def calculate_distance(points, random_solution):
        """
        returns the distance associated with a solution
        input:
            points:
        """
        matrix = distance_matrix(points)
        distance = 0
        for i in range(len(random_solution)):
            distance += matrix[random_solution[i]][random_solution[i - 1]]
        return distance


    def other_solutionts(first_solution, number_points, num_solution):
        pos_sol = []
        pos_sol.append(first_solution)
        for i in range(num_solution - 1):
            temp_sol = random_solution(number_points - 1)
        
            if temp_sol not in pos_sol:
                pos_sol.append(temp_sol)
    
        return pos_sol


    def best_solution(points, num_solution):
        best_sol = random_solution(len(points))
        distance = calculate_distance(points, best_sol)
        best_distance = distance
        dist = []
        solutions = other_solutionts(best_sol, len(best_sol), num_solution)
        for pos_sol in solutions:
            pos_dist = calculate_distance(points, pos_sol)
            if best_distance > pos_dist:
                best_distance = pos_dist
                best_sol = pos_sol
        return best_distance, best_sol

