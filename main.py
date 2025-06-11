import os
from nicegui import ui
from dotenv import load_dotenv

# Importa as páginas
from Telas.login import login
from Telas.signup import signup
from Telas.dashboard import dashboard
from Telas.sobre import sobre
from Telas.meus_planos import meus_planos
from Telas.novo_plano import novo_plano
from Telas.novo_plano_dias_semana import novo_plano_dias_semana
from Telas.novo_plano_calendario import novo_plano_calendario

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Registra as páginas de cadastro e login
signup()
login()

# --- Cabeçalho padronizado para a página inicial ---
def cabecalho_padrao():
    with ui.header().classes(
        "bg-gradient-to-r from-blue-700 to-blue-900 text-white p-4 shadow-lg"
    ):
        with ui.row().classes("items-center justify-between w-full px-4"):
            # Nome do sistema
            ui.label("📘 Meu App de Estudos").classes("text-2xl font-extrabold")
            # Links de navegação disponíveis na home (apenas Login e Sobre)
            with ui.row().classes("gap-8"):
                ui.link("🔑 Login", "/login").classes(
                    "text-lg hover:underline hover:text-yellow-300"
                )
                ui.link("ℹ️ Sobre", "/about").classes(
                    "text-lg hover:underline hover:text-yellow-300"
                )


# --- Página inicial do sistema ---
@ui.page("/")
def home():
    # Usa o cabeçalho padronizado
    cabecalho_padrao()

    # Conteúdo principal centralizado em um card
    with ui.card().classes("mx-auto mt-10 p-8 max-w-3xl shadow-lg bg-white"):
        ui.label("🎓 Bem-vindo ao Sistema de Estudos").classes(
            "text-3xl font-bold text-blue-800 mb-4"
        )
        ui.markdown(
            """
            **Aplicação desenvolvida com NiceGUI**  
            - Acesse o sistema pelo link de **Login**  
            - Navegue entre as páginas como **Dashboard**, **Planos**, e **Mais**  
            - Organize seus estudos com praticidade
            """
        ).classes("text-lg")

        # Botão para criar uma nova conta
        ui.button(
            "➡️ Criar uma Conta", on_click=lambda: ui.navigate.to("/signup")
        ).classes("mt-6 bg-blue-600 text-white hover:bg-blue-700 px-4 py-2 rounded")

        # Botão para acessar a tela de login
        ui.button(
            "➡️ Acessar Login", on_click=lambda: ui.navigate.to("/login")
        ).classes("mt-6 bg-blue-600 text-white hover:bg-blue-700 px-4 py-2 rounded")


# --- Inicializa o servidor NiceGUI ---
ui.run(
    title="Meu App",
    favicon="🔒",
    reload=True,
    port=8080,
    storage_secret=os.getenv("STORAGE_SECRET"),
)
