from shiny import render, reactive, ui
# import matplotlib.pyplot as plt
from functions import Functions, target_function_list_choices
from shiny_files.functions import TargetFunctions

new_restriction = None
new_target_function = None
target_function_dict = {}


def server(input, output, session):
    global new_restricton
    global new_target_function
    global target_function_dict

    @reactive.effect
    @reactive.event(input.button_zfkt_eingeben)
    def modal1():
        m = ui.modal(
            "Bitte Daten eingeben:",
            ui.row(
                ui.column(6,
                          ui.input_text("zfkt_x1", "x1 eingeben", "x1")),
                ui.column(6, ui.input_select(
                    "zfkt_select_attribute_1",
                    "Zahlenbereich:",
                    {"kon": "kontinuierlich", "int": "ganzzahlig"},
                )),
            ),
            ui.row(
                ui.column(6, ui.input_text("zfkt_x2", "x2 eingeben", "x2")),
                ui.column(6, ui.input_select(
                    "zfkt_select_attribute_2",
                    "Zahlenbereich:",
                    {"kon": "kontinuierlich", "int": "ganzzahlig"},
                )
                          )
            ),
            ui.input_text("zfkt_name", "Name eingeben", "Zielfunktion-Name"),
            ui.input_select(
                "zfkt_select_minmax",
                "Art der Optimierung:",
                {"min": "Minimierung", "max": "Maximierung"},
            ),
            footer=ui.div(
                ui.input_action_button(id="cancel_button", label="Abbrechen"),
                ui.input_action_button(id="submit_button", label="Übermitteln"),
            ),
            title="Zielfunktion",
            easy_close=False,
        )
        ui.modal_show(m)

    @reactive.effect
    @reactive.event(input.action_button_restriktionen_eingeben)
    def modal2():
        m2 = ui.modal(
            "Bitte Daten eingeben:",
            ui.row(
                ui.column(6,
                          ui.input_text("rest_x1", "x1 eingeben", "x1")),
                ui.column(6, ui.input_select(
                    "rest_select_attribute_1",
                    "Zahlenbereich:",
                    {"kon": "kontinuierlich", "int": "ganzzahlig"},
                )),
            ),
            ui.row(
                ui.column(6, ui.input_text("rest_x2", "x2 eingeben", "x2")),
                ui.column(6, ui.input_select(
                    "rest_select_attribute_2",
                    "Zahlenbereich:",
                    {"kon": "kontinuierlich", "int": "ganzzahlig"},
                )
                          )
            ),
            ui.input_text("rest_name", "Name eingeben", "Restriktion-Name"),
            footer=ui.div(
                ui.input_action_button(id="cancel_button_2", label="Abbrechen"),
                ui.input_action_button(id="submit_button_2", label="Übermitteln"),
            ),
            title="Restriktion",
            easy_close=False,
        )
        ui.modal_show(m2)

    @reactive.effect
    @reactive.event(input.cancel_button)
    def close_modal_cancel():
        ui.modal_remove()

    @reactive.effect
    @reactive.event(input.cancel_button_2)
    def close_modal2_cancel():
        ui.modal_remove()

    @reactive.effect
    @reactive.event(input.cancel_button_3)
    def close_modal3_cancel():
        ui.modal_remove()

    @reactive.effect
    @reactive.event(input.submit_button_2)
    def create_restriction():
        global new_restriction
        name = input.rest_name()
        x1 = input.rest_x1()
        attribute_1 = input.rest_select_attribute_1()
        x2 = input.rest_x2()
        attribute_2 = input.rest_select_attribute_2()
        new_restriction = Functions(name, x1, attribute_1, x2, attribute_2)
        ui.update_action_button("action_button_restriktionen_ändernLöschen", disabled=False)
        print(new_restriction.as_text())
        print(Functions.function_list)
        print(Functions.function_list[0].as_text())
        print(new_restriction.attributes())
        # print(new_restriction_list[new_restriction].as_text())
        ui.modal_remove()

    @output
    @render.ui
    def rest_text():
        return rest_text_reactive()

    @reactive.event(input.submit_button_2)
    def rest_text_reactive():
        # return "button gedrückt"
        # if new_restriction.name == "":
        #    return ""
        # else:
        # return new_restriction.as_text()
        summarized_text = ""
        for function in Functions.function_list:
            # if type(function) == type(Functions):
            summarized_text += "<br>" + function.as_text() + "<br>"
        return ui.HTML(summarized_text)

    @reactive.effect
    @reactive.event(input.submit_button)
    def create_target_function():
        global new_target_function
        name = input.zfkt_name()
        x1 = input.zfkt_x1()
        attribute_1 = input.zfkt_select_attribute_1()
        x2 = input.zfkt_x2()
        attribute_2 = input.zfkt_select_attribute_2()
        min_max = input.zfkt_select_minmax()
        new_target_function = TargetFunctions(name, x1, attribute_1, x2, attribute_2, min_max)
        ui.update_action_button("action_button_zielfunktion_ändernLöschen", disabled=False)
        print(new_target_function.as_text())
        print(TargetFunctions.target_function_list)
        print(target_function_list_choices())
        # print(Functions.function_list[0].as_text())
        # print(new_target_function.attributes())
        # print(new_restriction_list[new_restriction].as_text())
        ui.modal_remove()

    @output
    @render.ui
    def zfkt_text():
        return zfkt_text_reactive()


    @reactive.event(input.submit_button)
    def zfkt_text_reactive():
        return TargetFunctions.target_function_list[0].as_text()

    @reactive.effect
    @reactive.event(input.action_button_zielfunktion_ändernLöschen)
    def modal3():
        m3 = ui.modal(
            ui.row(
                ui.column(6, ui.input_select(
                    "select_target_function",
                    "Bitte Zielfunktion wählen:",
                    choices=target_function_dict,
                ), ),
                ui.column(6, ui.input_radio_buttons(
                    "radio_target_function",
                    "Bitte Aktion wählen",
                    {"option_löschen": "löschen", "option_ändern": "ändern"},
                ), ),
            ),
            ui.row(
                ui.column(6, ui.HTML("<b>""x1: ""</b>"), ui.output_text("modul3_x1_text")),
                ui.column(6, ui.HTML("<b>""Antwort""</b>"), ui.input_text("zfkt_x1_update", "x1", "neues x1 eingeben")),
            ),
            ui.row(
                ui.column(6, ui.HTML("<b>""Eigenschaft x1""</b>"), ui.output_text("modul3_eigenschaft_x1_text")),
                ui.column(6, ui.HTML("<b>""Antwort2""</b>"), ui.input_select(
                    "zfkt_select_attribute_1_update",
                    "Zahlenbereich:",
                    {"kon": "kontinuierlich", "int": "ganzzahlig"}
                ))
            ),
            ui.row(
                ui.column(6, ui.HTML("<b>""x2""</b>"), ui.output_text("modul3_x2_text")),
                ui.column(6, ui.HTML("<b>""Antwort3""</b>"), ui.input_text("zfkt_x2_update", "x2", "neues x2 eingeben"))
            ),
            ui.row(
                ui.column(6, ui.HTML("<b>""Eigenschaft x2""</b>"), ui.output_text("modul3_eigenschaft_x2_text")),
                ui.column(6, ui.HTML("<b>""Antwort4""</b>"), ui.input_select(
                    "zfkt_select_attribute_2_update",
                    "Zahlenbereich:",
                    {"kon": "kontinuierlich", "int": "ganzzahlig"}
                ))
            ),
            ui.row(
                ui.column(6, ui.HTML("<b>""min-max""</b>"), ui.output_text("modul3_min_max_text")),
                ui.column(6, ui.HTML("<b>""Antwort5""</b>"), ui.input_select(
                    "zfkt_select_minmax_update",
                    "Art der Optimierung:",
                    {"min": "Minimierung", "max": "Maximierung"}
                ))
            ),
            ui.row(
                ui.column(6, ui.HTML("<b>""Name""</b>"), ui.output_text("modul3_name_text")),
                ui.column(6, ui.HTML("<b>""Antwort6""</b>"),
                          ui.input_text("zfkt_name_update", "Name", "neuen Namen eingeben"))
            ),
            footer=ui.div(
                ui.input_action_button(id="cancel_button_3", label="Abbrechen"),
                ui.input_action_button(id="submit_button_3", label="Übermitteln"),
            ),
            title="Zielfunktion ändern oder löschen",
            easy_close=False,
        )
        ui.modal_show(m3)

    @reactive.effect
    @reactive.event(input.submit_button)
    def update_target_function_choices():
        global target_function_dict
        for target_function in TargetFunctions.target_function_list:
            target_function_dict[target_function.name] = target_function.name
        # target_function_dict = target_function_list_choices()
        print(target_function_dict)
        # ui.update_select("select_target_function", choices=target_function_list_choices())
        ui.update_select("select_target_function", choices=target_function_dict)

    @output
    @render.text
    def modul3_x1_text():
        return update_modul3_x1_text()

    @reactive.event(input.select_target_function)
    def update_modul3_x1_text():
        selected_function_name = input.select_target_function()
        for target_function in TargetFunctions.target_function_list:
            if target_function.name == selected_function_name:
                return f"x1: {target_function.x1}"
        return "Keine passende Zielfunktion gefunden"

    @output
    @render.text
    def modul3_eigenschaft_x1_text():
        return update_modul3_eigenschaft_x1_text()

    @reactive.event(input.select_target_function)
    def update_modul3_eigenschaft_x1_text():
        selected_function_name = input.select_target_function()
        for target_function in TargetFunctions.target_function_list:
            if target_function.name == selected_function_name:
                return f"Eigenschaft x1: {target_function.attribute_1}"
        return "Keine passende Zielfunktion gefunden"

    @output
    @render.text
    def modul3_x2_text():
        return update_modul3_x2_text()

    @reactive.event(input.select_target_function)
    def update_modul3_x2_text():
        selected_function_name = input.select_target_function()
        for target_function in TargetFunctions.target_function_list:
            if target_function.name == selected_function_name:
                return f"x2: {target_function.x2}"
        return "Keine passende Zielfunktion gefunden"

    @output
    @render.text
    def modul3_eigenschaft_x2_text():
        return update_modul3_eigenschaft_x2_text()

    @reactive.event(input.select_target_function)
    def update_modul3_eigenschaft_x2_text():
        selected_function_name = input.select_target_function()
        for target_function in TargetFunctions.target_function_list:
            if target_function.name == selected_function_name:
                return f"Eigenschaft x1: {target_function.attribute_2}"
        return "Keine passende Zielfunktion gefunden"

    @output
    @render.text
    def modul3_min_max_text():
        return update_modul3_min_max_text()

    @reactive.event(input.select_target_function)
    def update_modul3_min_max_text():
        selected_function_name = input.select_target_function()
        for target_function in TargetFunctions.target_function_list:
            if target_function.name == selected_function_name:
                return f"Min or Max: {target_function.min_max}"
        return "Keine passende Zielfunktion gefunden"

    @output
    @render.text
    def modul3_name_text():
        return update_modul3_name_text()

    @reactive.event(input.select_target_function)
    def update_modul3_name_text():
        selected_function_name = input.select_target_function()
        for target_function in TargetFunctions.target_function_list:
            if target_function.name == selected_function_name:
                return f"Name: {target_function.name}"
        return "Keine passende Zielfunktion gefunden"


    @reactive.effect
    @reactive.event(input.submit_button_3)
    def close_modal3_by_uebermitteln():
        print(TargetFunctions.target_function_list[0].as_text())
        print(TargetFunctions.target_function_list[0].attributes())
        new_x1 = None
        new_attribute_1 = None
        new_x2 = None
        new_attribute_2 = None
        new_min_max = None
        new_name = None
        selected_function_name = input.select_target_function()
        for target_function in TargetFunctions.target_function_list:
            if target_function.name == selected_function_name:
                if input.zfkt_x1_update() != target_function.x1:
                    new_x1 = input.zfkt_x1_update()
                elif input.zfkt_x1_update() == target_function.x1:
                    new_x1 = target_function.x1
                if input.zfkt_select_attribute_1_update() != target_function.attribute_1:
                    new_attribute_1 = input.zfkt_select_attribute_1_update()
                elif input.zfkt_select_attribute_1_update() == target_function.attribute_1:
                    new_attribute_1 = target_function.attribute_1
                if input.zfkt_x2_update() != target_function.x2:
                    new_x2 = input.zfkt_x2_update()
                elif input.zfkt_x2_update() == target_function.x2:
                    new_x2 = target_function.x2
                if input.zfkt_select_attribute_2_update() != target_function.attribute_2:
                    new_attribute_2 = input.zfkt_select_attribute_2_update()
                elif input.zfkt_select_attribute_2_update() == target_function.attribute_2:
                    new_attribute_2 = target_function.attribute_2
                if input.zfkt_select_minmax_update() != target_function.min_max:
                    new_min_max = input.zfkt_select_minmax_update()
                elif input.zfkt_select_minmax_update() == target_function.min_max:
                    new_min_max = target_function.min_max
                if input.zfkt_name_update() != target_function.name:
                    new_name = input.zfkt_name_update()
                elif input.zfkt_name_update() == target_function.name:
                    new_name = target_function.name

                target_function.update_function(name = new_name, x1=new_x1, attribute_1=new_attribute_1, x2=new_x2, attribute_2=new_attribute_2, min_max = new_min_max)
                print(target_function.as_text())
                print(target_function.attributes())

       # global new_target_function
       # name = input.zfkt_name()
       # x1 = input.zfkt_x1()
       # attribute_1 = input.zfkt_select_attribute_1()
       # x2 = input.zfkt_x2()
       # attribute_2 = input.zfkt_select_attribute_2()
       # min_max = input.zfkt_select_minmax()
       # new_target_function = TargetFunctions(name, x1, attribute_1, x2, attribute_2, min_max)
       # ui.update_action_button("action_button_zielfunktion_ändernLöschen", disabled=False)
       # print(new_target_function.as_text())
       # print(TargetFunctions.target_function_list)
       # print(target_function_list_choices())
        print(TargetFunctions.target_function_list[0].as_text())
        print(TargetFunctions.target_function_list[0].attributes())


        ui.modal_remove()


  #  @reactive.effect
  #  @reactive.event(input.submit_button_3)
  #  def close_modal3_by_uebermitteln_delete():
  #      if input.radio_target_function() == "option_löschen":
   #         for function in TargetFunctions.target_function_list:
    #            if function.name







    #@reactive.effect
    #@reactive.event(input.submit_button_3)
    #def update_zfkt_text():

        #ui.output_ui("zfkt_text")





    #@reactive.effect
    #@reactive.event(input.radio_target_function)
    #def update_modal3_inputs_disability():
    #    selected_option = input.radio_target_function()

     #   if selected_option == "option_ändern":
       #     ui.update_select("select_target_function", disabled=False)
        #    ui.update_text("zfkt_x1_update", disabled=False)
        #    ui.update_select("zfkt_select_attribute_1_update", disabled=False)
        #    ui.update_text("zfkt_x2_update", disabled=False)
        #    ui.update_select("zfkt_select_attribute_2_update", disabled=False)
        #    ui.update_select("zfkt_select_minmax_update", disabled=False)
        #    ui.update_text("zfkt_name_update", disabled=False)
       # else:
        #    ui.update_select("select_target_function", disabled=True)
         #   ui.update_text("zfkt_x1_update", disabled=True)
          #  ui.update_select("zfkt_select_attribute_1_update", disabled=True)
           # ui.update_text("zfkt_x2_update", disabled=True)
          #  ui.update_select("zfkt_select_attribute_2_update", disabled=True)
          #  ui.update_select("zfkt_select_minmax_update", disabled=True)
          #  ui.update_text("zfkt_name_update", disabled=True)
    # @reactive.effect
    # @reactive.event(input.submit_button)
    # def create_target_function():
    #    name = input.zfkt_name()
    #    x1 = input.zfkt_x1()
    #   attribute_1 = input.zfkt_select_attribute_1()
    #   x2 = input.zfkt_x2()
    #   attribute_2 = input.zfkt_select_attribute_2()
    #   min_max = input.zfkt_select_minmax()

    # current_target_function = TargetFunctions(name, x1, attribute_1, x2, attribute_2, min_max)

    #  ui.modal_remove()

    # @reactive.Calc
    # def zfkt_text():
    #    if current_target_function is None:
    #       return ""  # Leerer Text, wenn keine Zielfunktion definiert ist
    #   else:
    #       return current_target_function.as_text()  # Text der Zielfunktion, wenn definiert

    # @output
    # @render.text
