from nicegui import ui, app
from firebase_firestore import (
    firestore_get_user_plans,
    firestore_add_user_plan,
    firestore_update_user_plan,
    firestore_delete_user_plan,
)
from datetime import datetime


# --- Função utilitária para criar campos padrão de título, descrição, horário e duração ---
def criar_campos_padrao(
    titulo_val="", descricao_val="", horario_val="", duracao_val=""
):
    titulo = ui.input("Título", value=titulo_val).classes("w-full mb-2")
    descricao = ui.input("Descrição", value=descricao_val).classes("w-full mb-2")
    alerta_horario = ui.input(
        "Horário do alerta (formato HH:MM)", value=horario_val
    ).classes("w-full mb-2")
    alerta_duracao = ui.input("Duração (minutos)", value=duracao_val).classes(
        "w-full mb-2"
    )
    return titulo, descricao, alerta_horario, alerta_duracao


# --- Função utilitária para criar checkboxes dos dias da semana ---
def criar_checkboxes_dias_semana(valores_selecionados=None):
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    checkboxes = []
    with ui.row():
        for dia in dias_semana:
            cb = ui.checkbox(
                dia, value=(valores_selecionados and dia in valores_selecionados)
            ).classes("mr-2")
            checkboxes.append((dia, cb))
    return checkboxes


# --- Função utilitária para extrair horário e duração do alerta ---
def extrair_alerta(alerta):
    valor_horario = ""
    valor_duracao = ""
    if "Horário:" in alerta:
        partes = alerta.replace("Horário:", "").split(",")
        valor_horario = partes[0].strip()
        if len(partes) > 1 and "Duração:" in partes[1]:
            valor_duracao = partes[1].replace("Duração:", "").replace("min", "").strip()
    return valor_horario, valor_duracao


# --- Função para visualizar um plano em um dialog ---
def visualizar_plano(plano):
    with ui.dialog() as dialog, ui.card():
        ui.label(f"📘 {plano['titulo']}").classes("text-xl font-bold mb-2")
        ui.label(f"Descrição: {plano.get('descricao', 'Sem descrição.')}").classes(
            "mb-2"
        )
        ui.label(
            f"Programação: {plano.get('programacao', 'Sem programação.')}"
        ).classes("mb-2")
        ui.label(f"Alerta: {plano.get('alerta', 'Sem alerta.')}").classes("mb-4")
        ui.button("Fechar", on_click=dialog.close).classes("w-full")
    dialog.open()


# --- Função utilitária para notificar sucesso, fechar dialog e atualizar lista ---
def sucesso_e_atualiza(msg, dialog, atualizar_lista, carregar_planos):
    ui.notify(msg)
    dialog.close()
    atualizar_lista(carregar_planos())


