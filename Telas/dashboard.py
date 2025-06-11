from nicegui import ui
import Telas.novo_plano as novo_plano

# --- Cabeçalho padronizado para o dashboard ---
def cabecalho_dashboard():
    with ui.header().classes(
        "bg-gradient-to-r from-blue-700 to-blue-900 text-white p-4 shadow-lg"
    ):
        with ui.row().classes("items-center justify-between w-full px-4"):
            ui.label("📚 Painel de Estudos").classes("text-2xl font-extrabold")
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


@ui.page("/dashboard")
def dashboard():
    # --- Cabeçalho ---
    cabecalho_dashboard()

    # --- Card principal centralizado ---
    with ui.card().classes(
        "mx-auto mt-10 p-10 max-w-5xl shadow-xl bg-gray-150 rounded-lg"
    ):  
        # --- Título e instrução ---
        ui.label("🎉 Bem-vindo ao seu Painel de Estudos!").classes(
            "text-3xl font-bold mb-6 text-blue-900"
        )
        ui.markdown(
            """
            Organize e acompanhe seu aprendizado de forma simples e prática.  
            Escolha uma das opções abaixo para começar:
            """
        ).classes("text-lg mb-8 text-gray-700")

        # --- Cards de atalho alinhados na mesma linha ---
        with ui.row().classes("gap-8 justify-center"):
            # Card 1: Meus Planos
            with ui.card().classes(
                "w-64 p-6 shadow-md hover:shadow-xl transition-shadow cursor-pointer"
            ).on("click", lambda: ui.navigate.to("/meus_planos")):
                ui.label("📋 Meus Planos").classes("text-xl font-semibold mb-2")
                ui.markdown("Veja e gerencie seus planos de estudo atuais.").classes(
                    "text-gray-600"
                )
                
            # Card 2: Criar Novo Plano
            with ui.card().classes(
                "w-64 p-6 shadow-md hover:shadow-xl transition-shadow cursor-pointer"
            ).on("click", lambda: ui.navigate.to("/novo_plano")):
                ui.label("➕ Criar Novo Plano").classes("text-xl font-semibold mb-2")
                ui.markdown(
                    "Adicione novos planos para organizar seus estudos."
                ).classes("text-gray-600")
                
            # Card 3: Sobre
            with ui.card().classes(
                "w-64 p-6 shadow-md hover:shadow-xl transition-shadow cursor-pointer"
            ).on("click", lambda: ui.navigate.to("/sobre")):
                ui.label("ℹ️ Sobre").classes("text-xl font-semibold mb-2")
                ui.markdown("Saiba mais sobre o aplicativo e seus recursos.").classes(
                    "text-gray-600"
                )

        # --- Dica do dia ---
        ui.label("🔔 Dica do Dia: Consistência é a chave para o sucesso!").classes(
            "mt-12 italic text-sm text-blue-700"
        )
