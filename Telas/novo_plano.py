from nicegui import ui


def cabecalho_novo_plano():
    with ui.header().classes(
        "bg-gradient-to-r from-blue-700 to-blue-900 text-white p-4 shadow-lg"
    ):
        with ui.row().classes("items-center justify-between w-full px-4"):
            ui.label("📝 Criar Novo Plano").classes("text-2xl font-extrabold")
            with ui.row().classes("gap-8"):
                ui.link("🏠 Dashboard", "/dashboard").classes(
                    "text-lg hover:underline hover:text-yellow-300"
                )
                ui.link("📋 Meus Planos", "/meus_planos").classes(
                    "text-lg hover:underline hover:text-yellow-300"
                )
                ui.link("🔒 Sair", "/login").classes(
                    "text-lg hover:underline hover:text-yellow-300"
                )


@ui.page("/novo_plano")
def novo_plano():
    cabecalho_novo_plano()

    with ui.card().classes("mx-auto mt-16 w-[400px] p-8 shadow-lg"):
        ui.label("Como deseja criar seu plano?").classes("text-xl font-bold mb-6")
        with ui.row().classes("gap-4"):
            ui.button(
                "Criar por Calendário",
                on_click=lambda: ui.navigate.to("/novo_plano_calendario"),
            ).classes("bg-blue-500 text-white w-full")
            ui.button(
                "Criar por Dias da Semana",
                on_click=lambda: ui.navigate.to("/novo_plano_dias_da_semana"),
            ).classes("bg-green-500 text-white w-full")
