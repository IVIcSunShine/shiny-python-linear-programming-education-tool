# from scipy.special import functions
#from scipy.constants import value
from shiny import render, reactive, ui
import matplotlib.pyplot as plt
import pandas as pd
#import math
import random
# from functions_old import Functions, target_function_list_choices
# from shiny_files.functions_old import TargetFunctions
from shiny_files.functions import *

# für das Anlegen der OOP-Objekte
# new_restriction = None
# new_target_function = None
# Listen mit OOP-Objekten
# restrictions_object_list = []
# target_functions_object_list = []
# Listen mit Unterlisten aller Funktionen und Atrribute OHNE OOP
#restrictions_list = []
#target_functions_list = []
#all_functions_list = []
# Dictionaries für die Auswahl-Fenster nach User-Eingaben
target_function_dict = {}
nebenbedingung_dict = {}

zielfunktion_reactive_list = reactive.Value([])
nebenbedingung_reactive_list = reactive.value([])


#alle_funktionen_reactive_list = reactive.Value([])

def server(input, output, session):
    #   global new_restricton
    #   global new_target_function
    #   global restrictions_object_list
    #   global target_functions_object_list
    #global restrictions_list
    #global target_functions_list
    #global all_functions_list
    global target_function_dict
    global nebenbedingung_dict

    global nebenbedingung_reactive_list
    global zielfunktion_reactive_list
    #global alle_funktionen_reactive_list


    #########################################################################
    ##############Modal windows - Anfang#####################################
    #########################################################################

    #######################################################
    ##################Modal1 Anfang########################
    #######################################################
    @reactive.effect
    @reactive.event(input.button_zfkt_eingeben)
    def modal1():
        m = ui.modal(
            "Bitte Daten eingeben:",
            ui.row(
                ui.column(6,
                          ui.input_numeric("zfkt_x1", "x1 eingeben", 1, min=None, max=None, step=0.01)),
                ui.column(6, ui.input_select(
                    "zfkt_select_attribute_1",
                    "Zahlenbereich:",
                    {"kon": "kontinuierlich", "int": "ganzzahlig"},
                )),
            ),
            ui.row(
                ui.column(6, ui.input_numeric("zfkt_x2", "x2 eingeben", 1, min=None, max=None, step=0.01)),
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

    #######################################################
    ##################Modal1 Ende##########################
    #######################################################

    #######################################################
    ##################Modal2 Anfang########################
    #######################################################

    @reactive.effect
    @reactive.event(input.action_button_restriktionen_eingeben)
    def modal2():
        m2 = ui.modal(
            "Bitte Daten eingeben:",
            ui.row(
                ui.column(6,
                          ui.input_numeric("rest_x1", "x1 eingeben", 1, min=None, max=None,
                                           step=0.01)),
                ui.column(6, ui.input_select(
                    "rest_select_attribute_1",
                    "Zahlenbereich:",
                    {"kon": "kontinuierlich", "int": "ganzzahlig"},
                )),
            ),
            ui.row(
                ui.column(6, ui.input_numeric("rest_x2", "x2 eingeben", 2, min=None, max=None, step=0.01)),
                ui.column(6, ui.input_select(
                    "rest_select_attribute_2",
                    "Zahlenbereich:",
                    {"kon": "kontinuierlich", "int": "ganzzahlig"},
                )
                          )
            ),
            ui.input_text("rest_name", "Name eingeben", "Restriktion-Name"),

            ui.row(
                ui.column(6,
                          ui.input_select(
                              "select_wertebereich_nebenbedingung",
                              "Select Wertebereich",
                              {"≤": "≤", "≥": "≥",
                               "=": "="},
                          )
                          ),
                ui.column(6,
                          ui.input_numeric("numeric_wertebereich_nebenbedingungen", "Wert", 1.11, min=None, max=None,
                                           step=0.01),
                          )
            ),

            footer=ui.div(
                ui.input_action_button(id="cancel_button_2", label="Abbrechen"),
                ui.input_action_button(id="submit_button_2", label="Übermitteln"),
            ),
            title="Restriktion",
            easy_close=False,
        )
        ui.modal_show(m2)

    #######################################################
    ##################Modal2 Ende##########################
    #######################################################

    #########################################################################
    ##############Modal windows - Ende#######################################
    #########################################################################

    #######################################################
    ##################Cancel Button########################
    #######################################################
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
    @reactive.event(input.cancel_button_4)
    def close_modal4_cancel():
        ui.modal_remove()

    @reactive.effect
    @reactive.event(input.cancel_button_5)
    def close_modal5_cancel():
        ui.modal_remove()

    @reactive.effect
    @reactive.event(input.cancel_button_6)
    def close_modal6_cancel():
        ui.modal_remove()

    #######################################################
    ##################Submit Button########################
    #######################################################

    @reactive.effect
    @reactive.event(input.submit_button_2)
    def create_restriction():
        #global restrictions_list
        #global all_functions_list
        global nebenbedingung_reactive_list
        #global alle_funktionen_reactive_list
        updated_nebenbedingung_reactive_list = nebenbedingung_reactive_list.get().copy()
        if not nebenbedingung_reactive_list.get():
            name = input.rest_name()
        else:
            detected = False
            for function in nebenbedingung_reactive_list.get():
                if function[0] == input.rest_name():
                    detected = True
                    name = input.rest_name() + "_2"
            if detected == False:
                name = input.rest_name()
        x1 = input.rest_x1()
        attribute_1 = input.rest_select_attribute_1()
        x2 = input.rest_x2()
        attribute_2 = input.rest_select_attribute_2()
        wertebereich_symbol = input.select_wertebereich_nebenbedingung()
        wertebereich_wert = input.numeric_wertebereich_nebenbedingungen()
        #nebenbedingung_reactive_list.get().append([name, x1, attribute_1, x2, attribute_2, wertebereich_symbol, wertebereich_wert])
        updated_nebenbedingung_reactive_list.append([name, x1, attribute_1, x2, attribute_2, wertebereich_symbol, wertebereich_wert])
        nebenbedingung_reactive_list.set(updated_nebenbedingung_reactive_list)
        #alle_funktionen_reactive_list.get().append([name, x1, attribute_1, x2, attribute_2, wertebereich_symbol, wertebereich_wert])
        #restrictions_list.append([name, x1, attribute_1, x2, attribute_2, wertebereich_symbol, wertebereich_wert])
        #all_functions_list.append([name, x1, attribute_1, x2, attribute_2, wertebereich_symbol, wertebereich_wert])
        ui.update_action_button("action_button_restriktionen_ändern", disabled=False)
        ui.update_action_button("action_button_restriktionen_löschen", disabled=False)
        print(function_as_text(nebenbedingung_reactive_list.get()[0]))
        print(len(nebenbedingung_reactive_list.get()))
        #print(len(alle_funktionen_reactive_list.get()))
        print(nebenbedingung_reactive_list.get())
        #print(alle_funktionen_reactive_list.get())
        #print(function_as_text(restrictions_list[0]))
        #print(len(restrictions_list))
        #print(len(all_functions_list))
        #print(restrictions_list)
        #print(all_functions_list)
        # print(new_restriction_list[new_restriction].as_text())
        ui.modal_remove()


########################################################################################################################
    ########################################################################################################################
    ########################################################################################################################
    ########################################################################################################################
    @output
    @render.ui
    def rest_text():
        return rest_text_reactive()

    #@reactive.event(nebenbedingung_reactive_list)
    @reactive.Calc
    def rest_text_reactive():
        summarized_text_rest = ""
        for function in nebenbedingung_reactive_list.get():
            summarized_text_rest += "<br>" + function_as_text(function) + "<br>"
        return ui.HTML(summarized_text_rest)

    ########################################################################################################################
    ########################################################################################################################
    ########################################################################################################################
    ########################################################################################################################
    ########################################################################################################################
    ########################################################################################################################
    ########################################################################################################################
    ########################################################################################################################
    @output
    @render.ui
    def zfkt_text():
        return zfkt_text_reactive()

    #@reactive.event(input.submit_button, input.submit_button_4)
    # @reactive.event(zielfunktion_reactive_list)
    @reactive.Calc
    def zfkt_text_reactive():
        summarized_text = ""
        for function in zielfunktion_reactive_list.get():
            summarized_text += "<br>" + function_as_text(function) + "<br>"
        return ui.HTML(summarized_text)
    ########################################################################################################################
    ########################################################################################################################
    ########################################################################################################################
    ########################################################################################################################






    @reactive.effect
    @reactive.event(input.submit_button)
    def create_target_function():
        #global target_functions_list
        #global all_functions_list
        global zielfunktion_reactive_list
        #global alle_funktionen_reactive_list
        updated_zielfunktion_reactive_list = zielfunktion_reactive_list.get().copy()
        if not zielfunktion_reactive_list.get():
            name = input.zfkt_name()
        else:
            detected = False
            for function in zielfunktion_reactive_list.get():
                if function[0] == input.zfkt_name():
                    detected = True
                    name = input.zfkt_name() + "_2"
            if detected == False:
                name = input.zfkt_name()
        #if not target_functions_list:
        #    name = input.zfkt_name()
        #else:
        #    detected = False
        #    for function in target_functions_list:
        #        if function[0] == input.zfkt_name():
        #            detected = True
        #            name = input.zfkt_name() + "_2"
        #    if detected == False:
        #        name = input.zfkt_name()
        x1 = input.zfkt_x1()
        attribute_1 = input.zfkt_select_attribute_1()
        x2 = input.zfkt_x2()
        attribute_2 = input.zfkt_select_attribute_2()
        min_max = input.zfkt_select_minmax()
       # target_functions_list.append([name, x1, attribute_1, x2, attribute_2, min_max])
       # all_functions_list.append([name, x1, attribute_1, x2, attribute_2, min_max])
        #zielfunktion_reactive_list.get().append([name, x1, attribute_1, x2, attribute_2, min_max])
        updated_zielfunktion_reactive_list.append([name, x1, attribute_1, x2, attribute_2, min_max])
        zielfunktion_reactive_list.set(updated_zielfunktion_reactive_list)
        #alle_funktionen_reactive_list.get().append([name, x1, attribute_1, x2, attribute_2, min_max])
        ui.update_action_button("action_button_zielfunktion_ändern", disabled=False)
        ui.update_action_button("action_button_zielfunktion_löschen", disabled=False)
        print(len(zielfunktion_reactive_list.get()))
        #print(len(alle_funktionen_reactive_list.get()))
        print(zielfunktion_reactive_list.get())
       # print(alle_funktionen_reactive_list.get())
        #print(len(target_functions_list))
        #print(len(all_functions_list))
        #print(target_functions_list)
        #print(all_functions_list)
        # print(Functions.function_list[0].as_text())
        # print(new_target_function.attributes())
        # print(new_restriction_list[new_restriction].as_text())
        ui.modal_remove()

 #  @output
 #   @render.ui
 #   def zfkt_text():
 #       return zfkt_text_reactive()
 #   #@reactive.event(input.submit_button, input.submit_button_4)
 #   @reactive.event(input.submit_button, input.cancel_button)
 #   def zfkt_text_reactive():
 #       summarized_text = ""
 #       for function in target_functions_list:
 #           summarized_text += "<br>" + function_as_text(function) + "<br>"
 #       return ui.HTML(summarized_text)





    @reactive.effect
    @reactive.event(input.action_button_zielfunktion_löschen)
    def modal4():
        m4 = ui.modal(
            ui.row(
                ui.column(5, ui.input_select(
                    "select_target_function_for_delete",
                    "Zielfunktion wählen:",
                    choices=target_function_dict,
                ), ),
                ui.column(7, ui.output_text(id="mod4_text"))
            ),
            footer=ui.div(
                ui.input_action_button(id="cancel_button_4", label="Abbrechen"),
                ui.input_action_button(id="submit_button_4", label="löschen"),
            ),
            title="Zielfunktion löschen",
            easy_close=False,
            style="width: 100%;"
        )
        ui.modal_show(m4)

    @output
    @render.text
    def mod4_text():
        return update_mod4_text()

    @reactive.event(input.select_target_function_for_delete)
    def update_mod4_text():
        for function in zielfunktion_reactive_list.get():
            if function[0] == input.select_target_function_for_delete():
                return function_as_text(function)

        # return function_as_text([find_function_by_dict_entry(input.select_target_function_for_delete())])

    @reactive.effect
    @reactive.event(input.submit_button_4)
    def delete_target_function():
        updated_zielfunktion_reactive_list = zielfunktion_reactive_list.get().copy()
        #updated_alle_funktionen_reactive_list = alle_funktionen_reactive_list.get().copy()
        print(target_function_dict)
        print(zielfunktion_reactive_list.get())
       # print(alle_funktionen_reactive_list.get())
        for function in zielfunktion_reactive_list.get():
            if function[0] == input.select_target_function_for_delete():
                updated_zielfunktion_reactive_list.remove(function)
                zielfunktion_reactive_list.set(updated_zielfunktion_reactive_list)
                #zielfunktion_reactive_list.get().remove(function)
                #updated_alle_funktionen_reactive_list.remove(function)
                #alle_funktionen_reactive_list.set(updated_alle_funktionen_reactive_list)
                #alle_funktionen_reactive_list.get().remove(function)
                del target_function_dict[input.select_target_function_for_delete()]
        print(target_function_dict)
        print(zielfunktion_reactive_list.get())
        #print(alle_funktionen_reactive_list.get())
        ui.update_select("select_target_function", choices=target_function_dict)
        if not zielfunktion_reactive_list.get():
            ui.update_action_button("action_button_zielfunktion_ändern", disabled=True)
            ui.update_action_button("action_button_zielfunktion_löschen", disabled=True)
        # ui.update_text("zfkt_text", choices=target_function_dict)
        ui.modal_remove()

    @reactive.effect
    @reactive.event(input.action_button_zielfunktion_ändern)
    def modal3():
        m3 = ui.modal(
            ui.row(
                ui.column(6, ui.input_select(
                    "select_target_function",
                    "Bitte Zielfunktion wählen:",
                    choices=target_function_dict,
                ), ),
                # ui.column(6, ui.input_radio_buttons(
                #    "radio_target_function",
                #    "Bitte Aktion wählen",
                #   {"option_löschen": "löschen", "option_ändern": "ändern"},
                # ), ),
                ui.HTML("<b>""Aktuelle Werte vorausgefüllt. Bei Bedarf ändern. ""</b>"),
                ui.HTML("<br>""<br>")
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""x1: ""</b>")),
 #               ui.column(8, ui.input_numeric("zfkt_x1_update", None, target_functions_list[0][1], min=None, max=None,
  #                                            step=0.01)),
                 ui.column(8, ui.input_numeric("zfkt_x1_update", None, zielfunktion_reactive_list.get()[0][1], min=None, max=None,
                                               step=0.01)),
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""Eigenschaft x1""</b>")),
                ui.column(8, ui.input_select(
                    "zfkt_select_attribute_1_update",
                    None,
                    {"kon": "kontinuierlich", "int": "ganzzahlig"},
                    selected=zielfunktion_reactive_list.get()[0][2]
                ))
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""x2""</b>")),
                ui.column(8, ui.input_numeric("zfkt_x2_update", None, zielfunktion_reactive_list.get()[0][3], min=None, max=None,
                                              step=0.01)),
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""Eigenschaft x2""</b>")),
                ui.column(8, ui.input_select(
                    "zfkt_select_attribute_2_update",
                    None,
                    {"kon": "kontinuierlich", "int": "ganzzahlig"},
                    selected=zielfunktion_reactive_list.get()[0][4]
                ))
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""min-max""</b>")),
                ui.column(8, ui.input_select(
                    "zfkt_select_minmax_update",
                    None,
                    {"min": "Minimierung", "max": "Maximierung"},
                    selected=zielfunktion_reactive_list.get()[0][5]
                ))
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""Name""</b>")),
                ui.column(8,
                          ui.input_text("zfkt_name_update", None, zielfunktion_reactive_list.get()[0][0]))
            ),
            footer=ui.div(
                ui.input_action_button(id="cancel_button_3", label="Abbrechen"),
                ui.input_action_button(id="submit_button_3", label="Übermitteln"),
            ),
            title="Zielfunktion ändern",
            easy_close=False,
            style="width: 100%;"
        )

        ui.modal_show(m3)

    @reactive.effect
    @reactive.event(input.submit_button)
    def update_target_function_choices():
        global target_function_dict
        for target_function in zielfunktion_reactive_list.get():
            target_function_dict[target_function[0]] = target_function[0]
        print(target_function_dict)
        ui.update_select("select_target_function", choices=target_function_dict)

    @reactive.effect
    @reactive.event(input.select_target_function)
    def update_target_function_changing_placeholder():
        selected_function_name = input.select_target_function()
        for target_function in zielfunktion_reactive_list.get():
            if target_function[0] == selected_function_name:
                ui.update_text("zfkt_name_update", value=target_function[0])
                ui.update_numeric("zfkt_x1_update", value=target_function[1])
                ui.update_select("zfkt_select_attribute_1_update", selected=target_function[2])
                ui.update_numeric("zfkt_x2_update", value=target_function[3])
                ui.update_select("zfkt_select_attribute_2_update", selected=target_function[4])
                ui.update_select("zfkt_select_minmax_update", selected=target_function[5])

    @reactive.effect
    @reactive.event(input.submit_button_3)
    def close_modal3_by_uebermitteln():
        selected_function_name = input.select_target_function()
        counter = 0
        for target_function in zielfunktion_reactive_list.get():
            if target_function[0] == selected_function_name:
                updated_zielfunktion_reactive_list = zielfunktion_reactive_list.get().copy()
                print(function_as_text(target_function))
                if input.zfkt_x1_update() != target_function[1]:
                    updated_zielfunktion_reactive_list[counter][1] = input.zfkt_x1_update()
                    zielfunktion_reactive_list.set(updated_zielfunktion_reactive_list)
                    #zielfunktion_reactive_list.get()[counter][1] = input.zfkt_x1_update()
                if input.zfkt_select_attribute_1_update() != target_function[2]:
                    updated_zielfunktion_reactive_list[counter][2] = input.zfkt_select_attribute_1_update()
                    zielfunktion_reactive_list.set(updated_zielfunktion_reactive_list)
                    #zielfunktion_reactive_list.get()[counter][2] = input.zfkt_select_attribute_1_update()
                if input.zfkt_x2_update() != target_function[3]:
                    updated_zielfunktion_reactive_list[counter][3] = input.zfkt_x2_update()
                    zielfunktion_reactive_list.set(updated_zielfunktion_reactive_list)
                    #zielfunktion_reactive_list.get()[counter][3] = input.zfkt_x2_update()
                if input.zfkt_select_attribute_2_update() != target_function[4]:
                    updated_zielfunktion_reactive_list[counter][4] = input.zfkt_select_attribute_2_update()
                    zielfunktion_reactive_list.set(updated_zielfunktion_reactive_list)
                    #zielfunktion_reactive_list.get()[counter][4] = input.zfkt_select_attribute_2_update()
                if input.zfkt_select_minmax_update() != target_function[5]:
                    updated_zielfunktion_reactive_list[counter][5] = input.zfkt_select_minmax_update()
                    zielfunktion_reactive_list.set(updated_zielfunktion_reactive_list)
                    #zielfunktion_reactive_list.get()[counter][5] = input.zfkt_select_minmax_update()
                if input.zfkt_name_update() != target_function[0]:
                    updated_zielfunktion_reactive_list[counter][0] = input.zfkt_name_update()
                    zielfunktion_reactive_list.set(updated_zielfunktion_reactive_list)
                    #zielfunktion_reactive_list.get()[counter][0] = input.zfkt_name_update()
                    print(target_function_dict)
                    target_function_dict[target_function[0]] = input.zfkt_name_update()
                    print(target_function_dict)
                    del target_function_dict[selected_function_name]
                    print(target_function_dict)

                ui.update_select("select_target_function", choices=target_function_dict)

                print(function_as_text(target_function))
                print(zielfunktion_reactive_list.get())
                #print(alle_funktionen_reactive_list.get())
            counter += 1
        ui.modal_remove()

########################################################################################################################
########################################################################################################################
########################################################################################################################

    @reactive.effect
    @reactive.event(input.action_button_restriktionen_löschen)
    def modal6():
        m6 = ui.modal(
            ui.row(
                ui.column(5, ui.input_select(
                    "select_restriction_for_delete",
                    "Restriktion wählen:",
                    choices=nebenbedingung_dict,
                ), ),
                ui.column(7, ui.output_text(id="mod6_text"))
            ),
            footer=ui.div(
                ui.input_action_button(id="cancel_button_6", label="Abbrechen"),
                ui.input_action_button(id="submit_button_6", label="löschen"),
            ),
            title="Restriktion löschen",
            easy_close=False,
            style="width: 100%;"
        )
        ui.modal_show(m6)

    @output
    @render.text
    def mod6_text():
        return update_mod6_text()

    @reactive.event(input.select_restriction_for_delete)
    def update_mod6_text():
        for function in nebenbedingung_reactive_list.get():
            if function[0] == input.select_restriction_for_delete():
                return function_as_text(function)

        # return function_as_text([find_function_by_dict_entry(input.select_target_function_for_delete())])

    @reactive.effect
    @reactive.event(input.submit_button_6)
    def delete_restriction():
        updated_nebenbedingung_reactive_list = nebenbedingung_reactive_list.get().copy()
        #updated_alle_funktionen_reactive_list = alle_funktionen_reactive_list.get().copy()
        print(nebenbedingung_dict)
        print(nebenbedingung_reactive_list.get())
       # print(alle_funktionen_reactive_list.get())
        for function in nebenbedingung_reactive_list.get():
            if function[0] == input.select_restriction_for_delete():
                updated_nebenbedingung_reactive_list.remove(function)
                nebenbedingung_reactive_list.set(updated_nebenbedingung_reactive_list)
                #nebenbedingung_reactive_list.get().remove(function)
              #  updated_alle_funktionen_reactive_list.remove(function)
              #  alle_funktionen_reactive_list.set(updated_alle_funktionen_reactive_list)
                #alle_funktionen_reactive_list.get().remove(function)
                del nebenbedingung_dict[input.select_restriction_for_delete()]
        print(nebenbedingung_dict)
        print(nebenbedingung_reactive_list.get())
       # print(alle_funktionen_reactive_list.get())
        ui.update_selectize("selectize_nebenbedingung", choices=nebenbedingung_dict)
        if not nebenbedingung_reactive_list.get():
            ui.update_action_button("action_button_restriktionen_ändern", disabled=True)
            ui.update_action_button("action_button_restriktionen_löschen", disabled=True)
        # ui.update_text("zfkt_text", choices=target_function_dict)
        ui.modal_remove()

    @reactive.effect
    @reactive.event(input.action_button_restriktionen_ändern)
    def modal5():
        m5 = ui.modal(
            ui.row(
                ui.column(6, ui.input_select(
                    "select_rest_function_mod5",
                    "Bitte Nebenbedingung wählen:",
                    choices=nebenbedingung_dict,
                ), ),
                # ui.column(6, ui.input_radio_buttons(
                #    "radio_target_function",
                #    "Bitte Aktion wählen",
                #   {"option_löschen": "löschen", "option_ändern": "ändern"},
                # ), ),
                ui.HTML("<b>""Aktuelle Werte vorausgefüllt. Bei Bedarf ändern. ""</b>"),
                ui.HTML("<br>""<br>")
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""x1: ""</b>")),
                ui.column(8, ui.input_numeric("rest_x1_update", None, nebenbedingung_reactive_list.get()[0][1], min=None, max=None,
                                              step=0.01)),
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""Eigenschaft x1""</b>")),
                ui.column(8, ui.input_select(
                    "rest_select_attribute_1_update",
                    None,
                    {"kon": "kontinuierlich", "int": "ganzzahlig"},
                    selected=nebenbedingung_reactive_list.get()[0][2]
                ))
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""x2""</b>")),
                ui.column(8, ui.input_numeric("rest_x2_update", None, nebenbedingung_reactive_list.get()[0][3], min=None, max=None,
                                              step=0.01)),
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""Eigenschaft x2""</b>")),
                ui.column(8, ui.input_select(
                    "rest_select_attribute_2_update",
                    None,
                    {"kon": "kontinuierlich", "int": "ganzzahlig"},
                    selected=nebenbedingung_reactive_list.get()[0][4]
                ))
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""Wertebereich""</b>")),
                ui.column(8, ui.input_select(
                    "rest_select_wertebereich_update",
                    None,
                    {"≤": "≤", "≥": "≥",
                               "=": "="},
                    selected=nebenbedingung_reactive_list.get()[0][5]
                ))
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""Wert""</b>")),
                ui.column(8, ui.input_numeric("rest_wert_update", None, nebenbedingung_reactive_list.get()[0][6], min=None, max=None,
                                              step=0.01)),
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""Name""</b>")),
                ui.column(8,
                          ui.input_text("rest_name_update", None, nebenbedingung_reactive_list.get()[0][0]))
            ),
            footer=ui.div(
                ui.input_action_button(id="cancel_button_5", label="Abbrechen"),
                ui.input_action_button(id="submit_button_5", label="Übermitteln"),
            ),
            title="Nebenbedingung ändern",
            easy_close=False,
            style="width: 100%;"
        )

        ui.modal_show(m5)


    @reactive.effect
    @reactive.event(input.submit_button_2)
    def update_restriction_choices():
        global nebenbedingung_dict
        for restriction in nebenbedingung_reactive_list.get():
            nebenbedingung_dict[restriction[0]] = restriction[0]
        print(nebenbedingung_dict)
        ui.update_selectize("selectize_nebenbedingung", choices=nebenbedingung_dict)

    @reactive.effect
    @reactive.event(input.select_rest_function_mod5)
    def update_restriction_changing_placeholder():
        selected_function_name = input.select_rest_function_mod5()
        for restriction in nebenbedingung_reactive_list.get():
            if restriction[0] == selected_function_name:
                ui.update_text("rest_name_update", value=restriction[0])
                ui.update_numeric("rest_x1_update", value=restriction[1])
                ui.update_select("rest_select_attribute_1_update", selected=restriction[2])
                ui.update_numeric("rest_x2_update", value=restriction[3])
                ui.update_select("rest_select_attribute_2_update", selected=restriction[4])
                ui.update_select("rest_select_wertebereich_update", selected=restriction[5])
                ui.update_numeric("rest_wert_update", value=restriction[6])

    @reactive.effect
    @reactive.event(input.submit_button_5)
    def close_modal5_by_uebermitteln():
        selected_function_name = input.select_rest_function_mod5()
        counter = 0
        for restriction in nebenbedingung_reactive_list.get():
            if restriction[0] == selected_function_name:
                updated_nebenbedingung_reactive_list = nebenbedingung_reactive_list.get().copy()
                print(function_as_text(restriction))
                if input.rest_x1_update() != restriction[1]:
                    updated_nebenbedingung_reactive_list[counter][1] = input.rest_x1_update()
                    nebenbedingung_reactive_list.set(updated_nebenbedingung_reactive_list)
                    #nebenbedingung_reactive_list.get()[counter][1] = input.rest_x1_update()
                if input.rest_select_attribute_1_update() != restriction[2]:
                    updated_nebenbedingung_reactive_list[counter][2] = input.rest_select_attribute_1_update()
                    nebenbedingung_reactive_list.set(updated_nebenbedingung_reactive_list)
                    #nebenbedingung_reactive_list.get()[counter][2] = input.rest_select_attribute_1_update()
                if input.rest_x2_update() != restriction[3]:
                    updated_nebenbedingung_reactive_list[counter][3] = input.rest_x2_update()
                    nebenbedingung_reactive_list.set(updated_nebenbedingung_reactive_list)
                    #nebenbedingung_reactive_list.get()[counter][3] = input.rest_x2_update()
                if input.rest_select_attribute_2_update() != restriction[4]:
                    updated_nebenbedingung_reactive_list[counter][4] = input.rest_select_attribute_2_update()
                    nebenbedingung_reactive_list.set(updated_nebenbedingung_reactive_list)
                    #nebenbedingung_reactive_list.get()[counter][4] = input.rest_select_attribute_2_update()
                if input.rest_select_wertebereich_update() != restriction[5]:
                    updated_nebenbedingung_reactive_list[counter][5] = input.rest_select_wertebereich_update()
                    nebenbedingung_reactive_list.set(updated_nebenbedingung_reactive_list)
                    #nebenbedingung_reactive_list.get()[counter][5] = input.rest_select_wertebereich_update()
                if input.rest_wert_update() != restriction[6]:
                    updated_nebenbedingung_reactive_list[counter][6] = input.rest_wert_update()
                    nebenbedingung_reactive_list.set(updated_nebenbedingung_reactive_list)
                    #nebenbedingung_reactive_list.get()[counter][6] = input.rest_wert_update()
                if input.rest_name_update() != restriction[0]:
                    updated_nebenbedingung_reactive_list[counter][0] = input.rest_name_update()
                    nebenbedingung_reactive_list.set(updated_nebenbedingung_reactive_list)
                    #nebenbedingung_reactive_list.get()[counter][0] = input.rest_name_update()
                    print(nebenbedingung_dict)
                    nebenbedingung_dict[restriction[0]] = input.rest_name_update()
                    print(nebenbedingung_dict)
                    del nebenbedingung_dict[selected_function_name]
                    print(nebenbedingung_dict)

                ui.update_select("selectize_nebenbedingung", choices=nebenbedingung_dict)

                print(function_as_text(restriction))
                print(nebenbedingung_reactive_list.get())
            counter += 1
        ui.modal_remove()


    @output
    @render.data_frame
    def zahlenbereiche_df_output():
        return update_zahlenbereiche_df_output()

    @reactive.Calc
    def update_zahlenbereiche_df_output():

        zahlenbereiche_df = pd.DataFrame(columns = ["Name", "Eigenschaft x1", "Eigenschaft x2", "Total"])

        for function in zielfunktion_reactive_list.get():

            eigenschaft_total = None
            if function[2] == "int" and function[4] == "int":
                eigenschaft_total = "integer lp (ILP)"
            elif (function[2] == "int" and function[4] == "kon") or (function[2] == "kon" and function[4] == "int"):
                eigenschaft_total = "mixed integer lp (MILP)"
            elif function[2] == "kon" and function[4] == "kon":
                eigenschaft_total = "lineare Programmierung (LP)"


            zahlenbereiche_df.loc[len(zahlenbereiche_df)] = [function[0], function[2], function[4], eigenschaft_total]
            #zahlenbereiche_df = zahlenbereiche_df.append({"Name": entry[0], "x1": entry[1], "Eigenschaft x1": entry[2], "x2": entry[3], "Eigenschaft x2": entry[4], "min-max": entry[5]}, ignore_index=True)



        for function in nebenbedingung_reactive_list.get():

            eigenschaft_total = None
            if function[2] == "int" and function[4] == "int":
                eigenschaft_total = "integer lp (ILP)"
            elif (function[2] == "int" and function[4] == "kon") or (function[2] == "kon" and function[4] == "int"):
                eigenschaft_total = "mixed integer lp (MILP)"
            elif function[2] == "kon" and function[4] == "kon":
                eigenschaft_total = "lineare Programmierung (LP)"


            zahlenbereiche_df.loc[len(zahlenbereiche_df)] = [function[0], function[2], function[4], eigenschaft_total]



        return render.DataGrid(zahlenbereiche_df)


    @output
    @render.ui
    def finale_auswahl_text():
        return update_finale_auswahl_text()

    #@reactive.event(nebenbedingung_reactive_list)
    @reactive.event(input.selectize_nebenbedingung, input.select_target_function)
    def update_finale_auswahl_text():

        selected_nebenbedingungen = reactive.Value([])
        selected_zielfunktion = reactive.Value([])
        updated_selected_nebenbedingungen = selected_nebenbedingungen.get().copy()
        updated_selected_zielfunktion = selected_zielfunktion.get().copy()

        for nebenbedingung in nebenbedingung_reactive_list.get():
            if nebenbedingung[0] in input.selectize_nebenbedingung():
                updated_selected_nebenbedingungen.append(nebenbedingung)
                selected_nebenbedingungen.set(updated_selected_nebenbedingungen)
        print(len(selected_nebenbedingungen.get()))
        print(selected_nebenbedingungen.get())

        for zielfunktion in zielfunktion_reactive_list.get():
            if zielfunktion[0] in input.select_target_function():
                updated_selected_zielfunktion.append(zielfunktion)
                selected_zielfunktion.set(updated_selected_zielfunktion)
        print(len(selected_zielfunktion.get()))
        print(selected_zielfunktion.get())








        if not selected_zielfunktion.get() and not selected_nebenbedingungen.get():
            return ui.HTML('<div style="text-align: center;"><b>Bitte Zielfunktion und Nebenbedingung(en) auswählen.</b></div>')

        elif selected_zielfunktion.get() or selected_nebenbedingungen.get():
            summarized_text_rest = "<br>Durch die Auswahl der Zielfunktionen<br> <br>und Nebenbedingungen ergibt sich<br> <br>folgende finale Auswahl für Ihr Problem:<br>"

            eigenschaften_liste = []
            for function in selected_zielfunktion.get():
                eigenschaften_liste.append(function[2])
                eigenschaften_liste.append(function[4])

            for function in selected_nebenbedingungen.get():
                eigenschaften_liste.append(function[2])
                eigenschaften_liste.append(function[4])

            if "int" in eigenschaften_liste and not "kon" in eigenschaften_liste:
                summarized_text_rest += "<br><br><b>Integer Linear Programming (ILP)</b>"
            elif "kon" in eigenschaften_liste and not "int" in eigenschaften_liste:
                summarized_text_rest += "<br><br><b>Linear Programming (LP)</b>"
            elif "int" in eigenschaften_liste and "kon" in eigenschaften_liste:
                summarized_text_rest += "<br><br><b>Mixed Integer Linear Programming (MILP)</b>"

            return ui.HTML(f'<div style="text-align: center;">{summarized_text_rest}</div>')


        #for function in nebenbedingung_reactive_list.get():
            #summarized_text_rest += "<br>" + function_as_text(function) + "<br>"
































    # @reactive.effect
#  @reactive.event(input.select_target_function)
#   def update_modul3_placeholder():
#        ui.update_numeric("zfkt_x1_update", value=target_function[1])

    @output
    @render.plot()
    def optimierung_plot():
            optimierung_plot_reactive()

    @reactive.event(input.selectize_nebenbedingung, input.select_target_function)
    def optimierung_plot_reactive():
        if not input.selectize_nebenbedingung() and not input.select_target_function():
            fig, ax = plt.subplots()
            ax.spines["top"].set_color("none")
            ax.spines["right"].set_color("none")
            ax.grid(True, ls="--")
            ax.set_xlabel("x1-axis")
            ax.set_ylabel("x2-axis")
            ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on = False)
            ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on = False)
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            return fig
        #elif not nebenbedingung_reactive_list.get():
            #return None
        else:
            selected_nebenbedingungen = reactive.Value([])
            selected_zielfunktion = reactive.Value([])
            updated_selected_nebenbedingungen = selected_nebenbedingungen.get().copy()
            updated_selected_zielfunktion = selected_zielfunktion.get().copy()

            for nebenbedingung in nebenbedingung_reactive_list.get():
                if nebenbedingung[0] in input.selectize_nebenbedingung():
                    updated_selected_nebenbedingungen.append(nebenbedingung)
                    selected_nebenbedingungen.set(updated_selected_nebenbedingungen)
            print(len(selected_nebenbedingungen.get()))
            print(selected_nebenbedingungen.get())

            for zielfunktion in zielfunktion_reactive_list.get():
                if zielfunktion[0] in input.select_target_function():
                    updated_selected_zielfunktion.append(zielfunktion)
                    selected_zielfunktion.set(updated_selected_zielfunktion)
            print(len(selected_zielfunktion.get()))
            print(selected_zielfunktion.get())

            fig, ax = plt.subplots()

            ax.spines["top"].set_color("none")
            ax.spines["right"].set_color("none")
            ax.grid(True, ls = "--")
            ax.set_xlabel("x1-axis")
            ax.set_ylabel("x2-axis")





            xlim_var = reactive.Value([])
            ylim_var = reactive.Value([])
            for nebenbedingung in selected_nebenbedingungen.get():
                xlim_var_update = xlim_var.get().copy()
                ylim_var_update = ylim_var.get().copy()
                schnittpunkt_x1 = calculate_schnittpunkte_x1_x2_axis(nebenbedingung)[0]
                schnittpunkt_x2 = calculate_schnittpunkte_x1_x2_axis(nebenbedingung)[1]
                random_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
                ax.plot([0, schnittpunkt_x1], [schnittpunkt_x2, 0], label=nebenbedingung[0], color=random_color)
                xlim_var_update.append(schnittpunkt_x1)
                ylim_var_update.append(schnittpunkt_x2)
                xlim_var.set(xlim_var_update)
                ylim_var.set(ylim_var_update)

            print(len(xlim_var.get()))
            print(len(ylim_var.get()))
            print(xlim_var.get())
            print(ylim_var.get())
            #ax.set_xlim(0,calculate_highest_xlim_ylim(xlim_var.get(), ylim_var.get())[0])
            #ax.set_ylim(0,calculate_highest_xlim_ylim(xlim_var.get(), ylim_var.get())[1])

            for zielfunktion in selected_zielfunktion.get():
                xlim_var_update = xlim_var.get().copy()
                ylim_var_update = ylim_var.get().copy()

                schnittpunkt_x1, schnittpunkt_x2 = calculate_schnittpunkte_x1_x2_axis(zielfunktion,xlim_var_update, ylim_var_update)
                ax.plot([0, schnittpunkt_x1], [schnittpunkt_x2, 0], label=zielfunktion[0], color="blue", ls="--")
                xlim_var_update.append(schnittpunkt_x1)
                ylim_var_update.append(schnittpunkt_x2)
                xlim_var.set(xlim_var_update)
                ylim_var.set(ylim_var_update)

            ax.set_xlim(0,math.ceil(((calculate_highest_xlim_ylim(xlim_var.get(), ylim_var.get())[0]) * 1.1)))
            ax.set_ylim(0,math.ceil(((calculate_highest_xlim_ylim(xlim_var.get(), ylim_var.get())[1]) * 1.1)))

            #ax.plot(calculate_highest_xlim_ylim(xlim_var.get(), ylim_var.get())[0], 0, ">k", transform=ax.get_yaxis_transform(), clip_on = False)
            #ax.plot(0, calculate_highest_xlim_ylim(xlim_var.get(), ylim_var.get())[1], "^k", transform=ax.get_xaxis_transform(), clip_on = False)


            ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on = False)
            ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on = False)
            #schnittpunkte_x1_axis = [[0, 4]]
            #schnittpunkte_x2_axis = [[6, 0]]
            #schnittpunkte_x1_axis_2 = [[0, 2]]
            #schnittpunkte_x2_axis_2 = [[3, 0]]
            #ax.plot(schnittpunkte_x1_axis, schnittpunkte_x2_axis, label="Linie durch (4,0) und (0,6)", color = "black")
           # ax.plot(schnittpunkte_x1_axis_2, schnittpunkte_x2_axis_2, label="Linie durch (2,0) und (0,3)", color = "black")

           # ax.annotate('Zulässiger\nBereich', [2, 2])


            #ax.plot([2.5, 2.5], [3.5, 3.5], color = 'blue', ls = "--")
            #ax.arrow(2.5, 3.5, -1, -0.5, head_width=0.2, head_length=0.2, fc='blue', ec='blue')
            #ax.annotate("Zielfunktion_optimal", [2.5, 3.5], color = "blue")

            #ax.plot(2,5, "or", markersize = 8)
            #ax.arrow(4.5, 5.5, -1, -0.5, head_width=0.2, head_length=0.2, fc='red', ec='red')
           # ax.annotate("Optimale Lösung", [4.5, 5.5], color = "red")

            #fig.savefig("Name.png", dpi =150)

            ax.legend()

            return fig
