from shiny import ui
#from server import target_function_dict
#from server import nebenbedingung_dict

app_ui = ui.page_fillable( ui.page_navbar(
    ui.nav_panel("Lineare Optimierung",
                 ui.layout_sidebar(
                     ui.sidebar(
                         ui.row(
                             ui.card(
                                 ui.card_header("User Inputs"),
                                 ui.card(
                                     ui.input_action_button(id="button_zfkt_eingeben",
                                                            label="Zielfunktion eingeben"
                                                            ),
                                     ui.input_action_button(id="action_button_zielfunktion_ändern",
                                                            label="Zielfunktion ändern",
                                                            disabled=True
                                                            ),
                                     ui.input_action_button(id="action_button_zielfunktion_löschen",
                                                            label="Zielfunktion löschen",
                                                            disabled=True
                                                            ),
                                 ),
                                 ui.card(
                                     ui.input_action_button(id="action_button_restriktionen_eingeben",
                                                            label="Restriktionen eingeben",
                                                            disabled=False
                                                            ),
                                     ui.input_action_button(id="action_button_restriktionen_ändern",
                                                            label="Restriktionen ändern",
                                                            disabled=True
                                                            ),
                                     ui.input_action_button(id="action_button_restriktionen_löschen",
                                                            label="Restriktionen löschen",
                                                            disabled=True
                                                            ),
                                 ),
                             ),
                         ),
                         ui.card(
                             ui.card_header("Programm Options"),
                         ui.card(
                                ui.card_header("Calculations"),
                             ui.input_action_button(id="lineare_optimierung_button",
                                                    label="linear optimization",
                                                    disabled=True
                                                    ),
                             ui.input_action_button(id="Sensitivity_analysis_button",
                                                    label="sensitivity analysis",
                                                    disabled=True
                                                    )

                         ),
                         ui.card(
                             ui.card_header("Extras"),
                             ui.input_action_button(id="save_graph_png",
                                                    label="save graph as png",
                                                    disabled=True
                                                    ),
                             #ui.input_action_button(id="import_export_button",
                                    #                label="import / export",
                                     #               disabled=True
                                       #             ),
                         ),
                         ),

                         width="20%"),
                     #ui.layout_columns(
                        ui.layout_column_wrap(
                         ui.card(
                             ui.card_header("Übermittelte Daten"),
                             ui.layout_column_wrap(
                                 ui.card(
                                     ui.card_header("Übersicht der Funktionen"),
                                     ui.HTML("<b>""Zielfunktion:""</b>"),
                                     ui.output_ui("zfkt_text"),
                                     ui.br(),
                                     ui.HTML("<b>""Restriktionen:""</b>"),
                                     ui.output_ui("rest_text"),
                                 ),
                                 ui.card(
                                     ui.card_header("Auswahl der Funktionen"),
                                     ui.input_select(
                                         "select_target_function",
                                         "Select an Zielfunktion:",
                                         choices=[],
                                         #choices=target_function_dict,
                                     ),
                                     ui.input_selectize(
                                         "selectize_nebenbedingung",
                                         "Select Nebenbedingungen:",
                                         choices=[],
                                         #choices=nebenbedingung_dict,
                                         multiple=True,
                                     ),
                                     ui.HTML("<br>""<br>")
                                 ),
                                 ui.card(
                                     ui.card_header("Übersicht der Zahlenbereiche"),
                                     ui.output_data_frame("zahlenbereiche_df_output")
                                 ),
                                 ui.card(
                                     ui.card_header("Lineare Optimierung - Info"),
                                     ui.output_ui("finale_auswahl_text")
                                 ),
                                 width=1 / 2,
                             ),
                                #style="height: 200px;",
                         ),
                         ui.card(
                             ui.card_header("Output"),

                             ui.output_plot("optimierung_plot")
                         ),
                            #height="66%",
                            style="height: 66vh;",
                            width=1 / 2,
                        ),
                         ui.layout_column_wrap(
                             ui.card(ui.card_header("Beschreibung"),
                                     ui.output_ui("beschreibung_text")
                                     ),
                             ui.card(ui.card_header("Ergebnisse"),
                                     ui.row(
                                     ui.column( 4,ui.card(ui.card_header("linear optimization"),
                                                          ui.output_data_frame("lp_results_df"),
                                                          )),
                                     ui.column(8, ui.card(ui.card_header("sensitivity analysis"))),
                                     ),
                                     ),
                             #height="33%",
                             style="height: 34vh;",
                             width=1 / 2,
                         ),


                     #)
                 ),
                 ),
    ui.nav_panel("How to use", "Page C content"),
    ui.nav_panel("Über", "Page C content"),
    title="OptiSense",
    id="page",
    # ui.input_slider("n", "Number of bins", 10, 100, 50),
    # ui.output_plot("hist"),
),
style="height: 100vh;"
)
