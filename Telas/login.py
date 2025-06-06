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


# --- Função para cadastrar usuário no Firebase ---
def firebase_signup(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
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


# --- Função para validar email ---
def email_valido(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email) is not None


# --- Cabeçalho padronizado para Login e Cadastro ---
def cabecalho_login():
    with ui.header().classes(
        "bg-gradient-to-r from-blue-700 to-blue-900 text-white p-4 shadow-lg"
    ):
        with ui.row().classes("items-center justify-between w-full px-4"):
            ui.label("🔑 Login").classes("text-2xl font-extrabold")
            with ui.row().classes("gap-8"):
                ui.link("🔑 Login", "/login").classes(
                    "text-lg hover:underline hover:text-yellow-300"
                )
                ui.link("ℹ️ Sobre", "/about").classes(
                    "text-lg hover:underline hover:text-yellow-300"
                )


# --- Página de cadastro ---
def create_signup_page():
    @ui.page("/signup")
    def signup_page():
        ui.query("body").style("background-color: #f0f0f0")

        # Usa o cabeçalho padronizado
        cabecalho_login()

        with ui.column().classes("mx-auto mt-8 items-center"):
            ui.label("Cadastro").classes("text-2xl text-blue-500 mb-8")

            with ui.card().classes("w-96 p-8 shadow-lg"):
                email = ui.input("Email").classes("w-full mb-4")
                password = ui.input(
                    "Senha", password=True, password_toggle_button=True
                ).classes("w-full mb-4")

                # Função chamada ao clicar em cadastrar
                def register():
                    result = firebase_signup(email.value, password.value)
                    if result:
                        ui.notify("Usuário criado com sucesso!", color="positive")
                        ui.navigate.to("/login")
                    else:
                        ui.notify("Erro ao criar usuário", color="negative")

                ui.button("Cadastrar", on_click=register).classes(
                    "w-full bg-blue-500 text-white"
                )

                ui.link("Já tem conta? Faça login", "/login").classes("text-sm mt-2")


# --- Página de login ---
def create_login_page():
    @ui.page("/login")
    def login_page():
        ui.query("body").style("background-color: #f0f0f0")

        # Usa o cabeçalho padronizado
        cabecalho_login()

        # Conteúdo principal da tela de login
        with ui.column().classes("mx-auto mt-8 items-center"):
            ui.label("Tela de Login").classes("text-2xl text-blue-500 mb-8")

            with ui.card().classes("w-96 p-8 shadow-lg"):
                username = ui.input("Email").classes("w-full mb-4")
                password = ui.input(
                    "Senha", password=True, password_toggle_button=True
                ).classes("w-full mb-4")

                # Função chamada ao clicar em Entrar
                def authenticate():
                    result = firebase_login(username.value, password.value)
                    if result:
                        app.storage.user["uid"] = result["localId"]
                        app.storage.user["id_token"] = result["idToken"]
                        ui.notify("Login bem sucedido!", color="positive")
                        ui.navigate.to("/dashboard")
                    else:
                        ui.notify("Credenciais inválidas", color="negative")

                # Abre o diálogo de cadastro rápido
                def open_signup_dialog():
                    with ui.dialog() as dialog, ui.card():
                        ui.label("Criar nova conta").classes("text-lg mb-4")
                        signup_email = ui.input("Email").classes("w-full mb-2")
                        signup_password = ui.input(
                            "Senha", password=True, password_toggle_button=True
                        ).classes("w-full mb-2")
                        signup_password2 = ui.input(
                            "Repita a senha", password=True, password_toggle_button=True
                        ).classes("w-full mb-2")

                        # Validação de senha forte
                        def senha_valida(senha):
                            return (
                                len(senha) >= 8
                                and re.search(r"[A-Z]", senha)
                                and re.search(r"[a-z]", senha)
                                and re.search(r"\d", senha)
                                and re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha)
                            )

                        # Função chamada ao cadastrar pelo diálogo
                        def do_signup():
                            if not email_valido(signup_email.value):
                                ui.notify("Digite um email válido.", color="negative")
                                return
                            if signup_password.value != signup_password2.value:
                                ui.notify("As senhas não coincidem.", color="negative")
                                return
                            if not senha_valida(signup_password.value):
                                ui.notify(
                                    "A senha deve ter pelo menos 8 caracteres, uma maiúscula, uma minúscula, um número e um caractere especial.",
                                    color="negative",
                                )
                                return
                            result = firebase_signup(
                                signup_email.value, signup_password.value
                            )
                            if result:
                                ui.notify(
                                    "Usuário criado com sucesso!", color="positive"
                                )
                                dialog.close()
                            else:
                                ui.notify("Erro ao criar usuário", color="negative")

                        ui.button("Cadastrar", on_click=do_signup).classes(
                            "w-full bg-green-500 text-white"
                        )
                        ui.button("Cancelar", on_click=dialog.close).classes(
                            "w-full mt-2"
                        )
                    dialog.open()

                # Abre o diálogo de recuperação de senha
                def open_password_reset_dialog():
                    with ui.dialog() as dialog, ui.card():
                        ui.label("Recuperar senha").classes("text-lg mb-4")
                        reset_email = ui.input("Email").classes("w-full mb-2")

                        def do_reset():
                            if firebase_password_reset(reset_email.value):
                                ui.notify(
                                    "Email de recuperação enviado!", color="positive"
                                )
                                dialog.close()
                            else:
                                ui.notify(
                                    "Erro ao enviar email de recuperação",
                                    color="negative",
                                )

                        ui.button("Enviar", on_click=do_reset).classes(
                            "w-full bg-blue-500 text-white"
                        )
                        ui.button("Cancelar", on_click=dialog.close).classes(
                            "w-full mt-2"
                        )
                    dialog.open()

            # Botão para autenticar login
            ui.button("Entrar", on_click=authenticate).classes(
                "w-full bg-blue-500 text-white"
            )
            # Botão para abrir diálogo de recuperação de senha
            ui.button("Esqueci a senha", on_click=open_password_reset_dialog).classes(
                "w-full bg-gray-100 text-blue-700 mt-2"
            )
            # Botão para abrir diálogo de cadastro rápido
            ui.button("Criar conta", on_click=open_signup_dialog).classes(
                "w-full bg-gray-200 text-blue-700 mt-2"
            )
