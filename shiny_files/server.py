from shiny import render, reactive, ui
import matplotlib.pyplot as plt
from functions import *

ausgabe_rest = ""
restrictions = []
zfkt = []
zielfunktion_name = ""




def server(input, output, session):

    global ausgabe_rest
    global restrictions
    global zfkt
    global zielfunktion_name


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
                ui.modal_button(id="cancel_button", label="Abbrechen"),
                ui.modal_button(id="submit_button", label="Übermitteln"),
            ),
            title="Zielfunktion",
            easy_close=False,
        )
        ui.modal_show(m)


        @reactive.Effect
        @reactive.event(input.cancel_button or input.submit_button or input.cancel_button_2 or input.submit_button_2)
        def close_modal_cancel():
            ui.modal_remove()

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
                ui.modal_button(id="cancel_button_2", label="Abbrechen"),
                ui.modal_button(id="submit_button_2", label="Übermitteln"),
            ),
            title="Restriktion",
            easy_close=False,
        )
        ui.modal_show(m2)


    @reactive.effect
    @reactive.event(input.submit_button)
    def create_function():
        global zielfunktion_name
        zielfunktion_name = input.zfkt_name()
        zielfunktion_name = TargetFunctions(input.zfkt_name(), input.zfkt_x1(), input.zfkt_select_attribute_1(), input.zfkt_x2(), input.zfkt_select_attribute_2(), input.zfkt_select_minmax())



    @output
    @render.text
    def zfkt_text():
        return reactive_txt()


    @reactive.Calc
    def reactive_txt():
        if len(Functions.function_list) != 0:
            return TargetFunctions(zielfunktion_name).as_text()
        else:
            return ""
















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























    @output
    @render.plot()
    def optimierung_plot():
        # Neue Werte für die Linie, die durch (4,0) und (0,6) geht
        x_values_new = [0, 4]
        y_values_new = [6, 0]

        # Erstellen der neuen Grafik
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.plot(x_values_new, y_values_new, label="Linie durch (4,0) und (0,6)")

        # Achsenbeschriftungen und Legende
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_xlabel("x-Achse")
        ax.set_ylabel("y-Achse")
        ax.legend()

        # Gitter und Grafik zurückgeben
        ax.grid(True)
        return fig

