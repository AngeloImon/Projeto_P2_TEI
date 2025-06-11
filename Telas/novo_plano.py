from nicegui import ui, app
from datetime import datetime
from firebase_firestore import (
    firestore_add_user_plan,
)

@ui.page("/novo_plano")
def novo_plano():
    # Cabeçalho da página
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

    # --- Recupera sessão do usuário ---
    session = app.storage.user
    uid = session.get("uid")
    id_token = session.get("id_token")
    
    # --- Verifica autenticação ---
    if not uid or not id_token:
        ui.notify("Usuário não autenticado!", color="negative")
        return

    with ui.card().classes(
        "mx-auto mt-10 p-8 max-w-3xl shadow-xl bg-gray-100 rounded-lg"
    ):
        ui.label("Preencha os detalhes do seu novo plano").classes("text-xl mb-4 font-semibold")
        titulo_input = ui.input("Título").classes("w-full mb-2")
        descricao_input = ui.input("Descrição").classes("w-full mb-2")
        ui.label("Tipo de programação")
        programacao_tipo = ui.radio(
            options=["Data", "Dias da Semana"],
            value="Data",
        ).classes("mb-2")
        data_input = ui.date("Data").classes("w-full mb-2")
        dias_checkboxes = []

        def criar_checkboxes_dias():
            nonlocal dias_checkboxes
            dias_checkboxes = []
            dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
            with ui.row():
                for dia in dias_semana:
                    cb = ui.checkbox(dia).classes("mr-2")
                    dias_checkboxes.append((dia, cb))
            dias_checkboxes.clear()

        def atualizar_programacao():
            if programacao_tipo.value == "Data":
                data_input.style("display: block")
                for _, cb in dias_checkboxes:
                    cb.style("display: none")
            else:
                data_input.style("display: none")
                criar_checkboxes_dias()
                for _, cb in dias_checkboxes:
                    cb.style("display: block")


        programacao_tipo.on("change", lambda e: atualizar_programacao())
        atualizar_programacao()

        alerta_horario = ui.input("Horário do alerta (HH:MM)").classes("w-full mb-2")
        alerta_duracao = ui.input("Duração (minutos)").classes("w-full mb-4")

        def salvar():
            titulo = titulo_input.value.strip()
            descricao = descricao_input.value.strip()
            if not titulo:
                ui.notify("O título é obrigatório.", color="warning")
                return
            if programacao_tipo.value == "Data":
                data_programacao = data_input.value
                if not data_programacao:
                    ui.notify("Selecione uma data.", color="warning")
                    return
                programacao = f"Data: {data_programacao}"
            else:
                dias_selecionados = [dia for dia, cb in dias_checkboxes if cb.value]
                if not dias_selecionados:
                    ui.notify("Selecione pelo menos um dia da semana.", color="warning")
                    return
                programacao = f"Dias: {', '.join(dias_selecionados)}"

            horario_alerta = alerta_horario.value.strip()
            duracao_alerta = alerta_duracao.value.strip()

            if not horario_alerta:
                ui.notify("O horário do alerta é obrigatório.", color="warning")
                return
            if not duracao_alerta.isdigit():
                ui.notify("Duração deve ser um número.", color="warning")
                return

            alerta = f"Horário: {horario_alerta}, Duração: {duracao_alerta} min"

            novo_plano = {
                "titulo": titulo,
                "descricao": descricao,
                "programacao": programacao,
                "alerta": alerta,
                "data_adicionado": datetime.now().isoformat(),
            }

            sucesso = firestore_add_user_plan(uid, id_token, novo_plano)
            if sucesso:
                ui.notify("Plano criado com sucesso!", color="positive")
                ui.navigate("/meus_planos")
            else:
                ui.notify("Erro ao criar o plano.", color="negative")

        ui.button("Salvar", on_click=salvar).classes("w-full bg-green-500 text-white mt-4")
        ui.button("Cancelar", on_click=lambda: ui.navigate("/meus_planos")).classes("w-full mt-2")
