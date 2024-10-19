from shiny import render, reactive, ui



def server(input, output, session):

    restrictions = []

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
            title="Zielfunktion",
            easy_close=True,
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
            title="Restriktion",
            easy_close=True,
        )
        ui.modal_show(m2)












    @reactive.Calc
    def reactive_txt():
        if input.zfkt_x1() and input.zfkt_x2():
             return f"Z={input.zfkt_x1()}*x1+{input.zfkt_x2()}*x2"
        else:
            return ""

    @output
    @render.text
    def zfkt_text():
        return reactive_txt()



    @reactive.Calc
    def reactive_txt_rest():
        if input.rest_x1() and input.rest_x2():
             restrictions.append([input.rest_x1(), input.rest_x2()])
             return f"R1={input.rest_x1()}*x1+{input.rest_x2()}*x2"
        else:
            return ""

    @output
    @render.text
    def rest_text():
        return reactive_txt_rest()
