from nicegui import ui

def create_login_page():
    @ui.page('/login')
    def login_page():
        ui.query('body').style('background-color: #f0f0f0')

        with ui.column().classes('mx-auto mt-8 items-center'):
            ui.label('Tela de Login').classes('text-2xl text-blue-500 mb-8')

            with ui.card().classes('w-96 p-8 shadow-lg'):
                username = ui.input('Usuário').classes('w-full mb-4')
                password = ui.input('Senha', password=True, password_toggle_button=True).classes('w-full mb-4')

                ui.button('Entrar', on_click=lambda: authenticate(username.value, password.value)) \
                    .classes('w-full bg-blue-500 text-white')

                ui.link('Esqueci a senha', '/forgot-password').classes('text-sm mt-2')

    def authenticate(username: str, password: str):
        if username == 'admin' and password == '123':
            ui.notify('Login bem-sucedido!', color='positive')
            ui.open('/')
        else:
            ui.notify('Credenciais inválidas', color='negative')
