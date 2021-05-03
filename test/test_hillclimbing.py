import pytest
import numpy as np
import os

os.chdir("../")

import src.Opt_HC_CG.hill as opt

from python_tsp.distances import great_circle_distance_matrix
from python_tsp.exact import solve_tsp_dynamic_programming

sources = np.array([
    [40.73024833, -73.79440675],
    [41.47362495, -73.92783272],
    [41.26591   , -73.21026228],
    [41.3249908 , -73.507788  ]
])
distance_matrix = great_circle_distance_matrix(sources)
permutation, distance = solve_tsp_dynamic_programming(distance_matrix)


def test_distance():
    dist_opt = opt.best_solution(sources)
    assert np.linalg.norm(distance - dist_opt) < 1e-3  
    
