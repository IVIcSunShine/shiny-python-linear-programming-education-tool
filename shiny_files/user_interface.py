from shiny import ui

# from server import target_function_dict
# from server import nebenbedingung_dict

app_ui = ui.page_fillable(
    ui.tags.style("""
    .background-color-LightSkyBlue1 {
        background-color: #CCECFF;
    }
    .background-color-LightSkyBlue {
        background-color: #B0E2FF;
    }
    .background-color-White {
        background-color: #FFFFFF;
    }
    .background-color-SnowGrey {
        background-color: #FFF2E6;
    }
"""),

    ui.page_navbar(

        ui.nav_panel("Lineare Optimierung",
                     ui.layout_sidebar(
                         ui.sidebar(
                             ui.row(
                                 ui.card(
                                     ui.tooltip(
                                         ui.card_header("User Inputs"),
                                         "In dieser Rubrik können Sie Ihre Zielfunktion und Restriktionen eingeben."),
                                     ui.tooltip(
                                     ui.HTML('<div style="text-align: center;"><b>Nicht-Negativität vorausgesetzt</b></div>'),
                                         "Alle Eingeben müssen nicht-negativ sein."),
                                     ui.card(
                                         ui.tooltip(
                                             ui.input_action_button(id="button_zfkt_eingeben",
                                                                    label="Zielfunktion eingeben",
                                                                    class_="background-color-White"
                                                                    ),
                                             "Geben Sie Ihre Zielfunktion ein. Die Zielfunktion ist die Funktion, die optimiert werden soll."),
                                         ui.tooltip(
                                             ui.input_action_button(id="action_button_zielfunktion_ändern",
                                                                    label="Zielfunktion ändern",
                                                                    disabled=True,
                                                                    class_="background-color-White"
                                                                    ), "Ändern Sie die Zielfunktion."),
                                         ui.tooltip(
                                             ui.input_action_button(id="action_button_zielfunktion_löschen",
                                                                    label="Zielfunktion löschen",
                                                                    disabled=True,
                                                                    class_="background-color-White"
                                                                    ), "Löschen Sie die Zielfunktion."),
                                         class_="background-color-LightSkyBlue"
                                     ),
                                     ui.card(
                                         ui.tooltip(
                                             ui.input_action_button(id="action_button_restriktionen_eingeben",
                                                                    label="Restriktionen eingeben",
                                                                    disabled=False,
                                                                    class_="background-color-White"
                                                                    ),
                                             "Geben Sie Ihre Restriktionen ein. Restriktionen sind Nebenbedingungen, die die Zielfunktion einschränken."),
                                         ui.tooltip(
                                             ui.input_action_button(id="action_button_restriktionen_ändern",
                                                                    label="Restriktionen ändern",
                                                                    disabled=True,
                                                                    class_="background-color-White"
                                                                    ),
                                             "Ändern Sie die Restriktionen."),
                                         ui.tooltip(
                                             ui.input_action_button(id="action_button_restriktionen_löschen",
                                                                    label="Restriktionen löschen",
                                                                    disabled=True,
                                                                    class_="background-color-White"
                                                                    ),
                                             "Löschen Sie die Restriktionen."),
                                         class_="background-color-LightSkyBlue"
                                     ),
                                     class_="background-color-LightSkyBlue1"
                                 ),
                             ),
                             ui.card(
                                 ui.tooltip(
                                     ui.card_header("Programm Options"),
                                     "In dieser Kachel werden weiterführende Optionen bereitgestellt."),
                                 ui.card(
                                     ui.card_header("Calculations"),
                                     ui.tooltip(
                                         ui.input_action_button(id="lineare_optimierung_button",
                                                                label="linear optimization",
                                                                disabled=True,
                                                                class_="background-color-White"
                                                                ),
                                         "Starten Sie die lineare Optimierung für Ihr Problem."),
                                     ui.tooltip(
                                         ui.input_action_button(id="Sensitivity_analysis_button",
                                                                label="sensitivity analysis",
                                                                disabled=True,
                                                                class_="background-color-White"
                                                                ),
                                         "Starten Sie die Sensitivitätsanalyse für Ihr Problem."),
                                     class_="background-color-LightSkyBlue"

                                 ),
                                 ui.card(
                                     ui.card_header("Extras"),
                                     ui.tooltip(
                                         ui.input_action_button(id="save_graph_png",
                                                                label="save graph as png",
                                                                disabled=True,
                                                                class_="background-color-White"
                                                                ),
                                         "Speichern Sie den Graphen als png-Datei ab."),
                                     ui.tooltip(
                                     ui.input_action_button(id="import_export_button",
                                                            label="import / export",
                                                            disabled=True,
                                                            class_="background-color-White"
                                                            ),
                                         "Importieren oder exportieren Sie Ihre Daten mithilfe des LP-Formates."),
                                     # ui.input_action_button(id="import_export_button",
                                     #                label="import / export",
                                     #               disabled=True
                                     #             ),
                                     class_="background-color-LightSkyBlue"
                                 ),
                                 class_="background-color-LightSkyBlue1"
                             ),

                             width="20%"),
                         # ui.layout_columns(
                         ui.layout_column_wrap(
                             ui.card(
                                 ui.tooltip(
                                     ui.card_header("Übermittelte Daten"),
                                     "In dieser Rubtik werden Ihre übermittelten Daten angezeigt. Diese Daten können Sie für die lineare Optimierung verwenden."),
                                 ui.layout_column_wrap(
                                     ui.card(
                                         ui.tooltip(
                                             ui.card_header("Übersicht der Funktionen"),
                                             "Diese Kachel stellt alle eingegebenen Funktionen zu Ihrer Übersicht dar."),
                                         ui.card(
                                             ui.HTML("<b>""Zielfunktion:""</b>"),
                                             ui.output_ui("zfkt_text"),
                                         ),
                                         # ui.br(),
                                         ui.card(
                                             ui.HTML("<b>""Restriktionen:""</b>"),
                                             ui.output_ui("rest_text"),
                                         ),
                                         class_="background-color-LightSkyBlue"
                                     ),
                                     ui.card(
                                         ui.tooltip(
                                             ui.card_header("Auswahl der Funktionen"),
                                             "In dieser Kacel wählen Sie die Funktionen aus, die Sie für die lineare Optimierung verwenden möchten."),
                                         ui.input_select(
                                             "select_target_function",
                                             "Select an Zielfunktion:",
                                             choices=[],
                                             # choices=target_function_dict,
                                         ),
                                         ui.input_selectize(
                                             "selectize_nebenbedingung",
                                             "Select Nebenbedingungen:",
                                             choices=[],
                                             # choices=nebenbedingung_dict,
                                             multiple=True,
                                         ),
                                         #ui.row(
                                          #   ui.column(6,
                                         #ui.input_action_button(id="create_graph_button",
                                          #                      label="submit",
                                           #                     disabled=True,
                                            #                    class_="background-color-White"
                                             #                   )),
                                              #  ui.column(6,
                                         #ui.input_action_button(id="unload_graph_button",
                                          #                      label="unload",
                                           #                     disabled=True,
                                            #                    class_="background-color-White"
                                             #                   ))
                                        # ),
                                         ui.HTML("<br>""<br>"),
                                         class_="background-color-LightSkyBlue"
                                     ),
                                     ui.card(
                                         ui.tooltip(
                                             ui.card_header("Übersicht der Zahlenbereiche"),
                                             "Diese Kachel gibt die Eigenschaften der Funktionen wieder."),
                                         ui.card(
                                             ui.output_data_frame("zahlenbereiche_df_output"),
                                         ),
                                         class_="background-color-LightSkyBlue"
                                     ),
                                     ui.card(
                                         ui.tooltip(
                                             ui.card_header("Lineare Optimierung - Info"),
                                             "In dieser Kachel wird die Art der lineare Optimierung basierend auf den übermittelten Daten und der dazu passende Zahlenbereich angezeigt."),
                                         ui.card(
                                             ui.output_ui("finale_auswahl_text"),
                                         ),
                                         class_="background-color-LightSkyBlue"
                                     ),
                                     width=1 / 2,
                                 ),
                                 # style="height: 200px;",
                                 class_="background-color-LightSkyBlue1"
                             ),
                             ui.card(
                                 ui.tooltip(
                                     ui.card_header("Output"),
                                     "Diese Kachel gibt den Graphen mit allen an diesen übermittelten Daten aus. Die x1- sowie die x2-Achse passen sich dynamisch an."),
                                 ui.card(
                                     ui.output_plot("optimierung_plot"),
                                     class_="background-color-LightSkyBlue"
                                 ),
                                 class_="background-color-LightSkyBlue1"
                             ),
                             # height="66%",
                             style="height: 66vh;",
                             width=1 / 2,
                         ),
                         ui.layout_column_wrap(
                             ui.card(
                                 ui.tooltip(
                                     ui.card_header("Beschreibung"),
                                     "In dieser Rubrik werden Eigenschaften der Funktionen bezüglich des Graphen und Ergebnisbeschreibungen bereitgestellt."),
                                 ui.card(
                                     ui.card(
                                         ui.output_ui("beschreibung_text"),
                                     ),
                                     class_="background-color-LightSkyBlue"
                                 ),
                                 class_="background-color-LightSkyBlue1"
                             ),
                             ui.card(
                                 ui.tooltip(
                                     ui.card_header("Ergebnisse"),
                                     "In dieser Rubrik werden die Ergebnisse der linearen Optimierung und Sensitivitätsanalyse tabellarisch dargestellt."),
                                 ui.row(
                                     ui.column(4, ui.card(
                                         ui.tooltip(
                                             ui.card_header("linear optimization"),
                                             "Lesen Sie die Ergebnisse der linearen Optimierung ab mit den optimalen Werten für x1 und x2 und dem Ergebnis der Zielfunktion ab."),
                                         ui.output_data_frame("lp_results_df"),
                                         class_="background-color-LightSkyBlue"
                                     )),
                                     ui.column(8, ui.card(
                                         ui.tooltip(
                                             ui.card_header("sensitivity analysis"),
                                             "Lesen Sie die Ergebnisse der Sensitivitätsanalyse ab."),
                                         class_="background-color-LightSkyBlue"
                                     )),
                                 ),
                                 class_="background-color-LightSkyBlue1"
                             ),
                             # height="33%",
                             style="height: 34vh;",
                             width=1 / 2,
                         ),

                         # )
                     ),

                     ),
        ui.nav_panel("How to use", "Page C content"),
        ui.nav_panel("Über", "Page C content"),

        title="OptiSense",
        id="page",
        # ui.input_slider("n", "Number of bins", 10, 100, 50),
        # ui.output_plot("hist"),
        bg="#B0E2FF"
    ),
    style="height: 100vh;",
    class_="background-color-SnowGrey"
)
