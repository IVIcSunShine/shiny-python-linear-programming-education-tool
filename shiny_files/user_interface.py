from shiny import ui

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

        ui.nav_panel("Linear Programming and sensitivity analysis",
                     ui.layout_sidebar(
                         ui.sidebar(
                             ui.row(
                                 ui.card(
                                     ui.tooltip(
                                         ui.card_header("User inputs"),
                                         "In this section you can enter your objective function and constraints."),
                                     ui.tooltip(
                                         ui.HTML(
                                             '<div style="text-align: center;"><b>Non-negativity required</b></div>'),
                                         "All inputs must be non-negative."),
                                     ui.card(
                                         ui.tooltip(
                                             ui.input_action_button(id="btn_enter_obj_func",
                                                                    label="Enter objective function",
                                                                    class_="background-color-White"
                                                                    ),
                                             "Enter your objective function. The objective function is the function that is to be optimised."),
                                         ui.tooltip(
                                             ui.input_action_button(id="btn_change_obj_func",
                                                                    label="Change objective function",
                                                                    disabled=True,
                                                                    class_="background-color-White"
                                                                    ), "Change the objective function."),
                                         ui.tooltip(
                                             ui.input_action_button(id="btn_delete_obj_func",
                                                                    label="Delete objective function",
                                                                    disabled=True,
                                                                    class_="background-color-White"
                                                                    ), "Delete the objective function."),
                                         class_="background-color-LightSkyBlue"
                                     ),
                                     ui.card(
                                         ui.tooltip(
                                             ui.input_action_button(id="btn_enter_constraint",
                                                                    label="Enter constraint",
                                                                    disabled=False,
                                                                    class_="background-color-White"
                                                                    ),
                                             "Enter your constraints. Constraints are functions that restrict the target function."),
                                         ui.tooltip(
                                             ui.input_action_button(id="btn_change_constraint",
                                                                    label="Change constraint",
                                                                    disabled=True,
                                                                    class_="background-color-White"
                                                                    ),
                                             "Change the constraints."),
                                         ui.tooltip(
                                             ui.input_action_button(id="btn_delete_constraint",
                                                                    label="Delete constraint",
                                                                    disabled=True,
                                                                    class_="background-color-White"
                                                                    ),
                                             "Delete the constraints."),
                                         class_="background-color-LightSkyBlue"
                                     ),
                                     ui.card(
                                         ui.tooltip(
                                             ui.input_action_button(id="set_x1_x2_value_range",
                                                                    label="Set value range for x1 and x2",
                                                                    disabled=True,
                                                                    class_="background-color-White"
                                                                    ),
                                             "Change the value range of x1 and x2 at once instead of individually using the ‘change’ buttons."),
                                         class_="background-color-LightSkyBlue"
                                     ),
                                     class_="background-color-LightSkyBlue1"

                                 ),
                             ),
                             ui.card(
                                 ui.tooltip(
                                     ui.card_header("Main functions"),
                                     "Further options are provided in this panel."),
                                 ui.card(
                                     ui.tooltip(
                                     ui.card_header("Calculations"),
                                         "Select the type of calculation. NOTE: Sensitivity analysis is only possible after linear optimization."),
                                     ui.tooltip(
                                         ui.input_action_button(id="btn_lin_opt",
                                                                label="Linear optimization",
                                                                disabled=True,
                                                                class_="background-color-White"
                                                                ),
                                         "Start the linear optimization for your problem."),
                                     ui.tooltip(
                                         ui.input_action_button(id="btn_sens_ana",
                                                                label="Sensitivity analysis",
                                                                disabled=True,
                                                                class_="background-color-White"
                                                                ),
                                         "Start the sensitivity analysis for your problem."),
                                     class_="background-color-LightSkyBlue"

                                 ),
                                 ui.card(
                                     ui.card_header("Extras"),
                                     ui.tooltip(
                                         ui.input_action_button(id="btn_save_graph",
                                                                label="Save graph as PNG",
                                                                disabled=True,
                                                                class_="background-color-White"
                                                                ),
                                         "Save the graph as a png file."),
                                     ui.tooltip(
                                         ui.input_action_button(id="btn_import_export",
                                                                label="Import & export",
                                                                disabled=False,
                                                                class_="background-color-White"
                                                                ),
                                         "Import or export your data using the LP format."),

                                     class_="background-color-LightSkyBlue"
                                 ),
                                 class_="background-color-LightSkyBlue1"
                             ),
                             ui.card(
                                 ui.card(
                                     ui.tooltip(
                                     ui.input_action_button(id="btn_reset",
                                                            label="Reset all",
                                                            disabled=False,
                                                            class_="background-color-White"
                                                            ),
                                        "Reset all entries."),
                                     class_="background-color-LightSkyBlue"
                                 ),
                                 class_="background-color-LightSkyBlue1"
                             ),
                             ui.HTML('<div style="text-align: center;"><b>OptiSense Version 1.0</b></div>'),
                             ui.HTML('<div style="text-align: center;"><b>by Peter Oliver Ruhland</b></div>'),

                             width="20%"),

                         ui.layout_column_wrap(
                             ui.card(
                                 ui.tooltip(
                                     ui.card_header("Transmitted data"),
                                     "Your transmitted data is displayed in this section. You can use this data for linear optimization and the following sensitivity analysis."),
                                 ui.layout_column_wrap(
                                     ui.card(
                                         ui.tooltip(
                                             ui.card_header("Overview of the functions"),
                                             "This panel displays all the functions entered for your overview."),
                                         ui.card(
                                             ui.HTML("<b>Objective function(s):</b>"),
                                             ui.output_ui("txt_obj_func"),
                                         ),

                                         ui.card(
                                             ui.HTML("<b>Constraint(s):</b>"),
                                             ui.output_ui("txt_constraint"),
                                         ),
                                         class_="background-color-LightSkyBlue"
                                     ),
                                     ui.card(
                                         ui.tooltip(
                                             ui.card_header("Selecting the functions"),
                                             "In this panel, select the functions you want to use for linear optimization and sensitivity analysis."),
                                         ui.input_select(
                                             "select_obj_func",
                                             "Choose an objective function:",
                                             choices=[],

                                         ),
                                         ui.input_selectize(
                                             "selectize_constraints",
                                             "Choose constraint(s):",
                                             choices=[],

                                             multiple=True,
                                         ),

                                         ui.HTML("<br><br>"),
                                         class_="background-color-LightSkyBlue"
                                     ),
                                     ui.card(
                                         ui.tooltip(
                                             ui.card_header("Overview of the value ranges"),
                                             "This panel shows the value ranges of the individual functions and the resulting problem type per function."),
                                         ui.card(
                                             ui.output_data_frame("df_output_value_ranges"),
                                         ),
                                         class_="background-color-LightSkyBlue"
                                     ),
                                     ui.card(
                                         ui.tooltip(
                                             ui.card_header("Linear Programming - Information"),
                                             "This panel displays the type of linear programming based on the transmitted data and the corresponding numerical range."),
                                         ui.card(
                                             ui.output_ui("txt_lin_prog_type"),
                                         ),
                                         class_="background-color-LightSkyBlue"
                                     ),
                                     width=1 / 2,
                                 ),

                                 class_="background-color-LightSkyBlue1"
                             ),
                             ui.card(
                                 ui.tooltip(
                                     ui.card_header("Graphical solution"),
                                     "This panel displays the graph with all the data transmitted to it. The x1 and x2 axes update dynamically."),
                                 ui.card(
                                     ui.output_plot("plot_output_graph"),
                                     class_="background-color-LightSkyBlue"
                                 ),
                                 class_="background-color-LightSkyBlue1"
                             ),

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
                                         ui.card(
                                             ui.output_data_frame("lp_results_df"),
                                         ),
                                         class_="background-color-LightSkyBlue"
                                     )),
                                     ui.column(8, ui.card(
                                         ui.tooltip(
                                             ui.card_header("sensitivity analysis"),
                                             "Lesen Sie die Ergebnisse der Sensitivitätsanalyse ab."),
                                         ui.tooltip(
                                         ui.HTML("<b>""Ausschöpfen der Nebenbedingungen und Slack""</b>"),
                                             "Zeigt, wie stark die Nebenbedingungen im optimalen Punkt ausgelastet sind. Der “Slack” gibt an, wie viel von der Kapazität ungenutzt bleibt."),
                                         ui.card(
                                             ui.output_data_frame("sens_ana_ausschöpfen_df"),
                                         ),
                                         ui.tooltip(
                                         ui.HTML("<b>""Schattenpreis""</b>"),
                                             "Der Schattenpreis gibt an, wie stark sich der Zielfunktionswert verbessert, wenn eine Restriktion um eine Einheit gelockert wird. Ein Wert von 0 bedeutet, dass die Restriktion keinen Einfluss auf die Zielfunktion hat."),
                                         ui.card(
                                             ui.output_data_frame("sens_ana_schattenpreis_df"),
                                         ),
                                         ui.tooltip(
                                         ui.HTML("<b>""Koeffizientenänderung""</b>"),
                                             "Beschreibt, in welchem Bereich die Zielfunktion oder Restriktionen geändert werden können, ohne dass die optimale Lösung ungültig wird."),
                                         ui.card(
                                             ui.output_data_frame("sens_ana_coeff_change_df"),
                                         ),
                                         class_="background-color-LightSkyBlue"
                                     )),
                                 ),
                                 class_="background-color-LightSkyBlue1"
                             ),

                             style="height: 34vh;",
                             width=1 / 2,
                         ),

                     ),

                     ),
        ui.nav_panel("How to use",

                     ui.layout_sidebar(
                         ui.sidebar("Sidebar", bg="#f8f8f8"),
                         "Main content",
                     ),

                     "Page C content"),
        ui.nav_panel("Über", "Page C content"),

        title="OptiSense",
        id="page",

        bg="#B0E2FF"
    ),
    style="height: 100vh;",
    class_="background-color-SnowGrey"
)
