from scipy.optimize import milp, LinearConstraint
import numpy as np
import subprocess


def solve_linear_programming_problem(target_function, side_functions, art_of_problem):
    if art_of_problem == "LP" or art_of_problem == "ILP" or art_of_problem == "MILP_x1_int_x2_kon" or art_of_problem == "MILP_x1_kon_x2_int":
        upper_borders_list = []
        lower_borders_list = []

        target_coeff_1 = target_function[1]
        target_coeff_2 = target_function[3]
        if target_function[5] == "max":
            target_coeff_1 = target_coeff_1 * (-1)
            target_coeff_2 = target_coeff_2 * (-1)

        side_functions_coeff_list = []
        for function in side_functions:
            side_functions_coeff_list.append([function[1], function[3]])

            upper_borders_list.append(function[6])
            if function[5] == "≤":
                lower_borders_list.append(-np.inf)
            elif function[5] == "=":
                lower_borders_list.append(function[6])
            elif function[5] == "≥":
                lower_borders_list.append(function[6])
                upper_borders_list[(len(upper_borders_list) - 1)] = np.inf

        target_function_coefficients = np.array([target_coeff_1, target_coeff_2])
        side_function_coefficients = np.array(side_functions_coeff_list)
        all_functions_upper_border = np.array(upper_borders_list)
        all_functions_lower_border = np.array(lower_borders_list)
        problem_constraints = LinearConstraint(side_function_coefficients, all_functions_lower_border,
                                               all_functions_upper_border)

        if art_of_problem == "LP":
            problem_result = milp(target_function_coefficients, constraints=problem_constraints)
        elif art_of_problem == "ILP":
            problem_result = milp(target_function_coefficients, constraints=problem_constraints, integrality=[1,1])
        elif art_of_problem == "MILP_x1_int_x2_kon":
            problem_result = milp(target_function_coefficients, constraints=problem_constraints, integrality=[1,0])
        elif art_of_problem == "MILP_x1_kon_x2_int":
            problem_result = milp(target_function_coefficients, constraints=problem_constraints, integrality=[0,1])

        print(problem_result.message)
        if target_function[5] == "max":
            print(-problem_result.fun)
        elif target_function[5] == "min":
            print(problem_result.fun)
        print(problem_result.x)

        if target_function[5] == "max":
            return [-problem_result.fun, problem_result.x]
        elif target_function[5] == "min":
            return [problem_result.fun, problem_result.x]

    elif art_of_problem == "not defined":
        return "No problem type defined"


def solve_sensitivity_analysis(lp_solve_dateipfad, saved_lp_problem_dateipfad):

    result = subprocess.run(
        [lp_solve_dateipfad, saved_lp_problem_dateipfad],
        capture_output=True,
        text=True
    )
    #print(result.stdout)
    return result