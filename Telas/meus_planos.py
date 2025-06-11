from nicegui import ui, app
from firebase_firestore import (
    firestore_get_user_plans,
    firestore_add_user_plan,
    firestore_update_user_plan,
    firestore_delete_user_plan,
)
from datetime import datetime
import funcoes_planos


# --- Cabeçalho padronizado para a página Meus Planos ---
def cabecalho_meus_planos():
    with ui.header().classes(
        "bg-gradient-to-r from-blue-700 to-blue-900 text-white p-4 shadow-lg"
    ):
        with ui.row().classes("items-center justify-between w-full px-4"):
            ui.label("📋 Meus Planos").classes("text-2xl font-extrabold")
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


# --- Página principal dos planos ---
@ui.page("/meus_planos")
def meus_planos():
    cabecalho_meus_planos()

    # --- Recupera sessão do usuário ---
    session = app.storage.user
    uid = session.get("uid")
    id_token = session.get("id_token")

    # --- Verifica autenticação ---
    if not uid or not id_token:
        funcoes_planos.notificar_erro("Usuário não autenticado!")
        return

    # --- Função para buscar planos do usuário no Firestore ---
    def carregar_planos():
        return firestore_get_user_plans(uid, id_token)

    planos = carregar_planos()

    # --- Botão para criar novo plano ---
    with ui.row().classes("mb-4"):
        ui.button(
            "➕ Criar Novo Plano",
            on_click=lambda: ui.navigate.to("/novo_plano"),
        ).classes("bg-blue-500 text-white")

    # --- Campo de busca de planos ---
    search_row = ui.row().classes("mb-4 items-center gap-4")
    search_input = ui.input(
        label="Buscar plano...", on_change=lambda e: filtrar_planos(e.value)
    ).props("clearable")

    # --- Container dos cards dos planos ---
    cards_row = ui.row().classes("gap-4 flex-wrap")

    # --- Atualiza a lista de planos exibidos na tela ---
    def atualizar_lista(lista):
        funcoes_planos.atualizar_lista(
            cards_row,
            lista,
            editar_plano,
            excluir_plano,
            funcoes_planos.visualizar_plano,
        )

    # --- Filtra planos pelo texto digitado no campo de busca ---
    def filtrar_planos(texto):
        funcoes_planos.filtrar_planos(planos, texto, atualizar_lista)

    # --- Permite editar um plano existente ---
    def editar_plano(plano):
        with ui.dialog() as dialog, ui.card():
            valor_horario, valor_duracao = funcoes_planos.extrair_alerta(
                plano.get("alerta", "")
            )
            cor_val = plano.get("cor", None)
            titulo, descricao, alerta_horario, alerta_duracao, cor = (
                funcoes_planos.criar_campos_padrao(
                    plano["titulo"],
                    plano.get("descricao", ""),
                    valor_horario,
                    valor_duracao,
                    cor_val,
                )
            )
            programacao = plano.get("programacao", "")
            is_calendario = programacao.startswith("Data:") or programacao.startswith(
                "Datas:"
            )
            is_semana = programacao.startswith("Dias:")
            data_unica = None
            dias_semana_checkboxes = []
            if is_calendario:
                valor_data = ""
                if ":" in programacao:
                    valor_data = programacao.split(":", 1)[1].strip().split(",")[0]
                ui.label("Data")
                data_unica = ui.date(value=valor_data).classes("mb-2")
            elif is_semana:
                valor_dias = []
                if ":" in programacao:
                    valor_dias = [
                        d.strip() for d in programacao.split(":", 1)[1].split(",")
                    ]
                dias_semana_checkboxes = funcoes_planos.criar_checkboxes_dias_semana(
                    valor_dias
                )

            def salvar():
                if not funcoes_planos.verificar_titulo(titulo):
                    return
                if not funcoes_planos.verificar_alerta_horario(alerta_horario):
                    return
                if is_calendario:
                    if not data_unica.value:
                        ui.notify("Selecione uma data.", color="warning")
                        return
                    programacao_novo = f"Data: {data_unica.value}"
                elif is_semana:
                    dias_selecionados = [
                        dia for dia, cb in dias_semana_checkboxes if cb.value
                    ]
                    programacao_novo = f"Dias: {', '.join(dias_selecionados)}"
                else:
                    programacao_novo = ""
                alerta_novo = f"Horário: {alerta_horario.value}, Duração: {alerta_duracao.value} min"
                novo = {
                    "titulo": titulo.value,
                    "descricao": descricao.value,
                    "programacao": programacao_novo,
                    "alerta": alerta_novo,
                    "cor": cor.value,
                }
                sucesso = firestore_update_user_plan(uid, id_token, plano["id"], novo)
                if sucesso:
                    funcoes_planos.sucesso_e_atualiza(
                        "Plano editado com sucesso!",
                        dialog,
                        atualizar_lista,
                        carregar_planos,
                    )
                else:
                    funcoes_planos.notificar_erro("Erro ao editar plano.")

            ui.button("Salvar", on_click=salvar).classes(
                "bg-green-500 text-white w-full"
            )
            ui.button("Cancelar", on_click=dialog.close).classes("mt-2 w-full")
        dialog.open()

    # --- Permite excluir um plano existente ---
    def excluir_plano(plano):
        with ui.dialog() as dialog, ui.card():
            ui.label(
                f"Tem certeza que deseja excluir o plano '{plano['titulo']}'?"
            ).classes("mb-4")

            def confirmar():
                sucesso = firestore_delete_user_plan(uid, id_token, plano["id"])
                if sucesso:
                    funcoes_planos.sucesso_e_atualiza(
                        "Plano excluído com sucesso!",
                        dialog,
                        atualizar_lista,
                        carregar_planos,
                    )
                else:
                    funcoes_planos.notificar_erro("Erro ao excluir plano.")

            ui.button("Confirmar", color="red", on_click=confirmar).classes("w-full")
            ui.button("Cancelar", on_click=dialog.close).classes("mt-2 w-full")
        dialog.open()

    # --- Exibe a lista inicial de planos ---
    atualizar_lista(planos)
