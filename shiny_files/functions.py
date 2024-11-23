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


def calculate_schnittpunkte_x1_x2_axis(function, xlim=None, ylim=None):
    if len(function) == 7:
        schnittpunkt_x1 = (function[6] / function[1])
        schnittpunkt_x2 = (function[6] / function[3])
        return [schnittpunkt_x1, schnittpunkt_x2]
    if len(function) == 6:

        #xlim_lower_border = None
        #xlim_upper_border = None
        ylim_lower_border = None
        ylim_upper_border = None

        #if len(xlim) == 0:
          #  xlim_lower_border = 0
          #  xlim_upper_border = 1
        #elif len(xlim) == 1:
         #   xlim_lower_border = 0
         #   xlim_upper_border = xlim[0]
       # elif len(xlim) >= 2:
          #  xlim_lower_border = min(xlim)
         #   xlim_upper_border = max(xlim)

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

        #intervall_xlim = np.arange(xlim_lower_border, xlim_upper_border, 0.1)
        #intervall_ylim = np.arange(ylim_lower_border, ylim_upper_border, 0.1)

        #laenge_intervall_xlim = len(intervall_xlim)
        #laenge_intervall_ylim = len(intervall_ylim)
        selected_ylim = None
        if function[5] == "max":
            selected_ylim = (math.ceil(ylim_lower_border * 0.85 * 2) / 2)
        if function[5] == "min":
            selected_ylim = (math.ceil(ylim_upper_border * 1.15 * 2) / 2)

        #print(selected_ylim)

        # mittlerer_intervall_wert_xlim = (math.ceil(intervall_xlim[(laenge_intervall_xlim // 2)] * 2) / 2)
        #mittlerer_intervall_wert_ylim = (math.ceil(intervall_ylim[(laenge_intervall_ylim // 2)] * 2) / 2)

        zielfunktion_erg = function[3] * selected_ylim

        schnittpunkt_x1_axis = (zielfunktion_erg / function[1])
        #print([schnittpunkt_x1_axis, selected_ylim])

        return [schnittpunkt_x1_axis, selected_ylim]
# def find_function_by_dict_entry(dict_entry):
#  ordnungszahl_liste = 0
#   for function in target_functions_list:
#      if function[0] == dict_entry:
#          return ordnungszahl_liste
#      ordnungszahl_liste += 1


# def update_function(self, name = "", x1 = "", attribute_1 = "", x2 = "", attribute_2 = ""):
#    if name != "":
#        self.name = name
#    if x1 != "":
#        self.x1 = x1
#    if attribute_1 != "":
#        self.attribute_1 = attribute_1
#    if x2 != "":
#        self.x2 = x2
#    if attribute_2 != "":
#        self.attribute_2 = attribute_2

# def update_target_function(self, name = "", x1 = "", attribute_1 = "", x2 = "", attribute_2 = "", min_max = ""):
#    if name != "":
#        self.name = name
#    if x1 != "":
#        self.x1 = x1
#    if attribute_1 != "":
#        self.attribute_1 = attribute_1
#    if x2 != "":
#        self.x2 = x2
#    if attribute_2 != "":
#        self.attribute_2 = attribute_2
#    if min_max != "":
#        self.min_max = min_max


# def delete_function(self):
#    function_list.remove(self)
#    del self


# def move_target_function_to_front():

#    for function in Functions.function_list:
#       if isinstance(Functions.function_list[0], TargetFunctions): #ACHTUNG VLLT EHER MIT TYPE!!!!
#           break
#       if isinstance(function, TargetFunctions):
#           Functions.function_list.remove(function)
#           Functions.function_list.append(Functions.function_list[0])
#           Functions.function_list[0] = function
#           break


# def summarize_functions_text():
#    summarized_text = ""
#    for function in Functions.function_list:

#    summarized_text += "<br>" + function.as_text() + "<br>"
#   return ui.HTML(summarized_text)
def y_ergebnis_an_geradengleichung(schnittpunkt_x1_axis, schnittpunkt_x2_axis, x_value):

    m = (0 - schnittpunkt_x2_axis) / (schnittpunkt_x1_axis - 0)

    y_erg = m * x_value + schnittpunkt_x2_axis
    return y_erg


def generate_lp_file(zielfunktion, nebenbedingungen, problemart, speicherpfad):
    with open(speicherpfad, "w") as file:
        file.write(f"{zielfunktion[5]}: {zielfunktion[1]} x1 + {zielfunktion[3]} x2;\n")
        for nebenbedingung in nebenbedingungen:
            symbol = None
            if nebenbedingung[5] == "≤":
                symbol = "<="
            elif nebenbedingung[5] == "=":
                symbol = "="
            elif nebenbedingung[5] == "≥":
                symbol = ">="
            file.write(f"{nebenbedingung[1]} x1 + {nebenbedingung[3]} x2 {symbol} {nebenbedingung[6]};\n")
        if problemart == "LP":
            file.write("x1 >= 0;\n")
            file.write("x2 >= 0;")
        elif problemart == "ILP":
            file.write("x1 >= 0;\n")
            file.write("x2 >= 0;\n")
            file.write("int x1, x2;")
        elif problemart == "MILP_x1_int_x2_kon":
            file.write("x1 >= 0;\n")
            file.write("x2 >= 0;\n")
            file.write("int x1;")
        elif problemart == "MILP_x1_kon_x2_int":
            file.write("x1 >= 0;\n")
            file.write("x2 >= 0;\n")
            file.write("int x2;")
        file.close()
    print("lp-Format-Datei erfolgreich erstellt")