# --- Função utilitária para notificar erro ---
def notificar_erro(msg):
    ui.notify(msg, color="negative")


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
    # Usa o cabeçalho padronizado
    cabecalho_meus_planos()

    # --- Recupera sessão do usuário ---
    session = app.storage.user
    uid = session.get("uid")
    id_token = session.get("id_token")

    # --- Verifica autenticação ---
    if not uid or not id_token:
        notificar_erro("Usuário não autenticado!")
        return

    # --- Função para buscar planos do usuário no Firestore ---
    def carregar_planos():
        return firestore_get_user_plans(uid, id_token)

    planos = carregar_planos()

    # --- Botões para adicionar novos planos ---
    with ui.row().classes("mb-4"):
        ui.button(
            "➕ Novo Plano por Calendário",
            on_click=lambda: adicionar_plano_calendario(),
        ).classes("bg-blue-500 text-white")
        ui.button(
            "➕ Novo Plano por Dias da Semana",
            on_click=lambda: adicionar_plano_dias_semana(),
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
        cards_row.clear()
        for plano in lista:
            with cards_row:
                with ui.card().classes(
                    "p-4 shadow-md w-[350px] h-[297px] overflow-hidden"
                ):
                    # Título (sempre em uma linha)
                    ui.label(f"📘 {plano['titulo']}").classes(
                        "text-lg font-bold mb-1 min-h-[24px] truncate w-full"
                    )
                    # Descrição (até 2 linhas, depois corta)
                    ui.label(plano.get("descricao", "") or " ").classes(
                        "text-sm text-gray-600 mb-1 min-h-[32px] w-full line-clamp-2 overflow-hidden"
                    )
                    # Programação (até 1 linha)
                    ui.label(
                        f"Programação: {plano.get('programacao', '') or ' '}"
                    ).classes("text-sm text-gray-600 mb-1 min-h-[24px] truncate w-full")
                    # Alerta (até 1 linha)
                    ui.label(f"Alerta: {plano.get('alerta', '') or ' '}").classes(
                        "text-sm text-gray-600 mb-2 min-h-[24px] truncate w-full"
                    )
                    # Botões
                    with ui.row().classes("gap-3 flex-nowrap"):
                        ui.button(
                            "👁️ Visualizar", on_click=lambda p=plano: visualizar_plano(p)
                        ).classes("min-w-0 px-2")
                        ui.button(
                            "✏️ Editar", on_click=lambda p=plano: editar_plano(p)
                        ).classes("min-w-0 px-2")
                        ui.button(
                            "🗑️ Excluir",
                            color="red",
                            on_click=lambda p=plano: excluir_plano(p),
                        ).classes("min-w-0 px-2")

    # --- Filtra planos pelo texto digitado no campo de busca ---
    def filtrar_planos(texto):
        texto = texto.lower()
        filtrados = [p for p in planos if texto in p["titulo"].lower()]
        atualizar_lista(filtrados)

    # --- Permite editar um plano existente ---
    def editar_plano(plano):
        with ui.dialog() as dialog, ui.card():
            # Extrai valores do alerta para preencher os campos
            valor_horario, valor_duracao = extrair_alerta(plano.get("alerta", ""))
            # Cria campos padrão preenchidos
            titulo, descricao, alerta_horario, alerta_duracao = criar_campos_padrao(
                plano["titulo"],
                plano.get("descricao", ""),
                valor_horario,
                valor_duracao,
            )
            programacao = plano.get("programacao", "")
            is_calendario = programacao.startswith("Data:") or programacao.startswith(
                "Datas:"
            )
            is_semana = programacao.startswith("Dias:")
            data_unica = None
            dias_semana_checkboxes = []
            # Cria campo de data ou checkboxes de dias da semana conforme o tipo de plano
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
                dias_semana_checkboxes = criar_checkboxes_dias_semana(valor_dias)

            # Função chamada ao salvar edição
            def salvar():
                if not verificar_titulo(titulo):
                    return
                if not verificar_alerta_horario(alerta_horario):
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
                }
                sucesso = firestore_update_user_plan(uid, id_token, plano["id"], novo)
                if sucesso:
                    sucesso_e_atualiza(
                        "Plano editado com sucesso!",
                        dialog,
                        atualizar_lista,
                        carregar_planos,
                    )
                else:
                    notificar_erro("Erro ao editar plano.")

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
                    sucesso_e_atualiza(
                        "Plano excluído com sucesso!",
                        dialog,
                        atualizar_lista,
                        carregar_planos,
                    )
                else:
                    notificar_erro("Erro ao excluir plano.")

            ui.button("Confirmar", color="red", on_click=confirmar).classes("w-full")
            ui.button("Cancelar", on_click=dialog.close).classes("mt-2 w-full")
        dialog.open()

    # --- Validação do campo título ---
    def verificar_titulo(titulo):
        if not titulo.value or not titulo.value.strip():
            ui.notify("O título é obrigatório.", color="warning")
            return False
        return True

    # --- Validação do campo horário do alerta ---
    def verificar_alerta_horario(alerta_horario):
        if not alerta_horario.value or not alerta_horario.value.strip():
            ui.notify("O horário do alerta é obrigatório.", color="warning")
            return False
        return True

    # --- Adiciona um novo plano por calendário (apenas uma data) ---
    def adicionar_plano_calendario():
        with ui.dialog() as dialog, ui.card():
            titulo, descricao, alerta_horario, alerta_duracao = criar_campos_padrao()
            ui.label("Data")
            data_unica = ui.date().classes("mb-2")

            def salvar():
                if not verificar_titulo(titulo):
                    return
                if not data_unica.value:
                    ui.notify("Selecione uma data.", color="warning")
                    return
                if not verificar_alerta_horario(alerta_horario):
                    return
                programacao = f"Data: {data_unica.value}"
                alerta = f"Horário: {alerta_horario.value}, Duração: {alerta_duracao.value} min"
                novo = {
                    "titulo": titulo.value,
                    "descricao": descricao.value,
                    "programacao": programacao,
                    "alerta": alerta,
                    "data_adicionado": datetime.now().isoformat(),
                }
                sucesso = firestore_add_user_plan(uid, id_token, novo)
                if sucesso:
                    sucesso_e_atualiza(
                        "Plano adicionado com sucesso!",
                        dialog,
                        atualizar_lista,
                        carregar_planos,
                    )
                else:
                    notificar_erro("Erro ao adicionar plano.")

            ui.button("Salvar", on_click=salvar).classes(
                "bg-blue-500 text-white w-full"
            )
            ui.button("Cancelar", on_click=dialog.close).classes("mt-2 w-full")
        dialog.open()

    # --- Adiciona um novo plano por dias da semana (checkboxes) ---
    def adicionar_plano_dias_semana():
        with ui.dialog() as dialog, ui.card():
            titulo, descricao, alerta_horario, alerta_duracao = criar_campos_padrao()
            dias_semana_checkboxes = criar_checkboxes_dias_semana()

            def salvar():
                if not verificar_titulo(titulo):
                    return
                if not verificar_alerta_horario(alerta_horario):
                    return
                dias_selecionados = [
                    dia for dia, cb in dias_semana_checkboxes if cb.value
                ]
                programacao = f"Dias: {', '.join(dias_selecionados)}"
                alerta = f"Horário: {alerta_horario.value}, Duração: {alerta_duracao.value} min"
                novo = {
                    "titulo": titulo.value,
                    "descricao": descricao.value,
                    "programacao": programacao,
                    "alerta": alerta,
                    "data_adicionado": datetime.now().isoformat(),
                }
                sucesso = firestore_add_user_plan(uid, id_token, novo)
                if sucesso:
                    sucesso_e_atualiza(
                        "Plano adicionado com sucesso!",
                        dialog,
                        atualizar_lista,
                        carregar_planos,
                    )
                else:
                    notificar_erro("Erro ao adicionar plano.")

            ui.button("Salvar", on_click=salvar).classes(
                "bg-blue-500 text-white w-full"
            )
            ui.button("Cancelar", on_click=dialog.close).classes("mt-2 w-full")
        dialog.open()

    # --- Exibe a lista inicial de planos ---
    atualizar_lista(planos)
