from shiny import render, reactive, ui


def server(input, output, session):

    @reactive.effect
    @reactive.event(input.button_zfkt_eingeben)
    def _():
        m = ui.modal(
            "This is a somewhat important message.",
            title="Somewhat important message",
            easy_close=True,
        )
        ui.modal_show(m)
