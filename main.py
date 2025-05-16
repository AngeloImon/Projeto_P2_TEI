from nicegui import ui
from Telas.login import create_login_page

# Register all page routes first
create_login_page()

# Home page
@ui.page('/')
def home():
    with ui.header().classes('bg-blue-800 text-white p-4 shadow-md'):
        with ui.row().classes('items-center gap-4'):
            ui.link('Home', '/').classes('text-lg')
            ui.link('Login', '/login').classes('text-lg')
            ui.link('Sobre', '/about').classes('text-lg')

    with ui.column().classes('mx-auto mt-8 p-8 max-w-4xl'):
        ui.label('Bem-vindo ao Sistema').classes('text-3xl font-bold mb-4')
        ui.markdown('''
        **Aplicação desenvolvida com NiceGUI**
        - Acesse o sistema pelo link de Login
        - Navegue entre as páginas
        ''')

# Start the app with reload enabled (for development)
ui.run(
    title='Meu App',
    favicon='🔒',
    reload=True,  # Enable hot-reloading
    port=8080
)
