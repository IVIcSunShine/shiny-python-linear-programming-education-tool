import math


def function_as_text(list):
    if len(list) == 7:
        return f"{list[0]} ({str(list[1])}) * x1 + ({str(list[3])}) * x2 {str(list[5])} {str(list[6])}"
    elif len(list) == 6:
        return f"{list[0]} = ({str(list[1])}) * x1 + ({str(list[3])}) * x2 | {str(list[5])}"
    else:
        return "Function not found"


def calculate_highest_xlim_ylim(xlim_list, ylim_list):
    highest_x1 = 0
    highest_x2 = 0
    for x1 in xlim_list:
        if x1[0] > highest_x1:
            highest_x1 = x1[0]
    for x2 in ylim_list:
        if x2[0] > highest_x2:
            highest_x2 = x2[0]
    return [highest_x1, highest_x2]


def calculate_cutting_points_x1_x2_axis(function, xlim=None, ylim=None):
    if len(function) == 7:
        intersection_x1 = (function[6] / function[1])
        intersection_x2 = (function[6] / function[3])
        return [intersection_x1, intersection_x2]
    if len(function) == 6:

        ylim_lower_border = None
        ylim_upper_border = None

        if len(ylim) == 0:
            ylim_lower_border = 1
            ylim_upper_border = 2
        elif len(ylim) == 1:
            ylim_lower_border = 1
            ylim_upper_border = ylim[0][0]
        elif len(ylim) >= 2:

            ylim_lower_border_sorted = []
            for entry in ylim:
                ylim_lower_border_sorted.append(entry[0])

            ylim_lower_border = min(ylim_lower_border_sorted)
            ylim_upper_border = max(ylim_lower_border_sorted)

        selected_ylim = None
        if function[5] == "max":
            selected_ylim = (math.ceil(ylim_lower_border * 0.85 * 2) / 2)
        if function[5] == "min":
            selected_ylim = (math.ceil(ylim_upper_border * 1.15 * 2) / 2)

        obj_func_solution = function[3] * selected_ylim

        intersection_x1_axis = (obj_func_solution / function[1])

        return [intersection_x1_axis, selected_ylim]


def y_result_to_linear_equation(intersection_x1_axis, intersection_x2_axis, x_value):
    m = (0 - intersection_x2_axis) / (intersection_x1_axis - 0)

    y_solution = m * x_value + intersection_x2_axis
    return y_solution


def generate_lp_file(obj_func, constraints, type_of_problem, memory_path):
    with open(memory_path, "w") as file:
        file.write(f"{obj_func[5]}: {obj_func[1]} x1 + {obj_func[3]} x2;\n")
        for constraint in constraints:
            symbol = None
            if constraint[5] == "≤":
                symbol = "<="
            elif constraint[5] == "=":
                symbol = "="
            elif constraint[5] == "≥":
                symbol = ">="
            file.write(f"{constraint[1]} x1 + {constraint[3]} x2 {symbol} {constraint[6]};\n")
        if type_of_problem == "LP":
            file.write("x1 >= 0;\n")
            file.write("x2 >= 0;")
        elif type_of_problem == "ILP":
            file.write("x1 >= 0;\n")
            file.write("x2 >= 0;\n")
            file.write("int x1, x2;")
        elif type_of_problem == "MILP_x1_int_x2_con":
            file.write("x1 >= 0;\n")
            file.write("x2 >= 0;\n")
            file.write("int x1;")
        elif type_of_problem == "MILP_x1_con_x2_int":
            file.write("x1 >= 0;\n")
            file.write("x2 >= 0;\n")
            file.write("int x2;")
        file.close()
