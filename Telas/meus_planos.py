from nicegui import ui, app
from firebase_firestore import (
    firestore_get_user_plans,
    firestore_update_user_plan,
    firestore_delete_user_plan,
)
import funcoes_planos


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
                ui.link(
                    "⬇️⬆️ Exportar/Importar Plano", "/importar_exportar_dados_individual"
                ).classes("text-lg hover:underline hover:text-yellow-300")


@ui.page("/meus_planos")
def meus_planos():
    cabecalho_meus_planos()

    session = app.storage.user
    uid = session.get("uid")
    id_token = session.get("id_token")

    if not uid or not id_token:
        funcoes_planos.notificar_erro("Usuário não autenticado!")
        return

    def carregar_planos():
        return firestore_get_user_plans(uid, id_token)

    planos = carregar_planos()

    with ui.row().classes("mb-4"):
        ui.button(
            "➕ Criar Novo Plano",
            on_click=lambda: ui.navigate.to("/novo_plano"),
        ).classes("bg-blue-500 text-white")

    search_row = ui.row().classes("mb-4 items-center gap-4")
    search_input = ui.input(
        label="Buscar plano...", on_change=lambda e: filtrar_planos(e.value)
    ).props("clearable")

    cards_row = ui.row().classes("gap-4 flex-wrap")

    cor_hex = {
        "Verde": "#22c55e",
        "Azul": "#3b82f6",
        "Laranja": "#f59e42",
        "Amarelo": "#eab308",
        "Vermelho": "#ef4444",
        "Roxo": "#a855f7",
        "Teal": "#14b8a6",
    }

    def atualizar_lista(lista):
        cards_row.clear()
        if not lista:
            with cards_row:
                ui.label("Nenhum plano encontrado.").classes("text-gray-500")
            return

        for plano in lista:
            cor_card = cor_hex.get(plano.get("cor", "Azul"), "#3b82f6")
            with cards_row:
                with ui.card().style(
                    f"border-left: 8px solid {cor_card}; min-width: 320px; max-width: 340px;"
                ).classes("mb-2 shadow-lg"):
                    ui.label(plano.get("titulo", "")).classes("text-xl font-bold mb-1")
                    ui.label(plano.get("descricao", "")).classes("mb-1 text-gray-700")
                    programacao = plano.get("programacao", "")
                    if programacao.startswith("Data:"):
                        ui.label(f"📅 {programacao}").classes("mb-1 text-blue-700")
                    elif programacao.startswith("Dias:"):
                        ui.label(f"📆 {programacao}").classes("mb-1 text-blue-700")

                    horario_str = plano.get("horario")
                    if not horario_str:
                        horario_str = "--:--"
                    duracao_str = plano.get("duracao")
                    if not duracao_str or str(duracao_str).lower() == "none":
                        duracao_str = "00"
                    else:
                        try:
                            duracao_str = str(int(float(duracao_str)))
                        except Exception:
                            duracao_str = "00"

                    ui.label(f"⏰ Horário: {horario_str}").classes("mb-1")
                    ui.label(f"⏳ Duração: {duracao_str} min").classes("mb-1")

                    with ui.row().classes("gap-2 mt-2"):
                        ui.button(
                            "✏️ Editar", on_click=lambda p=plano: editar_plano(p)
                        ).classes("bg-yellow-400 text-white")
                        ui.button(
                            "❌ Excluir", on_click=lambda p=plano: excluir_plano(p)
                        ).classes("bg-red-500 text-white")

    def filtrar_planos(texto):
        texto = texto.lower()
        filtrados = [
            plano
            for plano in planos
            if texto in plano.get("titulo", "").lower()
            or texto in plano.get("descricao", "").lower()
            or texto in plano.get("programacao", "").lower()
        ]
        atualizar_lista(filtrados)

    def editar_plano(plano):
        with ui.dialog() as dialog, ui.card():
            cor_val = plano.get("cor", None)
            valor_duracao = plano.get("duracao")
            try:
                valor_duracao = (
                    int(float(valor_duracao))
                    if valor_duracao not in ("", None)
                    else None
                )
            except Exception:
                valor_duracao = None

            valor_horario = plano.get("horario", "12:00")
            if not valor_horario or ":" not in valor_horario:
                hora_inicial = 12
                minuto_inicial = 0
            else:
                try:
                    hora_inicial = int(valor_horario.split(":")[0])
                    minuto_inicial = int(valor_horario.split(":")[1])
                except Exception:
                    hora_inicial = 12
                    minuto_inicial = 0

            titulo = ui.input("Título", value=plano.get("titulo", "")).classes(
                "w-full mb-2"
            )
            descricao = ui.input("Descrição", value=plano.get("descricao", "")).classes(
                "w-full mb-2"
            )

            ui.label("Horário do alerta (hora)").classes("mb-1")
            alerta_horario = (
                ui.slider(min=0, max=23, value=hora_inicial, step=1)
                .props("label-always")
                .classes("w-full mb-2")
            )

            ui.label("Minutos").classes("mb-1")
            alerta_minuto = (
                ui.slider(min=0, max=59, value=minuto_inicial, step=1)
                .props("label-always")
                .classes("w-full mb-2")
            )

            alerta_duracao = ui.number(
                min=1, step=1, value=valor_duracao, label="Duração (minutos)"
            ).classes("w-full mb-2")

            nomes_cores = [
                "Verde",
                "Azul",
                "Laranja",
                "Amarelo",
                "Vermelho",
                "Roxo",
                "Teal",
            ]
            cor = ui.select(
                options=nomes_cores,
                value=cor_val if cor_val in nomes_cores else "Azul",
                label="Cor do Plano",
            ).classes("w-full mb-2")

            cor_preview = ui.html("").classes("mb-2")

            def atualizar_preview(e=None):
                cor_nome = cor.value if e is None else e.value
                cor_preview.content = (
                    f'<div id="cor-preview" style="display:inline-block;width:32px;height:32px;'
                    f'border-radius:6px;border:1px solid #ccc;background:{cor_hex[cor_nome]};margin-bottom:8px;"></div>'
                )

            cor.on("update:model-value", atualizar_preview)
            atualizar_preview()

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
                if alerta_horario.value is None or alerta_minuto.value is None:
                    ui.notify("Selecione um horário válido.", color="warning")
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
                hora = f"{alerta_horario.value:02d}:{alerta_minuto.value:02d}"
                novo = {
                    "titulo": titulo.value,
                    "descricao": descricao.value,
                    "programacao": programacao_novo,
                    "horario": hora,
                    "duracao": (
                        int(alerta_duracao.value) if alerta_duracao.value else None
                    ),
                    "cor": cor.value,
                }
                data_adicionado = plano.get("data_adicionado")
                if data_adicionado:
                    novo["data_adicionado"] = data_adicionado
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

    atualizar_lista(planos)
