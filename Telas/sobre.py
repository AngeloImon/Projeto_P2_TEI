from nicegui import ui
from dotenv import load_dotenv


# About page
@ui.page("/about")
def sobre():
    with ui.header().classes("bg-blue-800 text-white p-4 shadow-md"):
        with ui.row().classes("items-center gap-4"):
            ui.link("Home", "/").classes("text-lg")
            ui.link("Login", "/login").classes("text-lg")

    with ui.column().classes("mx-auto mt-8 p-8 max-w-4xl"):
        ui.label("Bem-vindo ao Sobre").classes("text-3xl font-bold mb-4")
        ui.markdown(
            """
        **Aplicativos de Estudos NOME GENERICO**
        Neste aplicativo voce ira aprender!!!!!
        """
        )
