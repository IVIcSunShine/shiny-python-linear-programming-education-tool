#from server import target_functions_list

def function_as_text(list):
    if len(list) == 7:
        return f"({list[0]}) ({str(list[1])}) * x1 + ({str(list[3])}) * x2 {str(list[5])} {str(list[6])}"
    elif len(list) == 6:
        return f"{list[0]} = ({str(list[1])}) * x1 + ({str(list[3])}) * x2 | {str(list[5])}"
    else:
        return "Function not found"

#def find_function_by_dict_entry(dict_entry):
  #  ordnungszahl_liste = 0
 #   for function in target_functions_list:
  #      if function[0] == dict_entry:
  #          return ordnungszahl_liste
  #      ordnungszahl_liste += 1



#def update_function(self, name = "", x1 = "", attribute_1 = "", x2 = "", attribute_2 = ""):
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

#def update_target_function(self, name = "", x1 = "", attribute_1 = "", x2 = "", attribute_2 = "", min_max = ""):
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


#def delete_function(self):
#    function_list.remove(self)
#    del self


#def move_target_function_to_front():

#    for function in Functions.function_list:
 #       if isinstance(Functions.function_list[0], TargetFunctions): #ACHTUNG VLLT EHER MIT TYPE!!!!
 #           break
 #       if isinstance(function, TargetFunctions):
 #           Functions.function_list.remove(function)
 #           Functions.function_list.append(Functions.function_list[0])
 #           Functions.function_list[0] = function
 #           break


#def summarize_functions_text():
#    summarized_text = ""
#    for function in Functions.function_list:

#    summarized_text += "<br>" + function.as_text() + "<br>"
 #   return ui.HTML(summarized_text)