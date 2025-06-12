from nicegui import ui, app
from datetime import datetime
from calendar import monthrange
from firebase_firestore import firestore_get_user_plans
from collections import defaultdict
from datetime import datetime, timedelta

CORES_HEX = {
    "Verde": "#22c55e",
    "Azul": "#3b82f6",
    "Laranja": "#f59e42",
    "Amarelo": "#eab308",
    "Vermelho": "#ef4444",
    "Roxo": "#a855f7",
    "Teal": "#14b8a6",
}


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
                ui.link(
                    "⬇️⬆️ Exportar/Importar Dados", "/importar_exportar_dados_geral"
                ).classes("text-lg hover:underline hover:text-yellow-300")


@ui.page("/dashboard")
def dashboard():
    cabecalho_dashboard()

    with ui.card().classes(
        "mx-auto mt-10 p-10 max-w-5xl shadow-xl bg-gray-150 rounded-lg"
    ):
        ui.label("🎉 Bem-vindo ao seu Painel de Estudos!").classes(
            "text-3xl font-bold mb-6 text-blue-900"
        )
        ui.markdown(
            """
            Organize e acompanhe seu aprendizado de forma simples e prática.  
            Escolha uma das opções abaixo para começar:
            """
        ).classes("text-lg mb-8 text-gray-700")

        # --- CARDS DE NAVEGAÇÃO ---
        with ui.row().classes("gap-8 justify-center"):
            with ui.card().classes(
                "w-64 p-6 shadow-md hover:shadow-xl transition-shadow cursor-pointer"
            ).on("click", lambda: ui.navigate.to("/meus_planos")):
                ui.label("📋 Meus Planos").classes("text-xl font-semibold mb-2")
                ui.markdown("Veja e gerencie seus planos de estudo atuais.").classes(
                    "text-gray-600"
                )
            with ui.card().classes(
                "w-64 p-6 shadow-md hover:shadow-xl transition-shadow cursor-pointer"
            ).on("click", lambda: ui.navigate.to("/novo_plano")):
                ui.label("➕ Criar Novo Plano").classes("text-xl font-semibold mb-2")
                ui.markdown(
                    "Adicione novos planos para organizar seus estudos."
                ).classes("text-gray-600")
            with ui.card().classes(
                "w-64 p-6 shadow-md hover:shadow-xl transition-shadow cursor-pointer"
            ).on("click", lambda: ui.navigate.to("/sobre")):
                ui.label("ℹ️ Sobre").classes("text-xl font-semibold mb-2")
                ui.markdown("Saiba mais sobre o aplicativo e seus recursos.").classes(
                    "text-gray-600"
                )

        # --- VARIÁVEIS E FUNÇÕES DO CALENDÁRIO ---
        hoje = datetime.now().date()
        ano_atual = hoje.year
        mes_atual = hoje.month

        MESES_PT = [
            "",
            "Janeiro",
            "Fevereiro",
            "Março",
            "Abril",
            "Maio",
            "Junho",
            "Julho",
            "Agosto",
            "Setembro",
            "Outubro",
            "Novembro",
            "Dezembro",
        ]

        ano = ui.number("Ano", value=ano_atual, min=1900, max=2100).classes("hidden")
        mes = ui.number("Mês", value=mes_atual, min=1, max=12).classes("hidden")

        session = app.storage.user
        uid = session.get("uid")
        id_token = session.get("id_token")
        planos = firestore_get_user_plans(uid, id_token)

        contagem_planos = defaultdict(int)
        cores_planos = dict()
        dias_semana_map = {
            "Domingo": 6,
            "Segunda": 0,
            "Terça": 1,
            "Quarta": 2,
            "Quinta": 3,
            "Sexta": 4,
            "Sábado": 5,
        }

        for plano in planos or []:
            try:
                prog = plano.get("programacao", "")
                cor_nome = plano.get("cor")
                data_criacao = plano.get("data_adicionado", "")
                data_criacao_dt = None
                if data_criacao:
                    try:
                        data_criacao_dt = datetime.fromisoformat(data_criacao[:10])
                    except Exception:
                        data_criacao_dt = None

                if "Data:" in prog and cor_nome:
                    data_prog = prog.split("Data:")[1].strip()[:10]
                    contagem_planos[data_prog] += 1
                    if data_prog not in cores_planos:
                        cores_planos[data_prog] = []
                    cores_planos[data_prog].append(cor_nome)
                elif "Dias:" in prog and cor_nome:
                    dias_str = prog.split("Dias:")[1].strip()
                    dias_lista = [d.strip() for d in dias_str.split(",")]
                    dias_indices = [
                        dias_semana_map[d] for d in dias_lista if d in dias_semana_map
                    ]
                    for mes_iter in range(1, 13):
                        for dia in range(1, 32):
                            try:
                                data = datetime(ano_atual, mes_iter, dia)
                            except ValueError:
                                continue
                            if data_criacao_dt and data.date() < data_criacao_dt.date():
                                continue
                            if data.weekday() in dias_indices:
                                data_prog = data.strftime("%Y-%m-%d")
                                contagem_planos[data_prog] += 1
                                if data_prog not in cores_planos:
                                    cores_planos[data_prog] = []
                                cores_planos[data_prog].append(cor_nome)
            except Exception:
                pass

        def mudar_mes(delta):
            novo_mes = mes.value + delta
            novo_ano = ano.value
            if novo_mes < 1:
                novo_mes = 12
                novo_ano -= 1
            elif novo_mes > 12:
                novo_mes = 1
                novo_ano += 1
            mes.value = novo_mes
            ano.value = novo_ano
            desenhar_calendario()

        # --- CALENDÁRIO E PRÓXIMAS TAREFAS LADO A LADO ---
        with ui.card().classes("mt-10 p-6 shadow-md bg-white rounded-lg"):
            with ui.row().classes("gap-10 items-start"):
                with ui.column().classes("flex-grow"):
                    ui.label("🗓️ Calendário").classes(
                        "text-lg font-semibold text-blue-900 mb-4"
                    )
                    calendario_box = ui.column().classes("mt-4")

                    def desenhar_calendario():
                        calendario_box.clear()
                        with calendario_box:
                            with ui.row().classes(
                                "justify-center items-center mb-2 gap-2"
                            ):
                                ui.button("◀", on_click=lambda: mudar_mes(-1)).props(
                                    "flat dense"
                                )
                                ui.label(f"{MESES_PT[mes.value]} {ano.value}").classes(
                                    "text-base font-bold w-40 text-center"
                                )
                                ui.button("▶", on_click=lambda: mudar_mes(1)).props(
                                    "flat dense"
                                )
                            DIAS_PT = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
                            with ui.row().classes("gap-2 justify-center font-bold"):
                                for dia in DIAS_PT:
                                    ui.label(dia).classes("w-10 text-center")

                            primeiro_dia_semana, dias_no_mes = monthrange(
                                int(ano.value), int(mes.value)
                            )
                            primeiro_dia_semana = (primeiro_dia_semana + 1) % 7

                            if mes.value == 1:
                                mes_ant = 12
                                ano_ant = ano.value - 1
                            else:
                                mes_ant = mes.value - 1
                                ano_ant = ano.value
                            _, dias_no_mes_ant = monthrange(ano_ant, mes_ant)

                            dias = []
                            for i in range(primeiro_dia_semana):
                                dias.append(
                                    {
                                        "dia": dias_no_mes_ant
                                        - (primeiro_dia_semana - i - 1),
                                        "tipo": "anterior",
                                    }
                                )
                            for d in range(1, dias_no_mes + 1):
                                dias.append({"dia": d, "tipo": "atual"})
                            proximo_dia = 1
                            while len(dias) % 7 != 0:
                                dias.append({"dia": proximo_dia, "tipo": "proximo"})
                                proximo_dia += 1
                            total_semanas = len(dias) // 7
                            if total_semanas < 6:
                                for i in range(7):
                                    dias.append({"dia": proximo_dia, "tipo": "proximo"})
                                    proximo_dia += 1

                            for semana in range(0, len(dias), 7):
                                with ui.row().classes("gap-2 justify-center"):
                                    for d in dias[semana : semana + 7]:
                                        if d["tipo"] == "anterior":
                                            if mes.value == 1:
                                                cell_ano = ano.value - 1
                                                cell_mes = 12
                                            else:
                                                cell_ano = ano.value
                                                cell_mes = mes.value - 1
                                        elif d["tipo"] == "proximo":
                                            if mes.value == 12:
                                                cell_ano = ano.value + 1
                                                cell_mes = 1
                                            else:
                                                cell_ano = ano.value
                                                cell_mes = mes.value + 1
                                        else:
                                            cell_ano = ano.value
                                            cell_mes = mes.value

                                        data_atual = datetime(
                                            cell_ano, cell_mes, d["dia"]
                                        ).date()
                                        data_str = data_atual.strftime("%Y-%m-%d")
                                        n_tarefas = contagem_planos.get(data_str, 0)

                                        cor = (
                                            (
                                                "bg-blue-200 text-blue-900 font-bold"
                                                if data_atual == hoje
                                                else "bg-white text-gray-700"
                                            )
                                            if d["tipo"] == "atual"
                                            else "bg-gray-100 text-gray-400"
                                        )

                                        with ui.element("div").classes(
                                            f"w-10 h-10 rounded border {cor} flex flex-col items-center justify-start p-0 m-0 overflow-hidden"
                                        ):
                                            ui.label(str(d["dia"])).classes(
                                                "text-xs text-center p-0 m-0"
                                            )
                                            cores_do_dia = cores_planos.get(
                                                data_str, []
                                            )
                                            for i in range(6):
                                                if i < len(cores_do_dia):
                                                    cor_barra = CORES_HEX.get(
                                                        cores_do_dia[i]
                                                    )
                                                    ui.element("div").classes(
                                                        "h-1 w-full m-0 p-0 rounded"
                                                    ).style(
                                                        f"background-color: {cor_barra};"
                                                    )
                                                else:
                                                    ui.element("div").classes(
                                                        "h-1 w-full bg-gray-200 m-0 p-0 rounded"
                                                    )

                    desenhar_calendario()
                    ano.on("change", lambda e: desenhar_calendario())
                    mes.on("change", lambda e: desenhar_calendario())

                # Próximas tarefas
                with ui.column().classes("w-80"):
                    ui.label("📅 Próximas Tarefas").classes("text-lg font-semibold text-blue-900 mb-2")
                    ui.space().classes("mb-10")
                    hoje_dt = datetime.now().date()
                    tarefas_futuras = []
                    for plano in planos or []:
                        prog = plano.get("programacao", "")
                        cor_nome = plano.get("cor")
                        if "Data:" in prog:
                            data_str = prog.split("Data:")[1].strip()[:10]
                            data_dt = datetime.strptime(data_str, "%Y-%m-%d").date()
                            if data_dt >= hoje_dt:
                                tarefas_futuras.append((data_dt, plano))
                        elif "Dias:" in prog:
                            dias_str = prog.split("Dias:")[1].strip()
                            dias_lista = [d.strip() for d in dias_str.split(",")]
                            dias_semana_map = {
                                "Domingo": 6, "Segunda": 0, "Terça": 1, "Quarta": 2,
                                "Quinta": 3, "Sexta": 4, "Sábado": 5,
                            }
                            dias_indices = [dias_semana_map[d] for d in dias_lista if d in dias_semana_map]
                            for i in range(14):
                                dia_check = hoje_dt + timedelta(days=i)
                                if dia_check.weekday() in dias_indices:
                                    tarefas_futuras.append((dia_check, plano))
                                    break
                    tarefas_futuras.sort(key=lambda x: x[0])
                    for tarefa in tarefas_futuras[:7]:
                        data_dt, plano = tarefa
                        cor_nome = plano.get("cor")
                        cor_hex = CORES_HEX.get(cor_nome, "#3b82f6")
                        titulo = plano.get("titulo", "")
                        descricao = plano.get("descricao", "")
                        horario = plano.get("horario", "--:--")
                        duracao = plano.get("duracao", "00")
                        if duracao is None or str(duracao).lower() == "none":
                            duracao = "00"
                        else:
                            try:
                                duracao = str(int(float(duracao)))
                            except Exception:
                                duracao = "00"
                        # Primeira linha: ícone, nome e descrição (tudo inline)
                        with ui.row().classes("items-center mb-0"):
                            ui.icon("event").style(f"color: {cor_hex};")
                            ui.label(f"{titulo}").classes("ml-2 font-semibold")
                            if descricao:
                                ui.label(f"— {descricao}").classes("ml-2 text-gray-700 text-sm")
                        # Segunda linha: data, horário e duração
                        with ui.row().classes("ml-8 mb-2"):
                            ui.label(f"{data_dt.strftime('%d/%m')} • {horario} • {duracao} min").classes("text-blue-900 text-xs")
                    if not tarefas_futuras:
                        ui.label("Nenhuma tarefa futura encontrada.").classes("text-gray-500")

        # --- DICA DO DIA ---
        ui.label("🔔 Dica do Dia: Consistência é a chave para o sucesso!").classes(
            "mt-12 italic text-sm text-blue-700"
        )
