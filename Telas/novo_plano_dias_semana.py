from nicegui import ui, app
from datetime import datetime
from firebase_firestore import firestore_add_user_plan
from funcoes_planos import (
    criar_campos_padrao,
    criar_checkboxes_dias_semana,
    verificar_titulo,
    verificar_alerta_horario,
    sucesso_e_atualiza,
    notificar_erro,
)


def cabecalho_novo_plano_dias_semana():
    with ui.header().classes(
        "bg-gradient-to-r from-blue-700 to-blue-900 text-white p-4 shadow-lg"
    ):
        with ui.row().classes("items-center justify-between w-full px-4"):
            ui.label("🗓️ Novo Plano por Dias da Semana").classes(
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


@ui.page("/novo_plano_dias_da_semana")
def novo_plano_dias_semana():
    cabecalho_novo_plano_dias_semana()

    # --- Recupera sessão do usuário ---
    session = app.storage.user
    uid = session.get("uid")
    id_token = session.get("id_token")

    # --- Verifica autenticação ---
    if not uid or not id_token:
        notificar_erro("Usuário não autenticado!")
        return

    with ui.card().classes("mx-auto mt-10 w-[400px] p-8 shadow-lg"):
        ui.label("Preencha os dados do novo plano:").classes("text-lg font-bold mb-4")
        titulo, descricao, alerta_horario, alerta_minuto, alerta_duracao, cor = (
            criar_campos_padrao()
        )
        dias_semana_checkboxes = criar_checkboxes_dias_semana([])

        def salvar():
            if not verificar_titulo(titulo):
                return
            if not verificar_alerta_horario(alerta_horario):
                return
            dias_selecionados = [dia for dia, cb in dias_semana_checkboxes if cb.value]
            if not dias_selecionados:
                ui.notify("Selecione pelo menos um dia da semana.", color="warning")
                return

            programacao = f"Dias: {', '.join(dias_selecionados)}"
            hora = f"{alerta_horario.value:02d}:{alerta_minuto.value:02d}"

            novo = {
                "titulo": titulo.value,
                "descricao": descricao.value,
                "programacao": programacao,
                "horario": hora,
                "duracao": (
                    str(int(alerta_duracao.value)) if alerta_duracao.value else None
                ),
                "cor": cor.value,
                "data_adicionado": datetime.now().isoformat(),
            }
            sucesso = firestore_add_user_plan(uid, id_token, novo)
            if sucesso:
                sucesso_e_atualiza(
                    "Plano adicionado com sucesso!",
                    ui.dialog(),
                    lambda _: None,
                    lambda: [],
                )
                ui.navigate.to("/meus_planos")
            else:
                notificar_erro("Erro ao adicionar plano.")

        ui.button("Salvar", on_click=salvar).classes(
            "bg-blue-500 text-white w-full mt-4"
        )
        ui.button("Voltar", on_click=lambda: ui.navigate.to("/novo_plano")).classes(
            "bg-gray-400 text-white w-full mt-2"
        )
