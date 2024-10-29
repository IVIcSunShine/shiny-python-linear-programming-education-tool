


    def attributes(self):
        return [self.name, self.x1, self.attribute_1, self.x2, self.attribute_2]










    def attributes(self):
        return super().attributes().append(self.min_max)












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