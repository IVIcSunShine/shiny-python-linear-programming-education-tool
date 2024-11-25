from scipy.optimize import milp, LinearConstraint
import numpy as np
import subprocess
import re


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


def solve_sensitivity_analysis(lp_solve_dateipfad, saved_lp_problem_dateipfad, parameter = None):

    result = subprocess.run(
        [lp_solve_dateipfad, parameter, saved_lp_problem_dateipfad],
        capture_output=True,
        text=True
    )
    #print(result.stdout)
    return result



def ausschöpfen_nebenbedingung_und_slack(solved_lp_problem):
    lines_list = solved_lp_problem.splitlines()

    constraint_b_list = []
    for entry in lines_list:
        if entry.startswith("R"):
            #constraint_b_list.append(re.search(r"(\d+(\.\d+)?)\s*$", entry))
            # Suche nach der Zahl am Ende der Zeile
            match = re.search(r"(\d+(\.\d+)?)\s*$", entry)
            # Füge das gefundene Ergebnis (den Zahlwert) der Liste hinzu
            constraint_b_list.append(float(match.group(1)) if '.' in match.group(1) else int(match.group(1)))
        elif entry.startswith("Type"):
            break

    actual_values_constraints = []
    beachten = False
    for entry in lines_list:
        if entry.startswith("Actual values of the constraints"):
            beachten = True
        if beachten == True:
            if entry.startswith("R"):
                match = re.search(r"(\d+(\.\d+)?)\s*$", entry)
                actual_values_constraints.append(float(match.group(1)) if '.' in match.group(1) else int(match.group(1)))
        if entry.startswith("Objective function limits"):
            break

    slack = []
    constraint_eigenschaft = []
    for counter in range(0, len(actual_values_constraints)):
        slack.append(constraint_b_list[counter] - actual_values_constraints[counter])
        if (constraint_b_list[counter] - actual_values_constraints[counter]) == 0:
            constraint_eigenschaft.append("einschränkend")
        else:
            constraint_eigenschaft.append("nicht einschränkend")



    print("------------")
    print(lines_list)
    print("------------")
    print(constraint_b_list)
    print("------------")
    print(actual_values_constraints)
    print("------------")
    print(slack)
    print("------------")
    print(constraint_eigenschaft)

    return [constraint_b_list, actual_values_constraints, slack, constraint_eigenschaft]




def schattenpreis(solved_lp_problem):
    lines_list = solved_lp_problem.splitlines()

    schattenpreis = []
    beachten = False
    for entry in lines_list:
        if entry.startswith("Dual values with from"):
            beachten = True
        if beachten == True:
            entry_ohne_leerzeichen = entry.strip().split()
            if entry_ohne_leerzeichen[0].startswith("R"):
                schattenpreis.append([entry_ohne_leerzeichen[1], entry_ohne_leerzeichen[2], entry_ohne_leerzeichen[3]])
            if entry_ohne_leerzeichen[0].startswith("x"):
                break

    print(schattenpreis)
    return schattenpreis

def coeff_change(solved_lp_problem):
    lines_list = solved_lp_problem.splitlines()
    print(f"AKTUELLE ZEILENLISTE: {lines_list}")

    objective_func_limits = []
    beachten = False
    for entry in lines_list:
        print(entry)
        if entry.startswith("Objective function limits"):
            beachten = True
        if beachten == True:
            print("AB HIER BEACHTEN TRUE")
            print(entry)
            entry_ohne_leerzeichen = entry.strip().split()
            print(entry_ohne_leerzeichen)
            if len(entry_ohne_leerzeichen) != 0 and entry_ohne_leerzeichen[0].startswith("x"):
                objective_func_limits.append([entry_ohne_leerzeichen[1], entry_ohne_leerzeichen[2], entry_ohne_leerzeichen[3]])
            if len(entry_ohne_leerzeichen) == 0 or entry_ohne_leerzeichen[0].startswith("Dual values with from"):
                break

    print(objective_func_limits)
    return objective_func_limits
