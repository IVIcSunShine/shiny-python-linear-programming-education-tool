import os
import platform
import random
import sys
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
from shiny import render, reactive, ui
from shiny_files.calculations import *
from shiny_files.functions import *


def server(input, output, session):
    target_function_dict = reactive.Value({})
    nebenbedingung_dict = reactive.Value({})
    zielfunktion_reactive_list = reactive.Value([])
    nebenbedingung_reactive_list = reactive.value([])
    selected_nebenbedingungen_reactive_list = reactive.Value([])
    selected_zielfunktion_reactive_list = reactive.Value([])
    solved_problems_list = reactive.Value([])
    xlim_var = reactive.Value([])
    ylim_var = reactive.Value([])
    xlim_var_dict = reactive.Value({})
    ylim_var_dict = reactive.Value({})
    function_colors = reactive.Value({})
    art_of_optimization_reactive = reactive.Value("")
    fig_reactive = reactive.Value(None)
    ist_gleich_probleme_y_werte_reactive = reactive.Value([])
    import_statement_reactive = reactive.Value(False)
    sens_ana_ausschöpfen_reactive = reactive.Value([])
    sens_ana_schattenpreis_reactive = reactive.Value([])
    sens_ana_coeff_change_reactive = reactive.Value([])

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
            "Please enter your data:",
            ui.HTML("<br><br>"),
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
            ui.HTML("<br><br>"),
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
    #######################################################
    ##################Modal 3 Anfang#######################
    #######################################################
    @reactive.effect
    @reactive.event(input.action_button_zielfunktion_ändern)
    def modal3():
        m3 = ui.modal(
            ui.row(
                ui.column(6, ui.input_select(
                    "select_target_function_for_change",
                    "Bitte Zielfunktion wählen:",
                    choices=target_function_dict.get(),
                ), ),

                ui.HTML("<b>""Aktuelle Werte vorausgefüllt. Bei Bedarf ändern. ""</b>"),
                ui.HTML("<br><br>")
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""x1: ""</b>")),

                ui.column(8, ui.input_numeric("zfkt_x1_update", None, zielfunktion_reactive_list.get()[0][1], min=None,
                                              max=None,
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
                ui.column(8, ui.input_numeric("zfkt_x2_update", None, zielfunktion_reactive_list.get()[0][3], min=None,
                                              max=None,
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

    ########################################################
    ##################Modal 3 nde###########################
    ########################################################
    ########################################################
    ##################Modal 4 Anfang########################
    ########################################################

    @reactive.effect
    @reactive.event(input.action_button_zielfunktion_löschen)
    def modal4():
        m4 = ui.modal(
            ui.row(
                ui.column(5, ui.input_select(
                    "select_target_function_for_delete",
                    "Zielfunktion wählen:",

                    choices=target_function_dict.get(),
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

    ########################################################
    ##################Modal 4 nde###########################
    ########################################################
    ########################################################
    ##################Modal 5 Anfang########################
    ########################################################

    @reactive.effect
    @reactive.event(input.action_button_restriktionen_ändern)
    def modal5():
        m5 = ui.modal(
            ui.row(
                ui.column(6, ui.input_select(
                    "select_rest_function_mod5",
                    "Bitte Nebenbedingung wählen:",

                    choices=nebenbedingung_dict.get(),
                ), ),

                ui.HTML("<b>""Aktuelle Werte vorausgefüllt. Bei Bedarf ändern. ""</b>"),
                ui.HTML("<br>""<br>")
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""x1: ""</b>")),
                ui.column(8,
                          ui.input_numeric("rest_x1_update", None, nebenbedingung_reactive_list.get()[0][1], min=None,
                                           max=None,
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
                ui.column(8,
                          ui.input_numeric("rest_x2_update", None, nebenbedingung_reactive_list.get()[0][3], min=None,
                                           max=None,
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
                ui.column(8,
                          ui.input_numeric("rest_wert_update", None, nebenbedingung_reactive_list.get()[0][6], min=None,
                                           max=None,
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

    ########################################################
    ##################Modal 5 Ende##########################
    ########################################################
    ########################################################
    ##################Modal 6 Anfang########################
    ########################################################
    @reactive.effect
    @reactive.event(input.action_button_restriktionen_löschen)
    def modal6():
        m6 = ui.modal(
            ui.row(
                ui.column(5, ui.input_select(
                    "select_restriction_for_delete",
                    "Restriktion wählen:",
                    choices=nebenbedingung_dict.get(),
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

    ########################################################
    ##################Modal 6 Ende##########################
    ########################################################
    ########################################################
    ##################Modal 7 Anfang########################
    ########################################################
    @reactive.effect
    @reactive.event(input.save_graph_png)
    def modal7():


        m7 = ui.modal(
            ui.row(
                ui.column(4, ui.HTML("<b>""Name Graph""</b>")),
                ui.column(8, ui.input_text("name_graph", None, "Enter name of graph")),
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""Speicherpfad""</b>")),
                ui.column(8, ui.input_text("speicherpfad_graph", None, "Bsp.: C:/Users/.../Desktop")),
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""Bitte Wahl treffen""</b>")),
                ui.column(8,
                          ui.input_radio_buttons(
                              "radio_graph_dpi",
                              None,
                              {"vordefinierte_dpi": "vordefinierte DPI", "selbst_dpi": "DPI selbst wählen"},
                          )),
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""Wähle DPI""</b>")),
                ui.column(8,
                          ui.input_select(
                              "select_dpi",
                              None,
                              {"72": 72, "150": 150, "300": 300, "600": 600},
                          )),
            ),
            ui.row(
                ui.HTML("<b>""oder (je nach obiger Wahl)""</b>"),
                ui.HTML("<br><br>")
            ),
            ui.row(
                ui.column(4, ui.HTML("<b>""Bitte DPI eingeben""</b>")),
                ui.column(8,
                          ui.input_numeric("numeric_dpi", None, 1, min=1, max=None, step=1)),
            ),
            footer=ui.div(
                ui.input_action_button(id="cancel_button_7", label="Abbrechen"),
                ui.input_action_button(id="submit_button_7", label="Übermitteln"),
            ),
            title="Save Graph as PNG",
            easy_close=False,
            style="width: 100%;"
        )
        ui.modal_show(m7)

        ########################################################
        ##################Modal 7 Ende##########################
        ########################################################

    @reactive.effect
    @reactive.event(input.import_export_button)
    def modal8():
        m8 = ui.modal(
            ui.row(
                ui.column(4, ui.HTML("<b>""Name lp-Datei (nur bei Export)""</b>")),
                ui.column(8, ui.input_text("name_export", None, "Enter name of file")),
            ),
            ui.HTML("<br><br>"),
            ui.row(
                ui.column(4, ui.HTML("<b>""Dateipfad / Speicherpfad""</b>")),
                ui.column(8,
                          ui.input_text("speicherpfad_import_export", None, "Bsp.: C:/Users/.../Desktop/lp_file.lp")),
            ),
            ui.HTML("<br><br>"),
            ui.row(
                ui.column(4, ui.HTML("<b>""Bitte Wahl treffen""</b>")),
                ui.column(8,
                          ui.input_radio_buttons(
                              "radio_import_export",
                              None,
                              {"import": "import aus lp-Datei", "export": "export in lp-Datei"},
                          )),
            ),

            footer=ui.div(
                ui.input_action_button(id="cancel_button_8", label="Abbrechen"),
                ui.input_action_button(id="submit_button_8", label="Übermitteln"),
            ),
            title="Import or Export lp-file",
            easy_close=False,
            style="width: 100%;"
        )
        ui.modal_show(m8)

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

    @reactive.effect
    @reactive.event(input.cancel_button_7)
    def close_modal7_cancel():
        ui.modal_remove()

    @reactive.effect
    @reactive.event(input.cancel_button_8)
    def close_modal8_cancel():
        ui.modal_remove()

    @reactive.effect
    @reactive.event(input.cancel_button_9)
    def close_modal9_cancel():
        ui.modal_remove()

    ########################################################################
    ##################Submit Button#########################################
    ########################################################################
    #######################################################
    ##################Submit Button 1######################
    #######################################################
    @reactive.effect
    @reactive.event(input.submit_button)
    def create_target_function():

        if input.zfkt_name() == "" or not input.zfkt_x1() or not input.zfkt_x2() or not isinstance(input.zfkt_x1(), (int, float)) or not isinstance(input.zfkt_x2(), (int, float)):
            notification_popup("Sie haben ungültige Werte vergeben, bitte überprüfen Sie Ihre Eingaben.", message_type= "error")
        else:
            if not zielfunktion_reactive_list.get():
                name = input.zfkt_name()
            else:
                detected = False
                for function in zielfunktion_reactive_list.get():
                    if input.zfkt_name() in function[0]:
                        detected = True
                        counter = 0
                        for entry in zielfunktion_reactive_list.get():
                            if input.zfkt_name() in entry[0]:
                                counter += 1
                        name = input.zfkt_name() + "_" + str(counter)
                if detected == False:
                    name = input.zfkt_name()

            x1 = input.zfkt_x1()
            attribute_1 = input.zfkt_select_attribute_1()
            x2 = input.zfkt_x2()
            attribute_2 = input.zfkt_select_attribute_2()
            min_max = input.zfkt_select_minmax()

            updated_zielfunktion_reactive_list = zielfunktion_reactive_list.get().copy()
            updated_zielfunktion_reactive_list.append([name, x1, attribute_1, x2, attribute_2, min_max])
            zielfunktion_reactive_list.set(updated_zielfunktion_reactive_list)

            ui.update_action_button("action_button_zielfunktion_ändern", disabled=False)
            ui.update_action_button("action_button_zielfunktion_löschen", disabled=False)
            print(len(zielfunktion_reactive_list.get()))

            print(zielfunktion_reactive_list.get())

            copy_target_function_dict = target_function_dict.get().copy()
            for target_function in zielfunktion_reactive_list.get():
                copy_target_function_dict[target_function[0]] = target_function[0]
            target_function_dict.set(copy_target_function_dict)

            print(target_function_dict)
            ui.update_select("select_target_function", choices=target_function_dict.get(), selected=[])

            notification_popup("Zielfunktion erfolgreich hinzugefügt")

            ui.modal_remove()

    #######################################################
    ##################Submit Button 2######################
    #######################################################

    @reactive.effect
    @reactive.event(input.submit_button_2)
    def create_restriction():

        if input.rest_name() == "" or not input.rest_x1() or not input.rest_x2() or not isinstance(input.rest_x1(), (int, float)) or not isinstance(input.rest_x2(), (int, float)) or not input.numeric_wertebereich_nebenbedingungen() or not isinstance(input.numeric_wertebereich_nebenbedingungen(), (int, float)):
            notification_popup("Sie haben ungültige Werte vergeben, bitte überprüfen Sie Ihre Eingaben", message_type= "error")
        else:

            if not nebenbedingung_reactive_list.get():
                name = input.rest_name()
            else:
                detected = False
                for function in nebenbedingung_reactive_list.get():
                    if input.rest_name() in function[0]:
                        detected = True
                        counter = 0
                        for entry in nebenbedingung_reactive_list.get():
                            if input.rest_name() in entry[0]:
                                counter += 1
                        name = input.rest_name() + "_" + str(counter)
                if detected == False:
                    name = input.rest_name()
            x1 = input.rest_x1()
            attribute_1 = input.rest_select_attribute_1()
            x2 = input.rest_x2()
            attribute_2 = input.rest_select_attribute_2()
            wertebereich_symbol = input.select_wertebereich_nebenbedingung()
            wertebereich_wert = input.numeric_wertebereich_nebenbedingungen()

            updated_nebenbedingung_reactive_list = nebenbedingung_reactive_list.get().copy()
            updated_nebenbedingung_reactive_list.append(
                [name, x1, attribute_1, x2, attribute_2, wertebereich_symbol, wertebereich_wert])
            nebenbedingung_reactive_list.set(updated_nebenbedingung_reactive_list)

            ui.update_action_button("action_button_restriktionen_ändern", disabled=False)
            ui.update_action_button("action_button_restriktionen_löschen", disabled=False)

            print(function_as_text(nebenbedingung_reactive_list.get()[0]))
            print(len(nebenbedingung_reactive_list.get()))

            print(nebenbedingung_reactive_list.get())

            copy_nebenbedingung_reactive_dict = nebenbedingung_dict.get().copy()
            for restriction in nebenbedingung_reactive_list.get():
                copy_nebenbedingung_reactive_dict[restriction[0]] = restriction[0]
            nebenbedingung_dict.set(copy_nebenbedingung_reactive_dict)

            print(nebenbedingung_dict)
            ui.update_selectize("selectize_nebenbedingung", choices=nebenbedingung_dict.get())

            notification_popup("Nebenfunktion erfolgreich hinzugefügt")

            ui.modal_remove()

    #######################################################
    ##################Submit Button 3######################
    #######################################################

    @reactive.effect
    @reactive.event(input.submit_button_3)
    def close_modal3_by_uebermitteln():

        if input.zfkt_name_update() == "" or not input.zfkt_x1_update() or not input.zfkt_x2_update() or not isinstance(input.zfkt_x1_update(), (int, float)) or not isinstance(input.zfkt_x2_update(), (int, float)):
            notification_popup("Sie haben ungültige Werte vergeben, bitte überprüfen Sie Ihre Eingaben.", message_type= "error")
        else:

            selected_function_name = input.select_target_function_for_change()
            counter = 0
            for target_function in zielfunktion_reactive_list.get():
                if target_function[0] == selected_function_name:
                    updated_zielfunktion_reactive_list = zielfunktion_reactive_list.get().copy()
                    if input.zfkt_x1_update() != target_function[1]:
                        updated_zielfunktion_reactive_list[counter][1] = input.zfkt_x1_update()
                        zielfunktion_reactive_list.set(updated_zielfunktion_reactive_list)

                    if input.zfkt_select_attribute_1_update() != target_function[2]:
                        updated_zielfunktion_reactive_list[counter][2] = input.zfkt_select_attribute_1_update()
                        zielfunktion_reactive_list.set(updated_zielfunktion_reactive_list)

                    if input.zfkt_x2_update() != target_function[3]:
                        updated_zielfunktion_reactive_list[counter][3] = input.zfkt_x2_update()
                        zielfunktion_reactive_list.set(updated_zielfunktion_reactive_list)

                    if input.zfkt_select_attribute_2_update() != target_function[4]:
                        updated_zielfunktion_reactive_list[counter][4] = input.zfkt_select_attribute_2_update()
                        zielfunktion_reactive_list.set(updated_zielfunktion_reactive_list)

                    if input.zfkt_select_minmax_update() != target_function[5]:
                        updated_zielfunktion_reactive_list[counter][5] = input.zfkt_select_minmax_update()
                        zielfunktion_reactive_list.set(updated_zielfunktion_reactive_list)

                    if input.zfkt_name_update() != target_function[0]:
                        updated_zielfunktion_reactive_list[counter][0] = input.zfkt_name_update()
                        zielfunktion_reactive_list.set(updated_zielfunktion_reactive_list)

                        copy_target_function_dict = target_function_dict.get().copy()

                        copy_target_function_dict[input.zfkt_name_update()] = input.zfkt_name_update()
                        print(target_function_dict)
                        del copy_target_function_dict[selected_function_name]
                        target_function_dict.set(copy_target_function_dict)
                        print(target_function_dict)

                    ui.update_select("select_target_function", choices=target_function_dict.get())

                    print(function_as_text(target_function))
                    print(zielfunktion_reactive_list.get())

                counter += 1
            notification_popup("Zielfunktion erfolgreich geändert")
            ui.modal_remove()

    #######################################################
    ##################Submit Button 4######################
    #######################################################

    @reactive.effect
    @reactive.event(input.submit_button_4)
    def delete_target_function():
        updated_zielfunktion_reactive_list = zielfunktion_reactive_list.get().copy()
        copy_target_function_dict = target_function_dict.get().copy()
        for function in zielfunktion_reactive_list.get():
            if function[0] == input.select_target_function_for_delete():
                updated_zielfunktion_reactive_list.remove(function)
                zielfunktion_reactive_list.set(updated_zielfunktion_reactive_list)

                del copy_target_function_dict[input.select_target_function_for_delete()]
                target_function_dict.set(copy_target_function_dict)

        ui.update_select("select_target_function", choices=target_function_dict.get())
        if not zielfunktion_reactive_list.get():
            ui.update_action_button("action_button_zielfunktion_ändern", disabled=True)
            ui.update_action_button("action_button_zielfunktion_löschen", disabled=True)

        notification_popup("Zielfunktion erfolgreich gelöscht")
        ui.modal_remove()

        #######################################################
        ##################Submit Button 5######################
        #######################################################

    @reactive.effect
    @reactive.event(input.submit_button_5)
    def close_modal5_by_uebermitteln():

        if input.rest_name_update() == "" or not input.rest_x1_update() or not input.rest_x2_update() or not isinstance(input.rest_x1_update(), (int, float)) or not isinstance(input.rest_x2_update(), (int, float)) or not input.rest_wert_update() or not isinstance(input.rest_wert_update(), (int, float)):
            notification_popup("Sie haben ungültige Werte vergeben, bitte überprüfen Sie Ihre Eingaben", message_type= "error")
        else:

            selected_function_name = input.select_rest_function_mod5()
            counter = 0
            for restriction in nebenbedingung_reactive_list.get():
                if restriction[0] == selected_function_name:
                    updated_nebenbedingung_reactive_list = nebenbedingung_reactive_list.get().copy()
                    if input.rest_x1_update() != restriction[1]:
                        updated_nebenbedingung_reactive_list[counter][1] = input.rest_x1_update()
                        nebenbedingung_reactive_list.set(updated_nebenbedingung_reactive_list)

                    if input.rest_select_attribute_1_update() != restriction[2]:
                        updated_nebenbedingung_reactive_list[counter][2] = input.rest_select_attribute_1_update()
                    nebenbedingung_reactive_list.set(updated_nebenbedingung_reactive_list)

                    if input.rest_x2_update() != restriction[3]:
                        updated_nebenbedingung_reactive_list[counter][3] = input.rest_x2_update()
                        nebenbedingung_reactive_list.set(updated_nebenbedingung_reactive_list)

                    if input.rest_select_attribute_2_update() != restriction[4]:
                        updated_nebenbedingung_reactive_list[counter][4] = input.rest_select_attribute_2_update()
                        nebenbedingung_reactive_list.set(updated_nebenbedingung_reactive_list)

                    if input.rest_select_wertebereich_update() != restriction[5]:
                        updated_nebenbedingung_reactive_list[counter][5] = input.rest_select_wertebereich_update()
                        nebenbedingung_reactive_list.set(updated_nebenbedingung_reactive_list)

                    if input.rest_wert_update() != restriction[6]:
                        updated_nebenbedingung_reactive_list[counter][6] = input.rest_wert_update()
                        nebenbedingung_reactive_list.set(updated_nebenbedingung_reactive_list)

                    if input.rest_name_update() != restriction[0]:
                        updated_nebenbedingung_reactive_list[counter][0] = input.rest_name_update()
                        nebenbedingung_reactive_list.set(updated_nebenbedingung_reactive_list)

                        copy_nebenbedingung_reactive_dict = nebenbedingung_dict.get().copy()
                        copy_nebenbedingung_reactive_dict[input.rest_name_update()] = input.rest_name_update()
                        del copy_nebenbedingung_reactive_dict[selected_function_name]
                        nebenbedingung_dict.set(copy_nebenbedingung_reactive_dict)

                    ui.update_select("selectize_nebenbedingung", choices=nebenbedingung_dict.get())

                counter += 1

            notification_popup("Nebenfunktion erfolgreich geändert")
            ui.modal_remove()

        #######################################################
        ##################Submit Button 6######################
        #######################################################

    @reactive.effect
    @reactive.event(input.submit_button_6)
    def delete_restriction():
        updated_nebenbedingung_reactive_list = nebenbedingung_reactive_list.get().copy()
        copy_nebenbedingung_dict = nebenbedingung_dict.get().copy()
        for function in nebenbedingung_reactive_list.get():
            if function[0] == input.select_restriction_for_delete():
                updated_nebenbedingung_reactive_list.remove(function)
                nebenbedingung_reactive_list.set(updated_nebenbedingung_reactive_list)

                del copy_nebenbedingung_dict[input.select_restriction_for_delete()]
                nebenbedingung_dict.set(copy_nebenbedingung_dict)
        ui.update_selectize("selectize_nebenbedingung", choices=nebenbedingung_dict.get())
        if not nebenbedingung_reactive_list.get():
            ui.update_action_button("action_button_restriktionen_ändern", disabled=True)
            ui.update_action_button("action_button_restriktionen_löschen", disabled=True)

        notification_popup("Nebenfunktion erfolgreich gelöscht")
        ui.modal_remove()

        ########################################################################
        ##################Submit Button Ende####################################
        ########################################################################

        ########################################################################
        ##################Render Text Outputs###################################
        ########################################################################

    @output
    @render.ui
    def rest_text():
        return rest_text_reactive()

    @reactive.Calc
    def rest_text_reactive():
        summarized_text_rest = ""
        for function in nebenbedingung_reactive_list.get():
            summarized_text_rest += function_as_text(function) + "<br><br>"
        return ui.HTML(summarized_text_rest)

    @output
    @render.ui
    def zfkt_text():
        return zfkt_text_reactive()

    @reactive.Calc
    def zfkt_text_reactive():
        summarized_text = ""
        for function in zielfunktion_reactive_list.get():
            summarized_text += function_as_text(function) + "<br><br>"
        return ui.HTML(summarized_text)

    @reactive.effect
    @reactive.event(input.select_target_function_for_change)
    def update_target_function_changing_placeholder():
        selected_function_name = input.select_target_function_for_change()
        for target_function in zielfunktion_reactive_list.get():
            if target_function[0] == selected_function_name:
                ui.update_text("zfkt_name_update", value=target_function[0])
                ui.update_numeric("zfkt_x1_update", value=target_function[1])
                ui.update_select("zfkt_select_attribute_1_update", selected=target_function[2])
                ui.update_numeric("zfkt_x2_update", value=target_function[3])
                ui.update_select("zfkt_select_attribute_2_update", selected=target_function[4])
                ui.update_select("zfkt_select_minmax_update", selected=target_function[5])

    @output
    @render.text
    def mod4_text():
        return update_mod4_text()

    @reactive.event(input.select_target_function_for_delete)
    def update_mod4_text():
        for function in zielfunktion_reactive_list.get():
            if function[0] == input.select_target_function_for_delete():
                return function_as_text(function)

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

    @output
    @render.text
    def mod6_text():
        return update_mod6_text()

    @reactive.event(input.select_restriction_for_delete)
    def update_mod6_text():
        for function in nebenbedingung_reactive_list.get():
            if function[0] == input.select_restriction_for_delete():
                return function_as_text(function)

    @output
    @render.ui
    def finale_auswahl_text():
        return update_finale_auswahl_text()

    #@reactive.event(input.selectize_nebenbedingung, input.select_target_function, input.lineare_optimierung_button)
    #@reactive.effect
    @reactive.Calc
    def update_finale_auswahl_text():

        if not selected_zielfunktion_reactive_list.get() and not selected_nebenbedingungen_reactive_list.get():
            return ui.HTML(
                '<div style="text-align: center;"><b>Bitte Zielfunktion und Nebenbedingung(en) auswählen.</b></div>')

        else:
            try:



                update_art_of_optimization_reactive = ""

                updated_selected_nebenbedingungen_reactive_list = selected_nebenbedingungen_reactive_list.get().copy()
                updated_selected_zielfunktion_reactive_list = selected_zielfunktion_reactive_list.get().copy()

                for nebenbedingung in nebenbedingung_reactive_list.get():
                    if nebenbedingung[
                        0] in input.selectize_nebenbedingung() and nebenbedingung not in selected_nebenbedingungen_reactive_list.get():
                        updated_selected_nebenbedingungen_reactive_list.append(nebenbedingung)
                        selected_nebenbedingungen_reactive_list.set(updated_selected_nebenbedingungen_reactive_list)

                for zielfunktion in zielfunktion_reactive_list.get():
                    if zielfunktion[
                        0] in input.select_target_function() and zielfunktion not in selected_zielfunktion_reactive_list.get():
                        updated_selected_zielfunktion_reactive_list.append(zielfunktion)
                        selected_zielfunktion_reactive_list.set(updated_selected_zielfunktion_reactive_list)

                if not selected_zielfunktion_reactive_list.get() and not selected_nebenbedingungen_reactive_list.get():
                    update_art_of_optimization_reactive = "not defined"
                    art_of_optimization_reactive.set(update_art_of_optimization_reactive)
                    return ui.HTML(
                        '<div style="text-align: center;"><b>Bitte Zielfunktion und Nebenbedingung(en) auswählen.</b></div>')


                elif selected_zielfunktion_reactive_list.get() or selected_nebenbedingungen_reactive_list.get():
                    summarized_text_rest = "<br>Durch die Auswahl der Zielfunktionen<br> <br>und Nebenbedingungen ergibt sich<br> <br>folgende finale Auswahl für Ihr Problem:<br>"

                    eigenschaften_liste = []
                    for function in selected_zielfunktion_reactive_list.get():
                        eigenschaften_liste.append([function[2], "x1"])
                        eigenschaften_liste.append([function[4], "x2"])

                    for function in selected_nebenbedingungen_reactive_list.get():
                        eigenschaften_liste.append([function[2], "x1"])
                        eigenschaften_liste.append([function[4], "x2"])

                    eigenschaften_liste_nur_wertebereiche = [entry[0] for entry in eigenschaften_liste]

                    if "int" in eigenschaften_liste_nur_wertebereiche and not "kon" in eigenschaften_liste_nur_wertebereiche:
                        summarized_text_rest += "<br><b>Integer Linear Programming (ILP)</b><br>innerhalb dieses Wertebereiches:<br> <br><div style='text-align: center;'><b>x1 e No ; x2 e No</b></div>"
                        update_art_of_optimization_reactive = "ILP"
                        art_of_optimization_reactive.set(update_art_of_optimization_reactive)
                    elif "kon" in eigenschaften_liste_nur_wertebereiche and not "int" in eigenschaften_liste_nur_wertebereiche:
                        summarized_text_rest += "<br><b>Linear Programming (LP)</b><br>innerhalb dieses Wertebereiches:<br> <br><div style='text-align: center;'><b>x1 ≥ 0 ; x2 ≥ 0</b></div>"
                        update_art_of_optimization_reactive = "LP"
                        art_of_optimization_reactive.set(update_art_of_optimization_reactive)
                    elif "int" in eigenschaften_liste_nur_wertebereiche and "kon" in eigenschaften_liste_nur_wertebereiche:
                        summarized_text_rest += "<br><b>Mixed Integer Linear Programming (MILP)</b>"

                        x1_int_counter = 0
                        x1_kon_counter = 0
                        x2_int_counter = 0
                        x2_kon_counter = 0
                        for entry in eigenschaften_liste:
                            if entry[1] == "x1" and entry[0] == "int":
                                x1_int_counter += 1
                            elif entry[1] == "x1" and entry[0] == "kon":
                                x1_kon_counter += 1
                            elif entry[1] == "x2" and entry[0] == "int":
                                x2_int_counter += 1
                            elif entry[1] == "x2" and entry[0] == "kon":
                                x2_kon_counter += 1

                        if (len(eigenschaften_liste) / 2) == x1_int_counter and (
                                len(eigenschaften_liste) / 2) == x2_kon_counter:
                            summarized_text_rest += "<br>innerhalb dieses Wertebereiches:<br> <br><div style='text-align: center;'><b>x1 e No ; x2 ≥ 0</b></div>"
                            update_art_of_optimization_reactive = "MILP_x1_int_x2_kon"
                            art_of_optimization_reactive.set(update_art_of_optimization_reactive)
                        elif (len(eigenschaften_liste) / 2) == x1_kon_counter and (
                                len(eigenschaften_liste) / 2) == x2_int_counter:
                            summarized_text_rest += "<br>innerhalb dieses Wertebereiches:<br> <br><div style='text-align: center;'><b>x1 ≥ 0 ; x2 e No</b></div>"
                            update_art_of_optimization_reactive = "MILP_x1_kon_x2_int"
                            art_of_optimization_reactive.set(update_art_of_optimization_reactive)
                        else:
                            if selected_nebenbedingungen_reactive_list.get():
                                summarized_text_rest += "<br>innerhalb dieses Wertebereiches:<br> <br><div style='text-align: center;'><b>Please set x1 and x2 only to one Wert</b></div>"
                                update_art_of_optimization_reactive = "not defined"
                                art_of_optimization_reactive.set(update_art_of_optimization_reactive)
                            #else:


                    return ui.HTML(f'<div style="text-align: center;">{summarized_text_rest}</div>')
            except TypeError:
                return ui.HTML(
                    '<div style="text-align: center;"><b>Bitte Zielfunktion und Nebenbedingung(en) auswählen.</b></div>')
        ########################################################################
        ##################Render DataFrames#####################################
        ########################################################################

    @output
    @render.data_frame
    def zahlenbereiche_df_output():
        return update_zahlenbereiche_df_output()

    @reactive.Calc
    def update_zahlenbereiche_df_output():

        zahlenbereiche_df = pd.DataFrame(columns=["Name", "x1", "x2", "Total"])

        for function in zielfunktion_reactive_list.get():

            eigenschaft_total = None
            if function[2] == "int" and function[4] == "int":
                eigenschaft_total = "integer lp (ILP)"
            elif (function[2] == "int" and function[4] == "kon") or (function[2] == "kon" and function[4] == "int"):
                eigenschaft_total = "mixed integer lp (MILP)"
            elif function[2] == "kon" and function[4] == "kon":
                eigenschaft_total = "lineare Programmierung (LP)"

            zahlenbereiche_df.loc[len(zahlenbereiche_df)] = [function[0], function[2], function[4], eigenschaft_total]

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
    @render.data_frame
    def lp_results_df():
        return update_lp_results_df()

    @reactive.Calc
    def update_lp_results_df():

        try:
            if not solved_problems_list.get():
                result_df = pd.DataFrame({
                    "Name": [""],
                    "x1": [""],
                    "x2": [""]
                })

                return render.DataGrid(result_df)

            if solved_problems_list.get():
                name_column = ""
                for zielfunktion in zielfunktion_reactive_list.get():
                    if zielfunktion[0] in input.select_target_function():
                        name_column = zielfunktion[0]

                result_df = pd.DataFrame({
                    name_column: [solved_problems_list.get()[0][6]],
                    "x1": [solved_problems_list.get()[1][0]],
                    "x2": [solved_problems_list.get()[1][1]]
                })

                return render.DataGrid(result_df)

        except TypeError:
            result_df = pd.DataFrame({
                "Name": [""],
                "x1": [""],
                "x2": [""]
            })

            return render.DataGrid(result_df)

    ########################################################################
    ##################Render Plot###########################################
    ########################################################################

    @reactive.effect
    @reactive.event(input.selectize_nebenbedingung, input.select_target_function)
    def update_selected_lists():
        # Aktualisierte Listen initialisieren
        updated_selected_nebenbedingungen_reactive_list = []
        updated_selected_zielfunktion_reactive_list = []

        # Füge nur die tatsächlich ausgewählten Nebenbedingungen hinzu
        for nebenbedingung in nebenbedingung_reactive_list.get():
            if nebenbedingung[0] in input.selectize_nebenbedingung():
                updated_selected_nebenbedingungen_reactive_list.append(nebenbedingung)

        # Füge nur die tatsächlich ausgewählte Zielfunktion hinzu
        for zielfunktion in zielfunktion_reactive_list.get():
            if zielfunktion[0] == input.select_target_function():
                updated_selected_zielfunktion_reactive_list.append(zielfunktion)

        # Setze die aktualisierten Listen
        selected_nebenbedingungen_reactive_list.set(updated_selected_nebenbedingungen_reactive_list)
        selected_zielfunktion_reactive_list.set(updated_selected_zielfunktion_reactive_list)

        # Debug-Ausgabe, um zu prüfen, ob die Listen korrekt aktualisiert werden
        print("Aktualisierte Nebenbedingungen:", selected_nebenbedingungen_reactive_list.get())
        print("Aktualisierte Zielfunktion:", selected_zielfunktion_reactive_list.get())

        solved_problems_list.set([])
        print("Solved Problems List:", solved_problems_list.get())

    @output
    @render.plot()
    def optimierung_plot():
        optimierung_plot_reactive()

    @reactive.event(input.selectize_nebenbedingung, input.select_target_function, input.lineare_optimierung_button)
    def optimierung_plot_reactive():

        status_x1_x2_wertebereiche = check_x1_x2()
        print(f"status: {status_x1_x2_wertebereiche}")

        #if status_x1_x2_wertebereiche[0] != 1 or status_x1_x2_wertebereiche[1] != 1 or (not input.selectize_nebenbedingung() and not input.select_target_function()):

        if (not input.selectize_nebenbedingung() and not input.select_target_function()) or status_x1_x2_wertebereiche[2] == "unselected_zielfunktion" or status_x1_x2_wertebereiche[2] == "unselected_nebenbedingungen":
            fig, ax = plt.subplots()
            ax.spines["top"].set_color("none")
            ax.spines["right"].set_color("none")
            ax.grid(True, ls="--")
            ax.set_xlabel("x1-axis")
            ax.set_ylabel("x2-axis")
            ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
            ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ui.update_action_button("lineare_optimierung_button", disabled=True)
            ui.update_action_button("Sensitivity_analysis_button", disabled=True)
            ui.update_action_button("save_graph_png", disabled=True)
            if input.selectize_nebenbedingung() and not input.select_target_function():
                notification_popup("Bitte wählen Sie auch eine Zielfunktion aus.", message_type="warning")
            elif not input.selectize_nebenbedingung() and input.select_target_function():
                notification_popup("Bitte wählen Sie auch mindestens eine Nebenbedingung aus.", message_type="warning")
            return fig


        elif (status_x1_x2_wertebereiche[0] != 1 or status_x1_x2_wertebereiche[1] != 1) and status_x1_x2_wertebereiche[2] == "alles_selected":
            notification_popup("Die vergebenen Wertebereich jeweils für x1 und x2 sind nicht einheitlich, bitte überprüfen Sie Ihre Eingaben, sodass alle x1 den selben Wertebereich haben und alle x2 den selben Wertebereich haben.",
                               message_type="error")
            notification_popup("Graph konnte nicht erstellt werden.",
                               message_type="error")
            fig, ax = plt.subplots()
            ax.spines["top"].set_color("none")
            ax.spines["right"].set_color("none")
            ax.grid(True, ls="--")
            ax.set_xlabel("x1-axis")
            ax.set_ylabel("x2-axis")
            ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
            ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ui.update_action_button("lineare_optimierung_button", disabled=True)
            ui.update_action_button("Sensitivity_analysis_button", disabled=True)
            ui.update_action_button("save_graph_png", disabled=True)
            return fig



        else:
            try:
                ui.update_action_button("save_graph_png", disabled=False)
                print("------vorher-------")
                print(target_function_dict.get())
                print(nebenbedingung_dict.get())
                print(zielfunktion_reactive_list.get())
                print(len(zielfunktion_reactive_list.get()))
                print(nebenbedingung_reactive_list.get())
                print(len(nebenbedingung_reactive_list.get()))
                print(selected_zielfunktion_reactive_list.get())
                print(len(selected_zielfunktion_reactive_list.get()))
                print(selected_nebenbedingungen_reactive_list.get())
                print(len(selected_nebenbedingungen_reactive_list.get()))
                print(xlim_var.get())
                print(len(xlim_var.get()))
                print(ylim_var.get())
                print(len(ylim_var.get()))
                print(xlim_var_dict.get())
                print(ylim_var_dict.get())
                print(function_colors.get())
                print("-------------")

                fig, ax = plt.subplots()

                ax.spines["top"].set_color("none")
                ax.spines["right"].set_color("none")
                ax.grid(True, ls="--")
                ax.set_xlabel("x1-axis")
                ax.set_ylabel("x2-axis")

                xlim_var_update = []
                ylim_var_update = []
                function_colors_update = {}
                xlim_var_dict_update = {}
                ylim_var_dict_update = {}

                print(f"vor for-Schleife neben{selected_nebenbedingungen_reactive_list.get()}")
                for nebenbedingung in selected_nebenbedingungen_reactive_list.get():
                    print(f"in for-Schleife neben{selected_nebenbedingungen_reactive_list.get()}")

                    schnittpunkt_x1 = calculate_schnittpunkte_x1_x2_axis(nebenbedingung)[0]
                    schnittpunkt_x2 = calculate_schnittpunkte_x1_x2_axis(nebenbedingung)[1]

                    random_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))

                    ax.plot([0, schnittpunkt_x1], [schnittpunkt_x2, 0], label=nebenbedingung[0], color=random_color)

                    xlim_var_update.append([schnittpunkt_x1, nebenbedingung[0]])

                    ylim_var_update.append([schnittpunkt_x2, nebenbedingung[0]])

                    xlim_var_dict_update[nebenbedingung[0]] = schnittpunkt_x1
                    ylim_var_dict_update[nebenbedingung[0]] = schnittpunkt_x2

                    function_colors_update[nebenbedingung[0]] = random_color

                    xlim_var.set(xlim_var_update)
                    ylim_var.set(ylim_var_update)

                    xlim_var_dict.set(xlim_var_dict_update)
                    ylim_var_dict.set(ylim_var_dict_update)

                    function_colors.set(function_colors_update)

                print(f"vor for-Schleife ziel{selected_zielfunktion_reactive_list.get()}")
                for zielfunktion in selected_zielfunktion_reactive_list.get():
                    print(f"in for-Schleife ziel{selected_zielfunktion_reactive_list.get()}")

                    schnittpunkt_x1, schnittpunkt_x2 = calculate_schnittpunkte_x1_x2_axis(zielfunktion, xlim_var_update,
                                                                                          ylim_var_update)

                    ax.plot([0, schnittpunkt_x1], [schnittpunkt_x2, 0], label=zielfunktion[0] + " (dummy)", color="#00FF00",
                            ls="--")

                    xlim_var_update.append([schnittpunkt_x1, zielfunktion[0]])

                    ylim_var_update.append([schnittpunkt_x2, zielfunktion[0]])

                    xlim_var_dict_update[zielfunktion[0]] = schnittpunkt_x1
                    ylim_var_dict_update[zielfunktion[0]] = schnittpunkt_x2

                    function_colors_update[zielfunktion[0]] = "#00FF00"

                    xlim_var.set(xlim_var_update)
                    ylim_var.set(ylim_var_update)

                    xlim_var_dict.set(xlim_var_dict_update)
                    ylim_var_dict.set(ylim_var_dict_update)

                    function_colors.set(function_colors_update)

                ax.set_xlim(0, math.ceil(((calculate_highest_xlim_ylim(xlim_var.get(), ylim_var.get())[0]) * 1.1)))
                ax.set_ylim(0, math.ceil(((calculate_highest_xlim_ylim(xlim_var.get(), ylim_var.get())[1]) * 1.1)))

                ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
                ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

                ui.update_action_button("lineare_optimierung_button", disabled=False)

                # zulässiger Bereich

                if input.selectize_nebenbedingung():
                    with ui.Progress() as progress_bar_feasible_region:
                        progress_bar_feasible_region.set(message="Calculating Graph", detail="loading... please wait")
                        progress_bar_feasible_region.set(0.1)

                        # sammelt sets (Mengen). Jedes Set enthält Punkte, die zu einer Nebenbedingung gehören
                        new_liste_geraden_punkte_sets_reactive = []

                        ist_gleich_probleme_y_werte_reactive.set([])
                        equals_detected = False

                        highest_selected_x1 = 0
                        highest_selected_x2 = 0

                        # Die höchsten x1 und x2 Werte der ausgewählten Nebenbedingungen werden ermittelt
                        # Zudem werden die Nebenfunktionen mit einem "=" ermittelt und nach vorne sortiert. Diese müssen zuerst berechnet werden, um den zulässigen Bereich zu ermitteln
                        # Da sont zweimal berechnet werden müsste
                        sorted_nebenfunktionen = []

                        for nebenfunktion in selected_nebenbedingungen_reactive_list.get():
                            if xlim_var_dict.get()[nebenfunktion[0]] > highest_selected_x1:
                                highest_selected_x1 = xlim_var_dict.get()[nebenfunktion[0]]
                            if ylim_var_dict.get()[nebenfunktion[0]] > highest_selected_x2:
                                highest_selected_x2 = ylim_var_dict.get()[nebenfunktion[0]]
                            if nebenfunktion[5] == "=":
                                sorted_nebenfunktionen.insert(0, nebenfunktion)
                            elif nebenfunktion[5] != "=":
                                sorted_nebenfunktionen.append(nebenfunktion)
                        print(f"Länge sorted_nebenfunktionen {len(sorted_nebenfunktionen)}")
                        print(f"sorted_nebenfunktionen {sorted_nebenfunktionen}")
                        # Die x1 und x2 Werte der ausgewählten Nebenbedingungen werden in einem bestimmten Massstab dargestellt. Für weitere Berechnungen.
                        massstab_x1 = (highest_selected_x1 / 750) + ((1 / 750) * (highest_selected_x1 / 750))
                        massstab_x2 = (highest_selected_x2 / 400) + ((1 / 400) * (highest_selected_x2 / 400))
                        # zusätzliche x1 und x2 Werte, die zu den x1 und x2 Werten der ausgewählten Nebenbedingungen hinzugefügt werden müssen, um den zulässigen Bereich zu ermitteln
                        zusätzlich_zu_x_range_hinzuzufügende_x1_Werte = []
                        zusätzlich_zu_y_range_hinzuzufügende_x2_Werte = []
                        ist_gleich_probleme_y_werte = []

                        for_counter = 0

                        # Schranken-Variable zur Überprüfung, ob größer- und kleiner-gleich Bedingungen erneut durchlaufen werden müssen
                        # reprocess_all_conditions = False

                        progress_bar_feasible_region.set(0.2)
                        for nebenfunktion in sorted_nebenfunktionen:
                            punkte = set()

                            if nebenfunktion[5] == "=":

                                x_range = None

                                if art_of_optimization_reactive.get() == "LP" or art_of_optimization_reactive.get() == "MILP_x1_kon_x2_int" or art_of_optimization_reactive.get() == "MILP_x1_int_x2_kon":

                                    x_range = np.arange(0, xlim_var_dict.get()[nebenfunktion[0]], massstab_x1)
                                    if xlim_var_dict.get()[nebenfunktion[0]] not in x_range:
                                        x_range = np.append(x_range, xlim_var_dict.get()[nebenfunktion[0]])
                                        zusätzlich_zu_x_range_hinzuzufügende_x1_Werte.append(
                                            xlim_var_dict.get()[nebenfunktion[0]])
                                    if for_counter > 0 and zusätzlich_zu_x_range_hinzuzufügende_x1_Werte:
                                        for entry in zusätzlich_zu_x_range_hinzuzufügende_x1_Werte:

                                            if entry not in x_range and entry < xlim_var_dict.get()[nebenfunktion[0]]:
                                                x_range = np.append(x_range, entry)

                                    progress_bar_feasible_region.set(0.5)
                                    for x in x_range:
                                        y_max = y_ergebnis_an_geradengleichung(xlim_var_dict.get()[nebenfunktion[0]],
                                                                               ylim_var_dict.get()[nebenfunktion[0]], x)

                                        punkte.add((x, y_max))
                                        ist_gleich_probleme_y_werte.append((x, y_max))

                                    equals_detected = True
                                    ist_gleich_probleme_y_werte_reactive.set(ist_gleich_probleme_y_werte)
                                    progress_bar_feasible_region.set(0.8)











                                elif art_of_optimization_reactive.get() == "ILP" or art_of_optimization_reactive.get() == "MILP_x1_int_x2_kon" or art_of_optimization_reactive.get() == "MILP_x1_kon_x2_int":

                                    if xlim_var_dict.get()[nebenfunktion[0]] % 1 != 0:
                                        x_range = np.arange(0, xlim_var_dict.get()[nebenfunktion[0]], 1)
                                    elif xlim_var_dict.get()[nebenfunktion[0]] % 1 == 0:
                                        x_range = np.arange(0, xlim_var_dict.get()[nebenfunktion[0]] + 1, 1)

                                    progress_bar_feasible_region.set(0.5)
                                    for x in x_range:
                                        y = y_ergebnis_an_geradengleichung(xlim_var_dict.get()[nebenfunktion[0]],
                                                                           ylim_var_dict.get()[nebenfunktion[0]], x)
                                        if y % 1 != 0:
                                            continue
                                        elif y % 1 == 0:
                                            punkte.add((x, y))

                                    equals_detected = True
                                    progress_bar_feasible_region.set(0.8)







                            elif nebenfunktion[5] == "≤":

                                y_range = None
                                x_range = None
                                print(f"art of optimization {art_of_optimization_reactive.get()}")

                                if art_of_optimization_reactive.get() == "LP" or art_of_optimization_reactive.get() == "MILP_x1_kon_x2_int":

                                    x_range = np.arange(0, xlim_var_dict.get()[nebenfunktion[0]], massstab_x1)
                                    if xlim_var_dict.get()[nebenfunktion[0]] not in x_range:
                                        x_range = np.append(x_range, xlim_var_dict.get()[nebenfunktion[0]])
                                        zusätzlich_zu_x_range_hinzuzufügende_x1_Werte.append(
                                            xlim_var_dict.get()[nebenfunktion[0]])
                                    if for_counter > 0 and zusätzlich_zu_x_range_hinzuzufügende_x1_Werte:
                                        for entry in zusätzlich_zu_x_range_hinzuzufügende_x1_Werte:
                                            if entry not in x_range and entry < xlim_var_dict.get()[nebenfunktion[0]]:
                                                x_range = np.append(x_range, entry)
                                    progress_bar_feasible_region.set(0.5)



                                elif art_of_optimization_reactive.get() == "ILP" or art_of_optimization_reactive.get() == "MILP_x1_int_x2_kon":

                                    # nur Ganzzahlen
                                    # bei Kommazahl beim letzten x-Wert: gerader letzter x-Wert mit dabei
                                    if xlim_var_dict.get()[nebenfunktion[0]] % 1 != 0:
                                        x_range = np.arange(0, xlim_var_dict.get()[nebenfunktion[0]], 1)
                                    # bei Ganzzahl beim letzten x-Wert: gerader letzter x-Wert nicht mit dabei, deswegen +1
                                    elif xlim_var_dict.get()[nebenfunktion[0]] % 1 == 0:
                                        x_range = np.arange(0, xlim_var_dict.get()[nebenfunktion[0]] + 1, 1)
                                    progress_bar_feasible_region.set(0.5)
                                #print(len(x_range))
                                print(f"x_range {x_range}")

                                for x in x_range:
                                    y_max = y_ergebnis_an_geradengleichung(xlim_var_dict.get()[nebenfunktion[0]],
                                                                           ylim_var_dict.get()[nebenfunktion[0]], x)

                                    if art_of_optimization_reactive.get() == "LP" or art_of_optimization_reactive.get() == "MILP_x1_int_x2_kon":

                                        y_range = np.arange(0, y_max, massstab_x2)
                                        if y_max not in y_range:
                                            y_range = np.append(y_range, y_max)
                                            zusätzlich_zu_y_range_hinzuzufügende_x2_Werte.append(
                                                y_max)
                                        if for_counter > 0 and zusätzlich_zu_y_range_hinzuzufügende_x2_Werte:
                                            for entry in zusätzlich_zu_y_range_hinzuzufügende_x2_Werte:
                                                if entry not in y_range and entry < y_max:
                                                    y_range = np.append(y_range, entry)

                                        for y in y_range:
                                            punkte.add(

                                                (x, y))

                                        if ist_gleich_probleme_y_werte_reactive.get():
                                            for ist_gleich_problem_punkte in ist_gleich_probleme_y_werte_reactive.get():
                                                x_wert, y_wert = ist_gleich_problem_punkte
                                                if x_wert == x and y_wert <= y_max:
                                                    punkte.add((x, y_wert))

                                        progress_bar_feasible_region.set(0.8)








                                    elif art_of_optimization_reactive.get() == "ILP" or art_of_optimization_reactive.get() == "MILP_x1_kon_x2_int":

                                        if y_max % 1 != 0:
                                            for y in np.arange(0, y_max, 1):
                                                punkte.add((x, y))


                                        elif y_max % 1 == 0:
                                            for y in np.arange(0, y_max + 1, 1):
                                                punkte.add((x, y))
                                        progress_bar_feasible_region.set(0.8)
                                print(len(punkte))
                                print(f"punkte {punkte}")











                            elif nebenfunktion[5] == "≥":

                                max_y_wert = ax.get_ylim()[1]
                                x_range = None
                                y_range = None

                                if art_of_optimization_reactive.get() == "LP" or art_of_optimization_reactive.get() == "MILP_x1_kon_x2_int":

                                    x_range = np.arange(0, ax.get_xlim()[1], massstab_x1)
                                    if xlim_var_dict.get()[nebenfunktion[0]] not in x_range:
                                        x_range = np.append(x_range, xlim_var_dict.get()[nebenfunktion[0]])
                                        zusätzlich_zu_x_range_hinzuzufügende_x1_Werte.append(
                                            xlim_var_dict.get()[nebenfunktion[0]])
                                    if for_counter > 0 and zusätzlich_zu_x_range_hinzuzufügende_x1_Werte:
                                        for entry in zusätzlich_zu_x_range_hinzuzufügende_x1_Werte:

                                            if entry not in x_range:
                                                x_range = np.append(x_range, entry)

                                    progress_bar_feasible_region.set(0.5)
















                                elif art_of_optimization_reactive.get() == "ILP" or art_of_optimization_reactive.get() == "MILP_x1_int_x2_kon":

                                    if ax.get_xlim()[1] % 1 != 0:
                                        x_range = np.arange(0, ax.get_xlim()[1], 1)
                                    elif ax.get_xlim()[1] % 1 == 0:
                                        x_range = np.arange(0, ax.get_xlim()[1] + 1, 1)

                                    progress_bar_feasible_region.set(0.5)

                                for x in x_range:

                                    y_min = None

                                    if x <= xlim_var_dict.get()[nebenfunktion[0]]:
                                        y_min = y_ergebnis_an_geradengleichung(
                                            xlim_var_dict.get()[nebenfunktion[0]],
                                            ylim_var_dict.get()[nebenfunktion[0]],
                                            x
                                        )
                                    elif x > xlim_var_dict.get()[nebenfunktion[0]]:

                                        y_min = 0

                                    if art_of_optimization_reactive.get() == "LP" or art_of_optimization_reactive.get() == "MILP_x1_int_x2_kon":

                                        y_range_total = np.arange(0, max_y_wert, massstab_x2)
                                        if max_y_wert not in y_range_total:
                                            y_range_total = np.append(y_range_total, max_y_wert)
                                        if y_min not in y_range_total:
                                            y_range_total = np.append(y_range_total, y_min)
                                            zusätzlich_zu_y_range_hinzuzufügende_x2_Werte.append(y_min)
                                        if for_counter > 0 and zusätzlich_zu_y_range_hinzuzufügende_x2_Werte:
                                            for entry in zusätzlich_zu_y_range_hinzuzufügende_x2_Werte:
                                                if entry not in y_range_total and entry < y_min:
                                                    y_range_total = np.append(y_range_total, entry)

                                        if x <= xlim_var_dict.get()[nebenfunktion[0]]:
                                            y_range_under_line = np.arange(0, y_min, massstab_x2)
                                            if y_min in y_range_under_line:
                                                y_range_under_line = y_range_under_line[y_range_under_line != y_min]

                                            # gibt symmetrische Differenz mit eizigartigen Elementen zurück
                                            y_range = np.setxor1d(y_range_total, y_range_under_line)

                                        elif x > xlim_var_dict.get()[nebenfunktion[0]]:
                                            y_range = y_range_total

                                        for y in y_range:
                                            punkte.add(

                                                (x, y))

                                        if ist_gleich_probleme_y_werte_reactive.get():
                                            for ist_gleich_problem_punkte in ist_gleich_probleme_y_werte_reactive.get():

                                                x_wert, y_wert = ist_gleich_problem_punkte
                                                if x_wert == x and y_wert >= y_min:
                                                    punkte.add((x, y_wert))

                                        progress_bar_feasible_region.set(0.8)








                                    elif art_of_optimization_reactive.get() == "ILP" or art_of_optimization_reactive.get() == "MILP_x1_kon_x2_int":

                                        if y_min % 1 != 0:
                                            for y in np.arange(math.trunc(y_min) + 1, max_y_wert + 1, 1):
                                                punkte.add((x, y))

                                        elif y_min % 1 == 0:
                                            for y in np.arange(y_min, max_y_wert + 1, 1):
                                                punkte.add((x, y))

                                        progress_bar_feasible_region.set(0.8)

                            new_liste_geraden_punkte_sets_reactive.append(punkte)

                            for_counter += 1

                        progress_bar_feasible_region.set(0.9)

                        print(len(new_liste_geraden_punkte_sets_reactive))

                        schnittmenge_punkte = None
                        counter = 0

                        for set_entry in new_liste_geraden_punkte_sets_reactive:
                            if counter == 0:
                                schnittmenge_punkte = set_entry
                            elif counter > 0:
                                schnittmenge_punkte = schnittmenge_punkte.intersection(set_entry)
                            counter += 1

                        gemeinsame_x1_werte = [punkt[0] for punkt in schnittmenge_punkte]
                        gemeinsame_x2_werte = [punkt[1] for punkt in schnittmenge_punkte]

                        print("Gemeinsame x1-Werte: " + str(len(gemeinsame_x1_werte)))
                        print("Gemeinsame x2-Werte: " + str(len(gemeinsame_x2_werte)))

                        if art_of_optimization_reactive.get() == "ILP":
                            ax.scatter(gemeinsame_x1_werte, gemeinsame_x2_werte, color='grey', s=5, alpha=0.8)
                        elif equals_detected == True:
                            ax.scatter(gemeinsame_x1_werte, gemeinsame_x2_werte, color='grey', s=8, alpha=1)
                        elif art_of_optimization_reactive.get() == "MILP_x1_int_x2_kon" or art_of_optimization_reactive.get() == "MILP_x1_kon_x2_int":
                            ax.scatter(gemeinsame_x1_werte, gemeinsame_x2_werte, color='lightgrey', s=5, alpha=0.6)
                        else:
                            ax.scatter(gemeinsame_x1_werte, gemeinsame_x2_werte, color='lightgrey', s=4, alpha=0.2)

                        progress_bar_feasible_region.set(1)

                if solved_problems_list.get():
                    function_colors_update = function_colors.get().copy()

                    schnittpunkt_x1 = calculate_schnittpunkte_x1_x2_axis(solved_problems_list.get()[0])[0]
                    schnittpunkt_x2 = calculate_schnittpunkte_x1_x2_axis(solved_problems_list.get()[0])[1]
                    ax.plot([0, schnittpunkt_x1], [schnittpunkt_x2, 0],
                            label=solved_problems_list.get()[0][0] + " (optimiert)", color="#0000FF", ls="--")

                    ax.plot(solved_problems_list.get()[1][0], solved_problems_list.get()[1][1], "or", markersize=8)

                    x_axis_ticks = ax.get_xticks()
                    y_axis_ticks = ax.get_yticks()
                    abstand_zweier_xticks = x_axis_ticks[2] - x_axis_ticks[1]
                    abstand_zweier_yticks = y_axis_ticks[2] - y_axis_ticks[1]
                    opt_lösung_arrow_start_x = solved_problems_list.get()[1][0] + abstand_zweier_xticks
                    opt_lösung_arrow_start_y = solved_problems_list.get()[1][1] + abstand_zweier_yticks
                    ax.arrow(opt_lösung_arrow_start_x, opt_lösung_arrow_start_y, abstand_zweier_xticks * 0.9 * -1,
                             abstand_zweier_yticks * 0.9 * -1, color="red",
                             width=(((abstand_zweier_xticks + abstand_zweier_yticks) / 2) * (1 / 50)),
                             head_width=abstand_zweier_xticks * 0.05, head_length=abstand_zweier_yticks * 0.15,
                             length_includes_head=True)
                    ax.annotate("Optimale Lösung", [opt_lösung_arrow_start_x, opt_lösung_arrow_start_y], color="red")

                    # Erstellung des grünen Pfeils und der Beschriftung "Verschiebung". Indem die Geradengleichung der dummy-Zielfunktion berechnet wird (mx +b)
                    steigung_zielfunktion_dummy = (
                            (ylim_var_dict.get()[selected_zielfunktion_reactive_list.get()[0][0]] - 0) / (
                            0 - xlim_var_dict.get()[selected_zielfunktion_reactive_list.get()[0][0]]))
                    b_dummy = (-1) * steigung_zielfunktion_dummy * xlim_var_dict.get()[
                        selected_zielfunktion_reactive_list.get()[0][0]]

                    # die VAriablen die für die Berechnung der Koordinaten des Lotfußpunktes benötigt werden
                    b = 1 * xlim_var_dict.get()[selected_zielfunktion_reactive_list.get()[0][0]]
                    a = steigung_zielfunktion_dummy * xlim_var_dict.get()[
                        selected_zielfunktion_reactive_list.get()[0][0]] * (-1)
                    c = b_dummy * xlim_var_dict.get()[selected_zielfunktion_reactive_list.get()[0][0]] * (-1)
                    x0 = solved_problems_list.get()[1][0]
                    y0 = solved_problems_list.get()[1][1]

                    # anschließend werden die Koordinaten des Lotfußpunktes berechnet
                    coord_lot_x1 = ((b * ((b * x0) - (a * y0))) - (a * c)) / ((a * a) + (b * b))
                    coord_lot_x2 = ((a * ((((-1) * b) * x0) + (a * y0))) - (b * c)) / ((a * a) + (b * b))

                    # anschließend wird der Abstand des Lotfußpunktes zur optimalen Lösung berechnet
                    x1_abstand_lot_x1_zu_opt_lös_punkt = solved_problems_list.get()[1][0] - coord_lot_x1
                    x2_abstand_lot_x2_zu_opt_lös_punkt = solved_problems_list.get()[1][1] - coord_lot_x2

                    # Je nach Zielfunktion wird der Pfeil in die entsprechende Richtung gezeichnet
                    if selected_zielfunktion_reactive_list.get()[0][5] == "max":

                        ax.arrow(coord_lot_x1, coord_lot_x2, x1_abstand_lot_x1_zu_opt_lös_punkt * 0.9,
                                 x2_abstand_lot_x2_zu_opt_lös_punkt * 0.9, color="#008800",
                                 width=(((abstand_zweier_xticks + abstand_zweier_yticks) / 2) * (1 / 50)),
                                 head_width=abstand_zweier_xticks * 0.05, head_length=abstand_zweier_yticks * 0.15,
                                 length_includes_head=True)
                        ax.annotate("Verschiebung", [coord_lot_x1, coord_lot_x2], color="#008800")
                    elif selected_zielfunktion_reactive_list.get()[0][5] == "min":

                        ax.arrow(coord_lot_x1, coord_lot_x2, x1_abstand_lot_x1_zu_opt_lös_punkt * 0.9,
                                 x2_abstand_lot_x2_zu_opt_lös_punkt * 0.9, color="#008800",
                                 width=(((abstand_zweier_xticks + abstand_zweier_yticks) / 2) * (1 / 50)),
                                 head_width=abstand_zweier_xticks * 0.05, head_length=abstand_zweier_yticks * 0.15,
                                 length_includes_head=True)
                        ax.annotate("Verschiebung", [coord_lot_x1, coord_lot_x2], color="#008800")

                    function_colors_update[solved_problems_list.get()[0][0]] = "#0000FF"
                    function_colors.set(function_colors_update)

                if selected_nebenbedingungen_reactive_list.get() and not solved_problems_list.get():
                    dummy_patch = mpatches.Patch(color='grey', label='Feasible Region')

                    ax.legend(handles=[dummy_patch] + ax.get_legend_handles_labels()[0], loc="upper right")
                elif selected_nebenbedingungen_reactive_list.get() and solved_problems_list.get():

                    dummy_patch_1 = mlines.Line2D([], [], color='red', marker='o', linestyle='None', markersize=10,
                                                  label=f'Optimale Lösung\n{solved_problems_list.get()[0][0]}: {solved_problems_list.get()[0][6]}\nx1: {solved_problems_list.get()[1][0]}\nx2: {solved_problems_list.get()[1][1]}')
                    dummy_patch_2 = mpatches.Patch(color='grey', label='Feasible Region')
                    ax.legend(handles=[dummy_patch_1, dummy_patch_2] + ax.get_legend_handles_labels()[0], loc="upper right")
                else:
                    ax.legend(loc="upper right")

                print("------nachher-------")
                print(target_function_dict.get())
                print(nebenbedingung_dict.get())
                print(zielfunktion_reactive_list.get())
                print(len(zielfunktion_reactive_list.get()))
                print(nebenbedingung_reactive_list.get())
                print(len(nebenbedingung_reactive_list.get()))
                print(selected_zielfunktion_reactive_list.get())
                print(len(selected_zielfunktion_reactive_list.get()))
                print(selected_nebenbedingungen_reactive_list.get())
                print(len(selected_nebenbedingungen_reactive_list.get()))
                print(xlim_var.get())
                print(len(xlim_var.get()))
                print(ylim_var.get())
                print(len(ylim_var.get()))
                print(xlim_var_dict.get())
                print(ylim_var_dict.get())
                print(function_colors.get())
                print("-------------")

                fig_reactive.set(fig)
                notification_popup("Graph erfolgreich erstellt")
                return fig
            except TypeError:

                notification_popup("Bitte unselecten Sie die Nebenbedingungen und wählen Sie die von Ihnen benötigten erneut aus.")

                fig, ax = plt.subplots()
                ax.spines["top"].set_color("none")
                ax.spines["right"].set_color("none")
                ax.grid(True, ls="--")
                ax.set_xlabel("x1-axis")
                ax.set_ylabel("x2-axis")
                ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
                ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)
                ax.set_xlim(0, 10)
                ax.set_ylim(0, 10)
                ui.update_action_button("lineare_optimierung_button", disabled=True)
                ui.update_action_button("Sensitivity_analysis_button", disabled=True)
                ui.update_action_button("save_graph_png", disabled=True)
                return fig


    ########################################################################
    ##################Lineare Optimierung Button############################
    ########################################################################

    @reactive.effect
    @reactive.event(input.lineare_optimierung_button)
    def initialize_lin_opt():
        #try:

            selected_operatoren = [entry[5] for entry in selected_nebenbedingungen_reactive_list.get()]


            status_x1_x2_wertebereiche = check_x1_x2()

            if status_x1_x2_wertebereiche[0] != 1 or status_x1_x2_wertebereiche[1] != 1:
                notification_popup("Bitte vergeben Sie nur einen Wertebreich jeweils für x1 und x2.", message_type="error")

            if selected_operatoren.count("≥") == len(selected_operatoren) and selected_zielfunktion_reactive_list.get()[0][5] == "max":
                notification_popup("Lineare Optimierung nicht möglich! Das Problem ist Unbounded. Bitte ändern Sie die Nebenbedingungen oder die Zielfunktion.", message_type="error")


            else:


                updated_solved_problems_list = []

                print("---------Art of Optimization---------")
                print("Art of Optimization: " + art_of_optimization_reactive.get())
                print("---------Art of Optimization---------")
                erg, schnittpunkte = solve_linear_programming_problem(selected_zielfunktion_reactive_list.get()[0],
                                                                      selected_nebenbedingungen_reactive_list.get(),
                                                                      art_of_optimization_reactive.get())

                solved_target_function = [selected_zielfunktion_reactive_list.get()[0][0],
                                          selected_zielfunktion_reactive_list.get()[0][1],
                                          selected_zielfunktion_reactive_list.get()[0][2],
                                          selected_zielfunktion_reactive_list.get()[0][3],
                                          selected_zielfunktion_reactive_list.get()[0][4], "=", erg]

                updated_solved_problems_list.append(solved_target_function)
                updated_solved_problems_list.append(schnittpunkte)
                solved_problems_list.set(updated_solved_problems_list)

                print(solved_problems_list.get())

                ui.update_action_button("Sensitivity_analysis_button", disabled=False)


                notification_popup("Lineare Optimierung erfolgreich durchgeführt.")

        #except TypeError:
            #notification_popup("Ihr Problem hat im gültigen Bereich keine Feasible Region. Bitte ändern Sie die Nebenbedingungen oder die Zielfunktion.")

    @output
    @render.ui
    def beschreibung_text():
        return update_beschreibung_text()

    @reactive.event(input.selectize_nebenbedingung, input.select_target_function, input.lineare_optimierung_button,
                    input.Sensitivity_analysis_button)
    def update_beschreibung_text():
        try:
            status_x1_x2_wertebereiche = check_x1_x2()

            if status_x1_x2_wertebereiche[0] != 1 or status_x1_x2_wertebereiche[1] != 1 or (not selected_zielfunktion_reactive_list.get() and not selected_nebenbedingungen_reactive_list.get()):
                return ui.HTML(
                    '<div style="text-align: center;"><b>Bitte Zielfunktion und Nebenbedingung(en) auswählen.</b></div>')

            elif selected_zielfunktion_reactive_list.get() or selected_nebenbedingungen_reactive_list.get():
                summarized_text_rest = ""

                if solved_problems_list.get():
                    summarized_text_rest += '<div style="text-align: center;"><u><b>--------Optimale Lösung Information--------</b></u></div><br>'
                    summarized_text_rest += f'Die optimale Lösung für die Zielfunktion <p style="color: #0000FF;">{solved_problems_list.get()[0][0]} (optimiert)</p> schneidet die <b>x1-axis</b> bei <b>{solved_problems_list.get()[1][0]}</b> und die <b>x2-axis</b> bei <b>{solved_problems_list.get()[1][1]}</b> und hat den optimalen Wert <p style="color: #FF0000;">{solved_problems_list.get()[0][6]}</p>.<br><br>'

                if sens_ana_ausschöpfen_reactive.get():
                    summarized_text_rest += '<div style="text-align: center;"><u><b>--------Sensitivity Analysis Information--------</b></u></div><br>'
                    summarized_text_rest += '<div style="text-align: center;"><u><b>---Ausschöpfen der Nebenbedingungen---</b></u></div><br>'

                    counter = 0
                    for entry in sens_ana_ausschöpfen_reactive.get()[2]:
                        if entry == 0:
                            name = selected_nebenbedingungen_reactive_list.get()[counter][0]
                            summarized_text_rest += f'Die Nebenbedingung <p style="color: {function_colors.get()[name]};"> {name}</p> ist eine <b>einschränkende</b> Nebenbedingung. Sie besitzt einen <b>Slack von 0</b>.<br>'
                        elif entry != 0:
                            name = selected_nebenbedingungen_reactive_list.get()[counter][0]
                            summarized_text_rest += f'Die Nebenbedingung <p style="color: {function_colors.get()[name]};"> {name}</p> ist <b>keine einschränkende</b> Nebenbedingung. Sie besitzt einen <b>Slack von {entry}</b>.<br>'
                        counter += 1

                if sens_ana_schattenpreis_reactive.get():
                    summarized_text_rest += '<div style="text-align: center;"><u><b>---Schattenpreise---</b></u></div><br>'

                    counter = 0
                    for entry in sens_ana_schattenpreis_reactive.get():

                        max_or_min = selected_zielfunktion_reactive_list.get()[0][5]
                        status = None
                        if max_or_min == "max":
                            status = ["Erhöhung", "erhöhen"]
                        elif max_or_min == "min":
                            status = ["Verringerung", "verringern"]
                        name = selected_nebenbedingungen_reactive_list.get()[counter][0]

                        if float(entry[0]) != 0:
                            if solved_problems_list.get():
                                summarized_text_rest += (
                                    f'Eine {status[0]} des rechten Wertes der Nebenbedingung <p style="color: {function_colors.get()[name]};"> {name}</p> um <b>1</b> würde den Wert der Zielfunktion um <b>{entry[0]}</b>, von <b>{solved_problems_list.get()[0][6]}</b> auf <b>{solved_problems_list.get()[0][6] + float(entry[0])}</b> {status[1]}. Diese {status[0]} ist gültig, '
                                    f'solange sich die rechte Seite im Bereich zwischen <b>{entry[1]}</b> und <b>{entry[2]}</b> befindet.<br><br>')
                            elif not solved_problems_list.get():
                                summarized_text_rest += (
                                    f'Eine {status[0]} des rechten Wertes der Nebenbedingung <p style="color: {function_colors.get()[name]};"> {name}</p> um <b>1</b> würde den Wert der Zielfunktion um <b>{entry[0]}</b> {status[1]}. Diese {status[0]} ist gültig, '
                                    f'solange sich die rechte Seite im Bereich zwischen <b>{entry[1]}</b> und <b>{entry[2]}</b> befindet.<br><br>')
                        elif float(entry[0]) == 0:
                            summarized_text_rest += (
                                f'Die Nebenbedingung <p style="color: {function_colors.get()[name]};"> {name}</p> ist keine einschränkende Bedingung. Ihr Schattenpreis ist <b>0</b> und somit spielt die Änderung der rechten Seite dieser Nebenbedingung keine Rolle.<br><br>')
                        counter += 1

                if sens_ana_coeff_change_reactive.get():
                    summarized_text_rest += '<div style="text-align: center;"><u><b>---Koeffizientenänderung---</b></u></div><br>'
                    summarized_text_rest += f'Solange der Zielfunktionskoeffizient von <b>x1</b> zwischen <b>{sens_ana_coeff_change_reactive.get()[0][0]}</b> und <b>{sens_ana_coeff_change_reactive.get()[0][1]}</b> und der Zielfunktionskoeffizient von <b>x2</b> zwischen <b>{sens_ana_coeff_change_reactive.get()[1][0]}</b> und <b>{sens_ana_coeff_change_reactive.get()[1][1]}</b> liegt, bleibt die optimale Lösung <b>x1 = {solved_problems_list.get()[1][0]}</b> und <b>x2 = {solved_problems_list.get()[1][1]}</b> bestehen.<br><br>'

                for zielfunktion in selected_zielfunktion_reactive_list.get():
                    summarized_text_rest += '<div style="text-align: center;"><u><b>--------Dummy-Zielfunktion Information--------</b></u></div><br>'
                    summarized_text_rest += f'Die <p style="color: #00FF00;">(Dummy)-Zielfunktion {zielfunktion[0]}</p> schneidet die <b>x1-axis</b> bei <b>{xlim_var_dict.get()[zielfunktion[0]]}</b> und die <b>x2-axis</b> bei <b>{ylim_var_dict.get()[zielfunktion[0]]}</b>.<br><br>'

                counter = 0
                for nebenbedingung in selected_nebenbedingungen_reactive_list.get():
                    if counter == 0:
                        summarized_text_rest += '<div style="text-align: center;"><u><b>--------Nebenbedingung(en) Information--------</b></u></div><br>'
                    summarized_text_rest += f'Die <p style="color: {function_colors.get()[nebenbedingung[0]]};">Nebenbedingung {nebenbedingung[0]}</p> schneidet die <b>x1-axis</b> bei <b>{xlim_var_dict.get()[nebenbedingung[0]]}</b> und die <b>x2-axis</b> bei <b>{ylim_var_dict.get()[nebenbedingung[0]]}</b>.<br><br>'
                    counter += 1

                return ui.HTML(f'<div style="text-align: center;">{summarized_text_rest}</div>')

        except TypeError:
            notification_popup(
                "Ihr Problem hat im gültigen Bereich keine Feasible Region. Bitte ändern Sie die Nebenbedingungen oder die Zielfunktion.")
            return ui.HTML(
                '<div style="text-align: center;"><b>Bitte Zielfunktion und Nebenbedingung(en) auswählen.</b></div>')
        except IndexError:
            return ui.HTML(
                '<div style="text-align: center;"><b>Bitte Zielfunktion und Nebenbedingung(en) auswählen.</b></div>')

    @reactive.effect
    @reactive.event(input.submit_button_7)
    def save_graph_png_and_close_mod7():

        try:

            if input.name_graph() == "" or input.speicherpfad_graph() == "":
                notification_popup("Bitte gebe einen gültigen Namen und Speicherpfad an.")
            elif input.numeric_dpi() == "" or input.numeric_dpi() <= 0 or not isinstance(input.numeric_dpi(), (int, float)):
                notification_popup("Bitte gebe eine gültige DPI-Zahl an.")
            else:


                fig = fig_reactive.get()
                speicherpfad = input.speicherpfad_graph()
                if speicherpfad[-1] != "/":
                    speicherpfad += "/"

                dpi_wahl = 0

                if input.radio_graph_dpi() == "vordefinierte_dpi":
                    dpi_wahl = input.select_dpi()
                elif input.radio_graph_dpi() == "selbst_dpi":
                    dpi_wahl = input.numeric_dpi()

                if fig is None:
                    print("Fehler: Keine Figur vorhanden zum Speichern.")
                print(f"dpi-wahl:{dpi_wahl}")
                fig.savefig(speicherpfad + input.name_graph() + ".png", dpi=int(dpi_wahl))

                notification_popup("Graph erfolgreich gespeichert")

                ui.modal_remove()
        except FileNotFoundError:
            notification_popup("Bitte gebe einen gültigen Speicherpfad an.", message_type="error")
        except TypeError:
            notification_popup("Bitte überprüfe deine Eingaben.", message_type="error")

    def notification_popup(text_message, message_type = "message",message_duration = 4.0):
        ui.notification_show(
            text_message,
            type=message_type,
            duration=message_duration,
        )

    @reactive.effect
    @reactive.event(input.submit_button_8)
    def import_export_lp_file():
        try:


            status_x1_x2_wertebereiche = check_x1_x2()


            if (input.radio_import_export() == "export" and input.name_export() == "") or (input.radio_import_export() == "export" and input.speicherpfad_import_export() == "") or (input.radio_import_export() == "export" and input.speicherpfad_import_export().endswith(".lp") == True):
                notification_popup("Bitte geben Sie beim export einen gültigen Namen ein und wähle einen Speicherpfad aus.", message_type="error")

            elif (input.radio_import_export() == "import" and input.speicherpfad_import_export() == "") or (input.radio_import_export() == "import" and not input.speicherpfad_import_export().endswith(".lp")):
                notification_popup("Bitte wählen Sie eine gültige Datei im .lp-Format aus.", message_type="error")
            elif not selected_zielfunktion_reactive_list.get() or not selected_nebenbedingungen_reactive_list.get():
                notification_popup("Bitte wählen Sie vor dem Export eine zielfunktion und Nebenfunktion(en) aus.",
                                   message_type="error")
            elif status_x1_x2_wertebereiche[0] != 1 or status_x1_x2_wertebereiche[1] != 1:
                notification_popup("Bitte vergeben Sie für x1 und x2 jeweils den selben Wertebereich.", message_type="error")




            else:



                user_operating_system = platform.system()
                speicherpfad_trennsymbol = None
                if user_operating_system == "Windows":
                    speicherpfad_trennsymbol = "\\"
                elif user_operating_system == "Linux":
                    speicherpfad_trennsymbol = "/"
                # Für MAC OS
                elif user_operating_system == "Darwin":
                    speicherpfad_trennsymbol = "/"

                if input.radio_import_export() == "export":
                    generate_lp_file(selected_zielfunktion_reactive_list.get()[0],
                                     selected_nebenbedingungen_reactive_list.get(), art_of_optimization_reactive.get(),
                                     speicherpfad=(
                                             input.speicherpfad_import_export() + speicherpfad_trennsymbol + input.name_export() + ".lp"))
                    notification_popup("Datei erfolgreich im .lp-Format exportiert.")

                elif input.radio_import_export() == "import":
                    import_list = []
                    with open(input.speicherpfad_import_export(), "r") as file:
                        for line in file:
                            elements = line.strip().split()

                            import_list.append(elements)
                        print(import_list)
                        print(len(import_list))

                    art_of_optimization_import = None
                    x1_art = None
                    x2_art = None
                    if import_list[(len(import_list) - 1)][0] == "int" and import_list[(len(import_list) - 1)][
                        (len(import_list[(len(import_list) - 1)]) - 1)] == "x2;" and import_list[(len(import_list) - 1)][
                        (len(import_list[(len(import_list) - 1)]) - 2)] == "x1,":
                        art_of_optimization_import = "ILP"
                        x1_art = "int"
                        x2_art = "int"
                    elif import_list[(len(import_list) - 1)][0] == "int" and import_list[(len(import_list) - 1)][
                        (len(import_list[(len(import_list) - 1)]) - 1)] == "x1;":
                        art_of_optimization_import = "MILP_x1_int_x2_kon"
                        x1_art = "int"
                        x2_art = "kon"
                    elif import_list[(len(import_list) - 1)][0] == "int" and import_list[(len(import_list) - 1)][
                        (len(import_list[(len(import_list) - 1)]) - 1)] == "x2;" and not import_list[(len(import_list) - 1)][(
                            len(import_list[(len(import_list) - 1)]) - 2)] == "x1,":
                        art_of_optimization_import = "MILP_x1_kon_x2_int"
                        x1_art = "kon"
                        x2_art = "int"
                    elif import_list[(len(import_list) - 1)][1] == "=" or import_list[(len(import_list) - 1)][1] == "<=" or \
                            import_list[(len(import_list) - 1)][1] == ">=":
                        art_of_optimization_import = "LP"
                        x1_art = "kon"
                        x2_art = "kon"

                    imported_zielfunktion = []
                    imported_nebenfunktionen = []
                    counter = 1
                    for element in import_list:
                        if element[0] == "max:" or element[0] == "min:":

                            imported_zielfunktion = ["Function", float(element[1]), x1_art, float(element[4]), x2_art,
                                                     element[0][0:3]]
                        elif element[0] not in ["max:", "min:", "x1", "x2", "int"]:
                            operator = None

                            if element[5] == "<=":
                                operator = "≤"
                            elif element[5] == ">=":
                                operator = "≥"
                            elif element[5] == "=":
                                operator = "="

                            imported_nebenfunktion = ["Constraint_" + str(counter), float(element[0]), x1_art,
                                                      float(element[3]), x2_art, operator, float(element[6][:-1])]
                            imported_nebenfunktionen.append(imported_nebenfunktion)

                            counter += 1

                    zielfunktion_reactive_list.set([imported_zielfunktion])
                    nebenbedingung_reactive_list.set(imported_nebenfunktionen)

                    target_function_dict.set({})
                    copy_target_function_dict = target_function_dict.get().copy()
                    for target_function in zielfunktion_reactive_list.get():
                        copy_target_function_dict[target_function[0]] = target_function[0]
                    target_function_dict.set(copy_target_function_dict)

                    all_names_nebenbedingungen = []
                    nebenbedingung_dict.set({})
                    copy_nebenbedingung_reactive_dict = nebenbedingung_dict.get().copy()
                    for restriction in nebenbedingung_reactive_list.get():
                        copy_nebenbedingung_reactive_dict[restriction[0]] = restriction[0]
                        all_names_nebenbedingungen.append(restriction[0])
                    nebenbedingung_dict.set(copy_nebenbedingung_reactive_dict)

                    selected_zielfunktion_reactive_list.set([imported_zielfunktion])
                    selected_nebenbedingungen_reactive_list.set(imported_nebenfunktionen)
                    art_of_optimization_reactive.set(art_of_optimization_import)

                    import_statement_reactive.set(True)

                    ui.update_action_button("action_button_zielfunktion_ändern", disabled=False)
                    ui.update_action_button("action_button_zielfunktion_löschen", disabled=False)
                    ui.update_action_button("action_button_restriktionen_ändern", disabled=False)
                    ui.update_action_button("action_button_restriktionen_löschen", disabled=False)
                    ui.update_action_button("lineare_optimierung_button", disabled=False)
                    ui.update_selectize("selectize_nebenbedingung", choices=nebenbedingung_dict.get(),
                                        selected=all_names_nebenbedingungen)
                    ui.update_select("select_target_function", choices=target_function_dict.get())
                    ui.update_action_button("Sensitivity_analysis_button", disabled=True)

                    notification_popup("Daten erfolgreich importiert.")

                ui.modal_remove()
        except FileNotFoundError:
            notification_popup("Bitte wählen Sie eine gültige Datei aus.", message_type="error")
        except IndexError:
            notification_popup("Bitte wählen Sie vor dem export zumindest eine Zielfunktion aus.", message_type="error")
        except ValueError:
            notification_popup("Bitte überprüfen Sie Ihre Datei auf korrekten Inhalt vor dem Import.", message_type="error")

    @reactive.effect
    @reactive.event(input.Sensitivity_analysis_button)
    def sensitivity_analysis():

        # Basispfad relativ zu server.py
        basis_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        lp_solve_paths = {
            "darwin": os.path.join(basis_directory, "lp_solve_5.5", "lp_solve", "bin", "mac", "lp_solve"),
            "windows": os.path.join(basis_directory, "lp_solve_5.5", "lp_solve", "bin", "windows64", "lp_solve.exe"),
            "linux": os.path.join(basis_directory, "lp_solve_5.5", "lp_solve", "bin", "linux", "lp_solve")
        }

        # Zugriff auf den Pfad für das aktuelle Betriebssystem
        # Aktuelles Betriebssystem erkennen
        executable_lp = None
        current_os = sys.platform
        if current_os.startswith("linux"):
            executable_lp = lp_solve_paths["linux"]
        elif current_os == "darwin":
            executable_lp = lp_solve_paths["darwin"]
        elif current_os == "windows":
            executable_lp = lp_solve_paths["windows"]

        print("Pfad zur ausführbaren Datei:", executable_lp)
        lp_problem_saving_path = os.path.join(basis_directory, "shiny_files", "lp_file.lp")

        generate_lp_file(selected_zielfunktion_reactive_list.get()[0],
                         selected_nebenbedingungen_reactive_list.get(),
                         art_of_optimization_reactive.get(), lp_problem_saving_path)

        lp_solve_output = solve_sensitivity_analysis(executable_lp, lp_problem_saving_path, "-S5")
        print(lp_solve_output.stdout)

        sens_ana_ausschöpfen = ausschöpfen_nebenbedingung_und_slack(lp_solve_output.stdout)
        sens_ana_ausschöpfen_reactive.set(sens_ana_ausschöpfen)

        sens_ana_schattenpreis = schattenpreis(lp_solve_output.stdout)
        sens_ana_schattenpreis_reactive.set(sens_ana_schattenpreis)

        sens_ana_coeff_change = coeff_change(lp_solve_output.stdout)
        sens_ana_coeff_change_reactive.set(sens_ana_coeff_change)

        notification_popup("Sensitivitätsanalyse erfolgreich durchgeführt.")

    @output
    @render.data_frame
    def sens_ana_ausschöpfen_df():
        return update_sens_ana_ausschöpfen_df()

    @reactive.Calc
    def update_sens_ana_ausschöpfen_df():

        if not sens_ana_ausschöpfen_reactive.get():
            sens_result_df_1 = pd.DataFrame({
                "Name": [""],
                "Right border": [""],
                "Actual value": [""],
                "Slack": [""],
                "Eigenschaft": [""],
            })

            return render.DataGrid(sens_result_df_1)

        if sens_ana_ausschöpfen_reactive.get():

            names = []
            for function in selected_nebenbedingungen_reactive_list.get():
                names.append(function[0])

            sens_result_df_1 = pd.DataFrame({
                "Name": names,
                "Right border": sens_ana_ausschöpfen_reactive.get()[0],
                "Actual value": sens_ana_ausschöpfen_reactive.get()[1],
                "Slack": sens_ana_ausschöpfen_reactive.get()[2],
                "Eigenschaft": sens_ana_ausschöpfen_reactive.get()[3],
            })

            return render.DataGrid(sens_result_df_1)

    @output
    @render.data_frame
    def sens_ana_schattenpreis_df():
        return update_sens_ana_schattenpreis_df()

    @reactive.Calc
    def update_sens_ana_schattenpreis_df():

        if not sens_ana_schattenpreis_reactive.get():
            sens_result_df_2 = pd.DataFrame({
                "Name": [""],
                "Schattenpreis": [""],
                "From (untere Grenze)": [""],
                "Till (obere Grenze)": [""]
            })

            return render.DataGrid(sens_result_df_2)

        if sens_ana_schattenpreis_reactive.get():

            names = []
            for function in selected_nebenbedingungen_reactive_list.get():
                names.append(function[0])

            sens_result_df_2 = pd.DataFrame({
                "Name": names,
                "Schattenpreis": [eintrag[0] for eintrag in sens_ana_schattenpreis_reactive.get()],
                "From (untere Grenze)": [eintrag[1] for eintrag in sens_ana_schattenpreis_reactive.get()],
                "Till (obere Grenze)": [eintrag[2] for eintrag in sens_ana_schattenpreis_reactive.get()]
            })

            return render.DataGrid(sens_result_df_2)

    @output
    @render.data_frame
    def sens_ana_coeff_change_df():
        return update_sens_ana_coeff_change_df()

    @reactive.Calc
    def update_sens_ana_coeff_change_df():

        if not sens_ana_coeff_change_reactive.get():
            sens_result_df_3 = pd.DataFrame({
                "Variable": ["x1", "x2"],
                "From": ["", ""],
                "Till": ["", ""],
                "FromValue": ["", ""]
            })

            return render.DataGrid(sens_result_df_3)

        if sens_ana_coeff_change_reactive.get():
            sens_result_df_3 = pd.DataFrame({
                "Variable": ["x1", "x2"],
                "From": [eintrag[0] for eintrag in sens_ana_coeff_change_reactive.get()],
                "Till": [eintrag[1] for eintrag in sens_ana_coeff_change_reactive.get()],
                "FromValue": [eintrag[2] for eintrag in sens_ana_coeff_change_reactive.get()]
            })

            return render.DataGrid(sens_result_df_3)

    @reactive.effect
    @reactive.event(input.reset_button)
    def reset_all():

        target_function_dict.set({})
        nebenbedingung_dict.set({})
        zielfunktion_reactive_list.set([])
        nebenbedingung_reactive_list.set([])
        selected_nebenbedingungen_reactive_list.set([])
        selected_zielfunktion_reactive_list.set([])
        solved_problems_list.set([])
        xlim_var.set([])
        ylim_var.set([])
        xlim_var_dict.set({})
        ylim_var_dict.set({})
        function_colors.set({})
        art_of_optimization_reactive.set("")
        fig_reactive.set(None)
        ist_gleich_probleme_y_werte_reactive.set([])
        import_statement_reactive.set(False)
        sens_ana_ausschöpfen_reactive.set([])
        sens_ana_schattenpreis_reactive.set([])
        sens_ana_coeff_change_reactive.set([])

        ui.update_action_button("action_button_zielfunktion_ändern", disabled=True)
        ui.update_action_button("action_button_zielfunktion_löschen", disabled=True)
        ui.update_action_button("action_button_restriktionen_ändern", disabled=True)
        ui.update_action_button("action_button_restriktionen_löschen", disabled=True)
        ui.update_action_button("lineare_optimierung_button", disabled=True)
        ui.update_action_button("Sensitivity_analysis_button", disabled=True)
        ui.update_action_button("x1_x2_Wertebereich_setzen", disabled=True)
        ui.update_selectize("selectize_nebenbedingung", choices={},
                            selected=[])
        ui.update_select("select_target_function", choices={})
        ui.update_text("beschreibung_text", value=ui.HTML(
            '<div style="text-align: center;"><b>Bitte Zielfunktion und Nebenbedingung(en) auswählen.</b></div>'))
        ui.update_text("finale_auswahl_text", value=ui.HTML(
            '<div style="text-align: center;"><b>Bitte Zielfunktion und Nebenbedingung(en) auswählen.</b></div>'))

        notification_popup("Alle Daten zurückgesetzt", message_type="warning")

    @reactive.effect
    @reactive.event(input.x1_x2_Wertebereich_setzen)
    def modal9():
        values_1 = {"LP": "kon", "ILP": "int", "MILP_x1_int_x2_kon": "int", "MILP_x1_kon_x2_int": "kon"}
        values_2 = {"LP": "kon", "ILP": "int", "MILP_x1_int_x2_kon": "kon", "MILP_x1_kon_x2_int": "int"}
        m9 = ui.modal(
            ui.row(
                ui.column(4, ui.HTML("<b>Wertebereich x1</b>")),
                ui.column(3, ui.HTML(
                    f'aktuell:<b>{values_1.get(art_of_optimization_reactive.get(), "nicht einheitlich oder nichts ausgewählt")}</b>')),
                ui.column(2, ui.HTML("wählen:")),
                ui.column(3, ui.input_select(
                    "select_x1_wertebreich_for_all",
                    None,
                    choices={"kon": "kon", "int": "int"}),
                          ),
            ),
            ui.HTML("<br><br>"),
            ui.row(
                ui.column(4, ui.HTML("<b>Wertebereich x2</b>")),
                ui.column(3, ui.HTML(
                    f'aktuell:<b>{values_2.get(art_of_optimization_reactive.get(), "nicht einheitlich oder nichts ausgewählt")}</b>')),
                ui.column(2, ui.HTML("wählen:")),
                ui.column(3, ui.input_select(
                    "select_x2_wertebreich_for_all",
                    None,
                    choices={"kon": "kon", "int": "int"}),
                          ),
            ),

            footer=ui.div(
                ui.input_action_button(id="cancel_button_9", label="Abbrechen"),
                ui.input_action_button(id="submit_button_9", label="Übermitteln"),
            ),
            title="Change Wertebereich x1 and x2 for all",
            easy_close=False,
            style="width: 100%;"
        )
        ui.modal_show(m9)


    @reactive.effect
    @reactive.event(input.submit_button_9)
    def set_x1_and_x2_all():

        x1_wertebreich = input.select_x1_wertebreich_for_all()
        x2_wertebreich = input.select_x2_wertebreich_for_all()

        update_zielfunktion_reactive_list = zielfunktion_reactive_list.get().copy()
        update_nebenbedingung_reactive_list = nebenbedingung_reactive_list.get().copy()
        #update_selected_zielfunktion_reactive_list = selected_zielfunktion_reactive_list.get().copy()
        #update_selected_nebenbedingungen_reactive_list = selected_nebenbedingungen_reactive_list.get().copy()

        for zielfunction in update_zielfunktion_reactive_list:
            zielfunction[2] = x1_wertebreich
            zielfunction[4] = x2_wertebreich
        zielfunktion_reactive_list.set(update_zielfunktion_reactive_list)

        #for zielfunction in update_selected_zielfunktion_reactive_list:
            #zielfunction[2] = x1_wertebreich
            #zielfunction[4] = x2_wertebreich
        selected_zielfunktion_reactive_list.set([])

        for restriction in update_nebenbedingung_reactive_list:
            restriction[2] = x1_wertebreich
            restriction[4] = x2_wertebreich
        nebenbedingung_reactive_list.set(update_nebenbedingung_reactive_list)

        #for restriction in update_selected_nebenbedingungen_reactive_list:
            #restriction[2] = x1_wertebreich
            #restriction[4] = x2_wertebreich
        selected_nebenbedingungen_reactive_list.set([])

        ui.update_selectize("selectize_nebenbedingung", choices=nebenbedingung_dict.get(),
                            selected=[])
        ui.update_select("select_target_function", choices=target_function_dict.get(), selected=[])

        notification_popup("Wertebereich für x1 und / oder x2 erfolgreich geändert.")







        ui.modal_remove()

    @reactive.effect
    @reactive.Calc
    def set_wertebreich_listener():
        if zielfunktion_reactive_list.get() and nebenbedingung_reactive_list.get():
            ui.update_action_button("x1_x2_Wertebereich_setzen", disabled=False)
        else:
            ui.update_action_button("x1_x2_Wertebereich_setzen", disabled=True)




    def check_x1_x2():

        typ_all_x1_neben = None
        typ_all_x1_target = None
        typ_all_x2_neben = None
        typ_all_x2_target = None

        if selected_zielfunktion_reactive_list.get():
            selected_zielfunktion = None
            for entry in zielfunktion_reactive_list.get():
                if entry[0] == input.select_target_function():
                    selected_zielfunktion = entry
            typ_all_x1_target = selected_zielfunktion[2]
            typ_all_x2_target = selected_zielfunktion[4]


        if selected_nebenbedingungen_reactive_list.get():
            selected_nebenbedingungen = []
            for entry in nebenbedingung_reactive_list.get():
                if entry[0] in input.selectize_nebenbedingung():
                    selected_nebenbedingungen.append(entry)

            typ_all_x1_neben = [entry[2] for entry in selected_nebenbedingungen]
            typ_all_x2_neben = [entry[4] for entry in selected_nebenbedingungen]


        if not selected_zielfunktion_reactive_list.get():
            return [2, 2, "unselected_zielfunktion"]
        if  not selected_nebenbedingungen_reactive_list.get():
            return [2, 2, "unselected_nebenbedingungen"]

        else:
            typ_all_x1 = typ_all_x1_neben + [typ_all_x1_target]
            typ_all_x2 = typ_all_x2_neben + [typ_all_x2_target]

            print(f"typ_x1: {typ_all_x1}")
            print(f"typ_x2: {typ_all_x2}")

            return [len(set(typ_all_x1)), len(set(typ_all_x2)), "alles_selected"]