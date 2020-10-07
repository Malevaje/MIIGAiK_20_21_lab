# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 14:18:43 2020

@author: Oleg_Chekin
"""
import numpy as np
import math as m
from func_with_angles import *

source_data = {
    'wall_sign_1': {
        'x': 1118.185,
        'y': 693.035,
    },
    'wall_sign_2': {
        'x': 1258.054,
        'y': 686.978,
    },
    'D1': 51.051,
    'D2': 77.730,
    'S_t1_t2': 187.323,
    'beta_1': [79, 19, 8],
    'beta_2': [59, 57, 36],
}


def tan_alpha(data):
    """
    Accepts a dictionary with the source data as input.
    Returns the value of the stroke tangent and the
    distance between marks.
    :param data: dict {source data}
    :return: tangens alpha stroke, distance between mark 1 and 2
    """
    x_1 = data['wall_sign_1']['x']
    y_1 = data['wall_sign_1']['y']
    x_2 = data['wall_sign_2']['x']
    y_2 = data['wall_sign_2']['y']

    tan_a = (y_2 - y_1) / (x_2 - x_1)
    D = np.sqrt((y_2 - y_1) ** 2 + (x_2 - x_1) ** 2)
    return abs(tan_a), D


def alpha(tg):
    """
    Takes the tangent value from the tan_alpha function
    as input. Returns the value of the angle alpha_stroke
    and alpha.
    :param tg: tan_a
    :return: angle alpha_stroke and alpha.
    """
    alpha_stroke = sek_r_grad(radVgrad(np.arctan(tg)))
    alpha_3_2 = sek_r_grad(radVgrad(gradVrad(180 * 3600) - np.arctan(tg)))

    return alpha_stroke, alpha_3_2


def h1_h2_delta(data, D):
    """

    :param data:
    :param D:
    :return:
    """
    h1 = data['D1'] * np.sin(gradVrad(grad_r_sek_list(data['beta_1'])))
    h2 = data['D2'] * np.sin(gradVrad(grad_r_sek_list(data['beta_2'])))
    sin_delta_alpha = (h2-h1) / D

    return h1, h2, sin_delta_alpha


def binding_to_a_pair_of_wall_signs(data):
    t_a, D = tan_alpha(data)
    alpha_stroke, alpha_3_2 = alpha(t_a)
    h1, h2, sin_delta_alpha = h1_h2_delta(data, D)
    result_of_calculation = {
        'tanα`_3221_2717': t_a,
        'α`_3221_2717': alpha_stroke,
        'α_3221_2717': alpha_3_2,
        'D_3221_2717': round(D, 4),
        'h1': round(h1, 3),
        'h2': round(h2, 3),
        'sinδα': sin_delta_alpha,
    }

    return result_of_calculation


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    result = binding_to_a_pair_of_wall_signs(source_data)
    for i in result:
        print('{:15} : {}'.format(i, result[i]))
