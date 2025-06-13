from nicegui import ui


@ui.page("/sobre")
def sobre():
    with ui.header().classes(
        "bg-gradient-to-r from-blue-700 to-blue-900 text-white p-4 shadow-lg"
    ):
        with ui.row().classes("items-center justify-between w-full px-4"):
            ui.label("ℹ️ Sobre o Aplicativo").classes("text-2xl font-extrabold")
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

    with ui.card().classes(
        "mx-auto mt-10 p-10 max-w-3xl shadow-xl bg-white rounded-lg"
    ):
        ui.label("Sobre o Aplicativo de Estudos").classes(
            "text-3xl font-bold mb-4 text-blue-900"
        )
        ui.markdown(
            """
            Este aplicativo foi criado para ajudar você a organizar, planejar e acompanhar seus estudos de forma simples e eficiente.

            **Funcionalidades principais:**
            
            - Criação e gerenciamento de planos de estudo
            
            - Visualização de calendário com tarefas
            
            - Destaque para próximas tarefas e dicas motivacionais
            
            - Interface intuitiva e responsiva

            Desenvolvido como projeto acadêmico para a disciplina de Tópicos Especiais em Informática (Fatec).

            **Tecnologias utilizadas:**

            - NiceGUI para a interface web
            
            - Firebase Firestore para armazenamento de dados
            
            - Python para lógica de backend

            **Autor:**

            - Angelo Ferdinand Imon Spanó - RA 2840482221025

            - Mariana Nakamura Taba - RA 2840482221005

            - João Vitor Bravo Arruda - RA 2840482221006

            ---
            **Dúvidas ou sugestões?**  
            Entre em contato com o desenvolvedor.
            """
        ).classes("text-lg text-gray-700")