# def zfkt_text():
#     return zfkt_text_reactive()


# @reactive.Calc
# def zfkt_text_reactive():
#     return "hallo"  # return current_target_function.as_text()


# @reactive.Calc
# def reactive_txt():
#    if len(Functions.function_list) != 0:
#       return
#   else:
#       return ""


# @reactive.effect
# @reactive.event(input.submit_button)
# def create_function():
# global zielfunktion_name
# zielfunktion_name = input.zfkt_name()
# zielfunktion_name = TargetFunctions(input.zfkt_name(), input.zfkt_x1(), input.zfkt_select_attribute_1(), input.zfkt_x2(), input.zfkt_select_attribute_2(), input.zfkt_select_minmax())


# @reactive.Calc
# def reactive_txt():
#    if input.zfkt_x1() and input.zfkt_x2():
#        zfkt = [input.zfkt_x1(), input.zfkt_x2()]
#        return f"Z={input.zfkt_x1()}*x1+{input.zfkt_x2()}*x2"
#    else:
#        return ""


# @output
# @render.text
# def zfkt_text():
#     return reactive_txt()


#    @reactive.Effect
#   @reactive.event(input.submit_button_2)
#   def calc_rest_list():
#       global restrictions, ausgabe_rest
#       restrictions.append([input.rest_name(), input.rest_x1(), input.rest_x2()])
#
#       ausgabe_rest = ""
#      for rest_entry in restrictions:
#             ausgabe_rest += f"{rest_entry[0]} = {rest_entry[1]}x1 + {rest_entry[2]}x2 <br>"

#    output.rest_text.set(ausgabe_rest)


# @output
# @render.text
# def rest_text():
#     return ausgabe_rest if ausgabe_rest else ""


# @output
# @render.plot()
# def optimierung_plot():
#     x_values_new = [0, 4]
#      y_values_new = [6, 0]

#      fig, ax = plt.subplots(figsize=(6, 6))
#      ax.plot(x_values_new, y_values_new, label="Linie durch (4,0) und (0,6)")

#      ax.set_xlim(0, 10)
#      ax.set_ylim(0, 10)
#      ax.set_xlabel("x-Achse")
#      ax.set_ylabel("y-Achse")
#      ax.legend()

#      ax.grid(True)
#      return fig
