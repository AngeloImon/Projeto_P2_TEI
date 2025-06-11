from nicegui import ui
import random
from calendar import monthrange


# --- Função utilitária para criar campos padrão de título, descrição, horário, duração e cor ---
def criar_campos_padrao(
    titulo_val="", descricao_val="", horario_val="", duracao_val="", cor_val=None
):
    cores = [
        ("Verde", "#22c55e"),
        ("Azul", "#3b82f6"),
        ("Laranja", "#f59e42"),
        ("Amarelo", "#eab308"),
        ("Vermelho", "#ef4444"),
        ("Roxo", "#a855f7"),
        ("Teal", "#14b8a6"),
    ]
    nomes_cores = [nome for nome, _ in cores]
    cor_hex = {nome: hex for nome, hex in cores}

    cor_val = cor_val if cor_val in nomes_cores else random.choice(nomes_cores)

    cor = ui.select(
        options=nomes_cores,
        value=cor_val,
        label="Cor do Plano",
    ).classes("w-full mb-2")

    # Preview dinâmico da cor selecionada (criado após o select)
    cor_preview = ui.html("").classes("mb-2")

    def atualizar_preview(e=None):
        cor_nome = cor.value if e is None else e.value
        cor_preview.content = (
            f'<div id="cor-preview" style="display:inline-block;width:32px;height:32px;'
            f'border-radius:6px;border:1px solid #ccc;background:{cor_hex[cor_nome]};margin-bottom:8px;"></div>'
        )

    cor.on("update:model-value", atualizar_preview)
    atualizar_preview()  # Atualiza preview na criação inicial

    titulo = ui.input("Título", value=titulo_val).classes("w-full mb-2")
    descricao = ui.input("Descrição", value=descricao_val).classes("w-full mb-2")
    alerta_horario = ui.input(
        "Horário do alerta (formato HH:MM)", value=horario_val
    ).classes("w-full mb-2")
    alerta_duracao = ui.input("Duração (minutos)", value=duracao_val).classes(
        "w-full mb-2"
    )
    return titulo, descricao, alerta_horario, alerta_duracao, cor


# --- Função utilitária para criar checkboxes dos dias da semana ---
def criar_checkboxes_dias_semana(valores_selecionados=None):
    if valores_selecionados is None:
        valores_selecionados = []
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    checkboxes = []
    with ui.row():
        for dia in dias_semana:
            cb = ui.checkbox(dia, value=(dia in valores_selecionados)).classes("mr-2")
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


# --- Função utilitária para notificar sucesso, fechar dialog e atualizar lista ---
def sucesso_e_atualiza(msg, dialog, atualizar_lista, carregar_planos):
    ui.notify(msg)
    dialog.close()
    atualizar_lista(carregar_planos())


# --- Função utilitária para notificar erro ---
def notificar_erro(msg):
    ui.notify(msg, color="negative")


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


# --- Função para atualizar a lista de planos exibidos na tela ---
def atualizar_lista(
    cards_row, lista, editar_plano, excluir_plano, visualizar_plano_func
):
    cards_row.clear()
    for plano in lista:
        with cards_row:
            with ui.card().classes("p-4 shadow-md w-[350px] h-[297px] overflow-hidden"):
                ui.label(f"📘 {plano['titulo']}").classes(
                    "text-lg font-bold mb-1 min-h-[24px] truncate w-full"
                )
                ui.label(plano.get("descricao", "") or " ").classes(
                    "text-sm text-gray-600 mb-1 min-h-[32px] w-full line-clamp-2 overflow-hidden"
                )
                ui.label(f"Programação: {plano.get('programacao', '') or ' '}").classes(
                    "text-sm text-gray-600 mb-1 min-h-[24px] truncate w-full"
                )
                ui.label(f"Alerta: {plano.get('alerta', '') or ' '}").classes(
                    "text-sm text-gray-600 mb-2 min-h-[24px] truncate w-full"
                )
                with ui.row().classes("gap-3 flex-nowrap"):
                    ui.button(
                        "👁️ Visualizar",
                        on_click=lambda p=plano: visualizar_plano_func(p),
                    ).classes("min-w-0 px-2")
                    ui.button(
                        "✏️ Editar", on_click=lambda p=plano: editar_plano(p)
                    ).classes("min-w-0 px-2")
                    ui.button(
                        "🗑️ Excluir",
                        color="red",
                        on_click=lambda p=plano: excluir_plano(p),
                    ).classes("min-w-0 px-2")


# --- Função para filtrar planos pelo texto digitado ---
def filtrar_planos(planos, texto, atualizar_lista_func):
    texto = texto.lower()
    filtrados = [p for p in planos if texto in p["titulo"].lower()]
    atualizar_lista_func(filtrados)
