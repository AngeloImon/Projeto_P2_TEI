from nicegui import ui, app
from funcoes_dados import exportar_plano_individual, importar_plano_individual
from firebase_firestore import firestore_get_user_plans


def cabecalho_importar_exportar_individual():
    with ui.header().classes(
        "bg-gradient-to-r from-blue-700 to-blue-900 text-white p-4 shadow-lg"
    ):
        with ui.row().classes("items-center justify-between w-full px-4"):
            ui.label("⬇️⬆️ Exportar/Importar Plano Individual").classes(
                "text-2xl font-extrabold"
            )
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


@ui.page("/importar_exportar_dados_individual")
def importar_exportar_dados_individual():
    cabecalho_importar_exportar_individual()
    with ui.card().classes("mx-auto mt-10 p-8 max-w-2xl shadow-lg bg-white"):
        ui.label("Exportar/Importar Plano Individual").classes(
            "text-2xl font-bold mb-4 text-blue-900"
        )
        ui.markdown(
            """
            Utilize esta página para **exportar** seus planos de estudo individuais em formato JSON zipado.
            Ou **importar** planos individuais salvos anteriormente.
            """
        ).classes("text-lg mb-6 text-gray-700")

        session = app.storage.user
        uid = session.get("uid")
        id_token = session.get("id_token")
        planos = firestore_get_user_plans(uid, id_token)

        with ui.row().classes("gap-8 justify-center mb-8"):
            # Botão Exportar
            def abrir_dialog_exportar():
                with ui.dialog() as dialog:
                    with ui.card().classes("max-w-2xl"):
                        ui.label("Selecione um plano para exportar:").classes("font-bold mb-4")
                        with ui.row().classes("w-full font-bold text-blue-900 mb-2"):
                            ui.label("Título").classes("w-1/3")
                            ui.label("Descrição").classes("w-2/3")
                            ui.label("").classes("w-12")  # espaço para o botão
                        with ui.column().classes("w-full"):
                            for plano in planos:
                                with ui.row().classes("items-center border-b border-gray-200 py-2"):
                                    ui.label(plano.get("titulo", "Sem título")).classes("w-1/3")
                                    ui.label(
                                        plano.get("descricao", "")[:60] +
                                        ("..." if len(plano.get("descricao", "")) > 60 else "")
                                    ).classes("w-2/3 text-sm text-gray-500")
                                    ui.button(
                                        "",
                                        on_click=lambda p=plano: (exportar_plano_individual(p), dialog.close()),
                                        icon="download"
                                    ).classes("bg-blue-600 text-white w-10 h-10")
                        ui.button("Fechar", on_click=dialog.close).classes("mt-4")
                dialog.open()

            ui.button(
                "Exportar Plano", on_click=abrir_dialog_exportar, icon="download"
            ).classes("bg-blue-600 text-white w-48 text-lg")

            # Botão Importar
            ui.upload(
                label="Importar Plano (ZIP)",
                auto_upload=True,
                on_upload=lambda e: importar_plano_individual(
                    e, lambda ok, msg: ui.notify(msg, color="green" if ok else "red")
                ),
            ).props("accept=.zip").classes("bg-blue-600 text-white w-48 text-lg")

        ui.markdown(
            """
            > **Atenção:**  
            > Ao importar, apenas planos que não existam ainda serão adicionados.
            """
        ).classes("text-xs text-gray-400 mt-6")
