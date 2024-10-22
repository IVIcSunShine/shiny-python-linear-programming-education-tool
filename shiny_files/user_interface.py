from shiny import ui
import numpy as np

app_ui = ui.page_navbar(
    ui.nav_panel("Lineare Optimierung",
                 ui.layout_sidebar(
                     ui.sidebar(
                         ui.row(
                             ui.card(
                                 ui.card_header("User Inputs"),
                                 ui.input_action_button(id="button_zfkt_eingeben",
                                                        label="Zielfunktion eingeben"
                                                        ),
                                 ui.input_action_button(id="action_button_zielfunktion_aendern",
                                                        label="Zielfunktion aendern",
                                                        disabled=True
                                                        ),
                                 ui.input_action_button(id="action_button_zielfunktion_loeschen",
                                                        label="Zielfunktion loeschen",
                                                        disabled=True
                                                        ),
                                 ui.input_action_button(id="action_button_restriktionen_eingeben",
                                                        label="Restriktionen eingeben",
                                                        disabled=False
                                                        ),
                                 ui.input_action_button(id="action_button_restriktionen_ändernLöschen",
                                                        label="Restriktionen ändern / löschen",
                                                        disabled=True
                                                        ),
                             ),
                         ),
                         ui.row(
                             ui.card(
                                 ui.card_header("Import / Export / Save png")
                             )
                         ),
                         width="20%"),
                     ui.layout_columns(
                         ui.card(
                             ui.card_header("Übermittelte Daten"),
                             ui.layout_columns(
                                 ui.column(12,
                                           ui.card(
                                               ui.card_header("Funktionen"),
                                               ui.HTML("<b>""Zielfunktion:""</b>"),
                                               ui.output_text("zfkt_text"),
                                               ui.br(),
                                               ui.HTML("<b>""Restriktionen:""</b>"),
                                               ui.output_text("rest_text"),
                                           )),
                                 ui.column(12,
                                           ui.card(
                                               ui.card_header("Auswahl"),
                                           ),
                                           ),
                             ),
                         ),
                         ui.card(
                             ui.card_header("Output"),
                             ui.p("BLUPBLUP"),
                             ui.output_plot("optimierung_plot")
                         ),
                     )
                 ),
                 ),
    ui.nav_panel("Sensitivitätsanalyse", "Page B content"),
    ui.nav_panel("How to use", "Page C content"),
    ui.nav_panel("Über", "Page C content"),
    title="OptiSense",
    id="page",
    # ui.input_slider("n", "Number of bins", 10, 100, 50),
    # ui.output_plot("hist"),
)
