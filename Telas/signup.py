from nicegui import ui
from dotenv import load_dotenv
import requests
import re
import os

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")

# --- Função para cadastrar usuário no Firebase ---
def firebase_signup(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# --- Função para validar email ---
def email_valido(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email) is not None

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
                
def signup():
    @ui.page("/signup")
    def signup_page():
        ui.query("body").style("background-color: #f0f0f0")
        
        cabecalho_login()
        
        # Conteúdo principal da tela de cadastro
        with ui.column().classes("mx-auto mt-8 items-center"):
            ui.label("Cadastro").classes("text-2xl text-blue-500 mb-8")
            with ui.card().classes("w-96 p-8 shadow-lg"):
                email = ui.input("Email").classes("w-full mb-4")
                password = ui.input(
                    "Senha", password=True, password_toggle_button=True
                ).classes("w-full mb-4")
                password2 = ui.input(
                    "Repita a senha", password=True, password_toggle_button=True
                ).classes("w-full mb-4")
                
                def register():
                    if not email_valido(email.value):
                        ui.notify("Digite um email válido.", color="negative")
                        return
                    if password.value != password2.value:
                        ui.notify("As senhas não coincidem.", color="negative")
                        return
                    if not (
                        len(password.value) >= 8
                        and re.search(r"[A-Z]", password.value)
                        and re.search(r"[a-z]", password.value)
                        and re.search(r"\d", password.value)
                        and re.search(r"[!@#$%^&£%¢¨¬*()\-_=+§´`^~,.?\":;{}ªº|<>]", password.value)
                    ):
                        ui.notify(
                            "A senha deve ter pelo menos 8 caracteres, uma maiúscula, uma minúscula, um número e um caractere especial.",
                            color="negative",
                        )
                        return
                    result = firebase_signup(email.value, password.value)
                    if result:
                        ui.notify("Usuário criado com sucesso!", color="positive")
                        ui.navigate.to("/dashboard")
                    else:
                        ui.notify("Erro ao criar usuário", color="negative")
                
                ui.button("Cadastrar", on_click=register).classes(
                    "w-full bg-blue-500 text-white"
                )