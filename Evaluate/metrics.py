import numpy as np


def rmse_ate(trajectory_1, trajectory_2):
    alignment_error = trajectory_1 - trajectory_2
    trans_error = np.sqrt(np.sum(np.multiply(alignment_error, alignment_error), 1))
    rmse_ate_value = float(np.sqrt(np.dot(trans_error, trans_error) / len(trans_error)))
    return rmse_ate_value