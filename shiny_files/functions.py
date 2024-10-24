
#from server import zfkt

#print(zfkt)

class Functions:
    function_list = []

    def __init__(self, name = "", x1 = "", attribute_1 = "", x2 = "", attribute_2 = ""):
        self.name = name
        self.x1 = x1
        self.attribute_1 = attribute_1
        self.x2 = x2
        self.attribute_2 = attribute_2
        Functions.function_list.append(self)


    def attributes(self):
        return [self.name, self.x1, self.attribute_1, self.x2, self.attribute_2]

    def as_text(self):
        return f"{self.name} = ({self.x1}) * x1 + ({self.x2}) * x2 "

    def update_function(self, name = "", x1 = "", attribute_1 = "", x2 = "", attribute_2 = ""):
        if name != "":
            self.name = name
        if x1 != "":
            self.x1 = x1
        if attribute_1 != "":
            self.attribute_1 = attribute_1
        if x2 != "":
            self.x2 = x2
        if attribute_2 != "":
            self.attribute_2 = attribute_2

    def delete_function(self):
        Functions.function_list.remove(self)
        del self




class TargetFunctions(Functions):
    target_function_list = []

    def __init__(self, name, x1, attribute_1, x2, attribute_2, min_max):
        super().__init__(name, x1, attribute_1, x2, attribute_2)
        self.min_max = min_max
        TargetFunctions.target_function_list.append(self)

    def attributes(self):
        return super().attributes().append(self.min_max)

    def as_text(self):
        return super().as_text() + f" | ({self.min_max})"

    def update_function(self, name = "", x1 = "", attribute_1 = "", x2 = "", attribute_2 = "", min_max = ""):
        super().update_function(name, x1, attribute_1, x2, attribute_2)
        if min_max != "":
            self.min_max = min_max

    def delete_function(self):
        super().delete_function()


def move_target_function_to_front():

    for function in Functions.function_list:
        if isinstance(Functions.function_list[0], TargetFunctions): #ACHTUNG VLLT EHER MIT TYPE!!!!
            break
        if isinstance(function, TargetFunctions):
            Functions.function_list.remove(function)
            Functions.function_list.append(Functions.function_list[0])
            Functions.function_list[0] = function
            break


def summarized_func_text_without_target_function():
    summarized_text = ""

    for function in Functions.function_list:
        if type(function) == type(Functions):
            summarized_text += function.as_text() + " \n"


def target_function_list_choices():
    dic_target_functions = {}
    for target_function in TargetFunctions.target_function_list:
        dic_target_functions[target_function.name] = target_function.name
    return dic_target_functions

#def operand(x2):

 #   if x2[0] == "-":
  #      return "-"
   # elif x2[0] == "+":
    #    return "+"
    #else:
     #   return "+"