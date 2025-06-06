from nicegui import ui
from Telas.login import create_login_page, create_signup_page
from Telas.dashboard import dashboard
from Telas.sobre import sobre
from Telas.meus_planos import meus_planos


# Register all page routes first
create_signup_page()
create_login_page()
dashboard()
sobre()
meus_planos()

# Home page
@ui.page("/")
def home():
    #Header
    with ui.header().classes("bg-gradient-to-r from-blue-700 to-blue-900 text-white p-4 shadow-lg"):
        with ui.row().classes("items-center justify-between w-full px-4"):
            ui.label("📘 Meu App de Estudos").classes("text-xl font-bold")
            with ui.row().classes("gap-6"):
                ui.link("🔑 Login", "/login").classes("text-lg hover:underline")
                ui.link("ℹ️ Sobre", "/about").classes("text-lg hover:underline")
            


    #Conteúdo principal
    with ui.card().classes("mx-auto mt-10 p-8 max-w-3xl shadow-lg bg-white"):
        ui.label("🎓 Bem-vindo ao Sistema de Estudos").classes("text-3xl font-bold text-blue-800 mb-4")
        ui.markdown(
            """
            **Aplicação desenvolvida com NiceGUI**  
            - Acesse o sistema pelo link de **Login**  
            - Navegue entre as páginas como **Dashboard**, **Planos**, e **Mais**  
            - Organize seus estudos com praticidade
            """
        ).classes("text-lg")


        ui.button("➡️ Criar uma Conta", on_click=lambda: ui.navigate.to('/signup')).classes("mt-6 bg-blue-600 text-white hover:bg-blue-700 px-4 py-2 rounded")

        ui.button("➡️ Acessar Login", on_click=lambda: ui.navigate.to('/login')).classes("mt-6 bg-blue-600 text-white hover:bg-blue-700 px-4 py-2 rounded")


# Start the app with reload enabled (for development)
ui.run(title="Meu App", favicon="🔒", reload=True, port=8080)  # Enable hot-reloading