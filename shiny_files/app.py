import os
from shiny import App
from user_interface import app_ui
from server import server

app = App(app_ui, server, static_assets= os.path.join(os.path.dirname(__file__), "www"))

if __name__ == "__main__":
    app.run()
