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
    alpha_T1_T2 = radVgrad(((gradVrad(180 * 3600) - np.arctan(t_a)) + np.arcsin(sin_delta_alpha)))
    alpha_2717_T2 = alpha_T1_T2 + grad_r_sek_list(data['beta_2'])
    angel = sek_r_grad((180 * 3600) - (90 * 3600) - grad_r_sek_list(data['beta_1']))
    print(angel)
    alpha_3221_T1 = (radVgrad(np.arcsin(sin_delta_alpha)) + 90 * 3600 +
                     ((180 * 3600) - (90 * 3600) - grad_r_sek_list(data['beta_1'])))

    result_of_calculation = {
        'tanα`_3221_2717': t_a,
        'α`_3221_2717': alpha_stroke,
        'α_3221_2717': alpha_3_2,
        'D_3221_2717': round(D, 4),
        'h1': round(h1, 3),
        'h2': round(h2, 3),
        'sinδα': sin_delta_alpha,
        'δα': sek_r_grad(radVgrad(np.arcsin(sin_delta_alpha))),
        'α_T1_T2': sek_r_grad(alpha_T1_T2),
        'α_2717_T2': sek_r_grad(alpha_2717_T2),
        'α_3221_T1': sek_r_grad(alpha_3221_T1),
        'X_T2': round(data['wall_sign_2']['x'] + data['D2'] * np.cos(gradVrad(alpha_2717_T2)), 3),
        'Y_T2': round(data['wall_sign_2']['y'] + data['D2'] * np.sin(gradVrad(alpha_2717_T2)), 3),
        'X_T1': round(data['wall_sign_1']['x'] + data['D1'] * np.cos(gradVrad(alpha_3221_T1)), 3),
        'Y_T1': round(data['wall_sign_1']['y'] + data['D1'] * np.sin(gradVrad(alpha_3221_T1)), 3),
    }

    return result_of_calculation


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    result = binding_to_a_pair_of_wall_signs(source_data)
    for i in result:
        print('{:15} : {}'.format(i, result[i]))

    print('\n')
    print('Control:')
    print('{:15} : {:.3f}'.format('X_T2', result['X_T1']
                                  + source_data['S_t1_t2'] *
                                  np.cos(gradVrad(grad_r_sek_list(result['α_T1_T2'])))))
    print('{:15} : {:.3f}'.format('Y_T2', result['Y_T1']
                                  + source_data['S_t1_t2'] *
                                  np.sin(gradVrad(grad_r_sek_list(result['α_T1_T2'])))))

