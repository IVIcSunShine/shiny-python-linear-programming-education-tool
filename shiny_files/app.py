from shiny import App
from user_interface import app_ui
from server import server



app = App(app_ui, server)

if __name__ == "__main__":
    app.run()