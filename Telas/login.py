from nicegui import ui, app
import os
from dotenv import load_dotenv
import requests
import re

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")


# --- Função para autenticar usuário no Firebase ---
def firebase_login(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return None


# --- Função para enviar email de recuperação de senha ---
def firebase_password_reset(email):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_API_KEY}"
    payload = {"requestType": "PASSWORD_RESET", "email": email}
    response = requests.post(url, json=payload)
    return response.status_code == 200


# --- Cabeçalho padronizado para Login e Cadastro ---
def cabecalho_login():
    with ui.header().classes(
        "bg-gradient-to-r from-blue-700 to-blue-900 text-white p-4 shadow-lg"
    ):
        with ui.row().classes("items-center justify-between w-full px-4"):
            ui.label("🔑 Home").classes("text-2xl font-extrabold")
            with ui.row().classes("gap-8"):
                ui.link("🔑 Home", "/login").classes(
                    "text-lg hover:underline hover:text-yellow-300"
                )
                ui.link("ℹ️ Sobre", "/about").classes(
                    "text-lg hover:underline hover:text-yellow-300"
                )


# --- Página de login ---
def login():
    @ui.page("/login")
    def login_page():
        # Define o estilo de fundo da página
        ui.query("body").style("background-color: #f0f0f0")
        
        cabecalho_login()
        
        # Conteúdo principal da tela de login
        with ui.column().classes("mx-auto mt-8 items-center"):
            ui.label("Tela de Login").classes("text-2xl text-blue-500 mb-8")
            with ui.card().classes("w-96 p-8 shadow-lg"):
                email_input = ui.input("Email").classes("w-full mb-4")
                password_input = ui.input(
                    "Senha", password=True, password_toggle_button=True
                ).classes("w-full mb-4")
                
                def authenticate():
                    result = firebase_login(email_input.value, password_input.value)
                    if result:
                        # Armazena informações do usuário na sessão
                        app.storage.user["uid"] = result["localId"]
                        app.storage.user["id_token"] = result["idToken"]
                        ui.notify("Login bem-sucedido!", color="positive")
                        ui.navigate.to("/dashboard")
                    else:
                        ui.notify("Credenciais inválidas", color="negative")
                
                # Botão de login
                ui.button("Entrar", on_click=authenticate).classes(
                    "w-full bg-blue-500 text-white"
                )
                
                def open_password_reset_dialog():
                    # Diálogo de recuperação de senha
                    with ui.dialog() as dialog, ui.card():
                        ui.label("Recuperar senha").classes("text-lg mb-4")
                        reset_email = ui.input("Email").classes("w-full mb-2")
                        
                        def do_reset():
                            if firebase_password_reset(reset_email.value):
                                ui.notify("Email de recuperação enviado!", color="positive")
                                dialog.close()
                            else:
                                ui.notify("Erro ao enviar email de recuperação", color="negative")
                        
                        ui.button("Enviar", on_click=do_reset).classes(
                            "w-full bg-blue-500 text-white"
                        )
                        ui.button("Cancelar", on_click=dialog.close).classes(
                            "w-full mt-2"
                        )
                    dialog.open()
                
                # Botões Recuperar senha
                ui.button("Esqueci a senha", on_click=open_password_reset_dialog).classes(
                    "w-full bg-gray-100 text-blue-700 mt-2"
                )
                
                # Botões Criar conta
                ui.button(
                    "Criar conta",on_click=lambda: ui.navigate.to("/signup")).classes("w-full bg-gray-200 text-blue-700 mt-2"
                )
                 