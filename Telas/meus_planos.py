from nicegui import ui

# Dummy dados e funções para evitar erro na importação
planos = [
    {"titulo": "Plano 1", "descricao": "Descrição do Plano 1", "status": "Ativo", "data": "2025-06-05"},
    {"titulo": "Plano 2", "descricao": "Descrição do Plano 2", "status": "Concluído", "data": "2025-05-20"},
]

def filtrar_planos(valor):
    print(f"Filtro aplicado: {valor}")

def ver_detalhes(plano):
    print(f"Ver detalhes do plano: {plano['titulo']}")

def editar_plano(plano):
    print(f"Editar plano: {plano['titulo']}")

def excluir_plano(plano):
    print(f"Excluir plano: {plano['titulo']}")

@ui.page('/meus_planos')
def meus_planos():
    ui.label("📋 Meus Planos de Estudo").classes("text-2xl font-bold mb-4 text-blue-800")
    ui.input(label="Buscar plano...", on_change=lambda e: filtrar_planos(e.value)).props("clearable").classes("mb-4")

    with ui.column().classes("gap-4"):
        for plano in planos:
            with ui.card().classes("p-4 shadow-md"):
                ui.label(f"📘 {plano['titulo']}").classes("text-lg font-bold")
                ui.label(f"{plano['descricao']}").classes("text-sm text-gray-600")
                ui.label(f"Status: {plano['status']} | Criado em: {plano['data']}").classes("text-xs text-gray-500")

                with ui.row().classes("gap-3 mt-2"):
                    ui.button("👁️ Visualizar", on_click=lambda p=plano: ver_detalhes(p))
                    ui.button("✏️ Editar", on_click=lambda p=plano: editar_plano(p))
                    ui.button("🗑️ Excluir", color="red", on_click=lambda p=plano: excluir_plano(p))

