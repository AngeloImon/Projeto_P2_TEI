from nicegui import ui


@ui.page("/dashboard")
def dashboard():
    with ui.header().classes("bg-blue-800 text-whit p-4 shadow-md"):
        with ui.row().classes("items-center gap-4"):
            ui.link("Dashboard", "/dashboard").classes("text-lg")
            ui.link("Meus Planos", "planos").classes("text-lg")
            ui.link("Novo Plano", "novo-plano").classes("text-lg")
            ui.link("Sair", "/login").classes("text-lg")

        with ui.column().classes("mx-auto mt-8 p-8 max-w-4x1"):
            ui.label("Bem vindo ao seu painel de estudos!").classes(
                "text-2x1 font-bold mb-4"
            )
            ui.markdown(
                """
                        Aqui você pode:
                        - Visualizar seus planos de estudo!
                        - Criar novos planos!
                        - Acompanhar seu progresso!
                         """
            )
