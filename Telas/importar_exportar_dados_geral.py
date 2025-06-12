from nicegui import ui
from funcoes_dados import exportar_dados, importar_dados


def cabecalho_importar_exportar():
    with ui.header().classes(
        "bg-gradient-to-r from-blue-700 to-blue-900 text-white p-4 shadow-lg"
    ):
        with ui.row().classes("items-center justify-between w-full px-4"):
            ui.label("📦 Importar/Exportar Dados").classes("text-2xl font-extrabold")
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


@ui.page("/importar_exportar_dados_geral")
def importar_exportar_dados_geral():
    cabecalho_importar_exportar()
    with ui.card().classes("mx-auto mt-10 p-8 max-w-2xl shadow-lg bg-white"):
        ui.label("Importação e Exportação de Dados").classes(
            "text-3xl font-bold mb-2 text-blue-900"
        )
        ui.markdown(
            """
            Utilize esta página para **exportar** todos os seus planos de estudo em formato JSON zipado. 
            Ou **importar** planos salvos anteriormente.
            """
        ).classes("text-lg mb-6 text-gray-700")

        with ui.row().classes("gap-8 justify-center mb-8"):
            with ui.column().classes("items-center"):
                ui.button(
                    "Exportar Dados", on_click=exportar_dados, icon="download"
                ).classes("bg-blue-600 text-white w-48 text-lg")
                ui.label("Baixe um backup dos seus planos").classes(
                    "text-sm text-gray-500 mt-2"
                )
            with ui.column().classes("items-center"):
                ui.upload(
                    label="Importar Dados (ZIP)",
                    auto_upload=True,
                    on_upload=lambda e: importar_dados(
                        e,
                        lambda ok, msg: ui.notify(msg, color="green" if ok else "red"),
                    ),
                ).props("accept=.zip").classes("bg-blue-600 text-white w-48 text-lg")
                ui.label("Restaure planos a partir de um arquivo ZIP").classes(
                    "text-sm text-gray-500 mt-2"
                )

        ui.markdown(
            """
            > **Atenção:**  
            > Ao importar, você poderá escolher quais planos deseja adicionar.  
            > Planos já existentes não serão duplicados.
            """
        ).classes("text-xs text-gray-400 mt-6")
