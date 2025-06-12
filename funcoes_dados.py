import json
import io
import zipfile
from nicegui import ui, app
from firebase_firestore import firestore_get_user_plans, firestore_create_user_plan
from datetime import datetime


def exportar_plano_individual(plano):
    # Gera nome do arquivo com data atual e nome do plano
    data_str = datetime.now().strftime("%Y-%m-%d")
    titulo = plano.get("titulo", "plano").replace(" ", "_")
    nome_arquivo = f"{titulo}_{data_str}.zip"

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr("plano.json", json.dumps(plano, ensure_ascii=False, indent=2))
    buffer.seek(0)

    ui.download(buffer.read(), filename=nome_arquivo)


def importar_plano_individual(arquivo, callback=None):
    try:
        zip_bytes = arquivo.content.read()
        with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as zip_file:
            if "plano.json" in zip_file.namelist():
                conteudo_json = zip_file.read("plano.json").decode("utf-8")
                plano = json.loads(conteudo_json)
            else:
                if callback:
                    callback(False, "Arquivo ZIP não contém plano.json.")
                return

        session = app.storage.user
        uid = session.get("uid")
        id_token = session.get("id_token")
        # Verifica se já existe um plano igual (por título e programação)
        planos_existentes = firestore_get_user_plans(uid, id_token)
        existe = any(
            p.get("titulo") == plano.get("titulo")
            and p.get("programacao") == plano.get("programacao")
            for p in planos_existentes
        )
        if existe:
            if callback:
                callback(False, "Já existe um plano com o mesmo título e programação.")
            return

        plano_novo = dict(plano)
        plano_novo.pop("id", None)
        firestore_create_user_plan(uid, id_token, plano_novo)
        if callback:
            callback(True, "Plano importado com sucesso!")
    except Exception as e:
        if callback:
            callback(False, f"Erro ao importar: {e}")


def exportar_dados():
    session = app.storage.user
    uid = session.get("uid")
    id_token = session.get("id_token")
    planos = firestore_get_user_plans(uid, id_token)
    json_str = json.dumps(planos, ensure_ascii=False, indent=2)

    data_str = datetime.now().strftime("%Y-%m-%d")
    nome_arquivo = f"meus_planos_{data_str}.zip"

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr("meus_planos.json", json_str)
    buffer.seek(0)

    ui.download(buffer.read(), filename=nome_arquivo)


def importar_dados(arquivo, callback=None):
    try:
        zip_bytes = arquivo.content.read()
        with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as zip_file:
            for nome_arquivo in zip_file.namelist():
                if nome_arquivo.endswith(".json"):
                    conteudo_json = zip_file.read(nome_arquivo).decode("utf-8")
                    dados = json.loads(conteudo_json)
                    break
            else:
                if callback:
                    callback(False, "Nenhum arquivo JSON encontrado no ZIP.")
                return

        session = app.storage.user
        uid = session.get("uid")
        id_token = session.get("id_token")
        planos_existentes = firestore_get_user_plans(uid, id_token)

        # Compara por conteúdo relevante
        def plano_igual(p1, p2):
            campos = ["titulo", "descricao", "programacao", "alerta", "cor"]
            return all(p1.get(c) == p2.get(c) for c in campos)

        planos_para_importar = []
        planos_ja_existentes = []
        for plano in dados:
            if any(plano_igual(plano, existente) for existente in planos_existentes):
                planos_ja_existentes.append(plano)
            else:
                planos_para_importar.append(plano)

        # Exibe todos os planos para o usuário escolher
        with ui.dialog() as dialog, ui.card():
            ui.label("Selecione os planos que deseja importar:").classes(
                "mb-2 font-bold"
            )
            checkboxes = []
            for plano in planos_para_importar:
                cb = ui.checkbox(
                    f"{plano.get('titulo', '')} | {plano.get('programacao', '')}",
                    value=True,
                )
                checkboxes.append((cb, plano))
            for plano in planos_ja_existentes:
                ui.checkbox(
                    f"{plano.get('titulo', '')} | {plano.get('programacao', '')} (já existe)",
                    value=False,
                ).props("disable")

            def confirmar_importacao():
                novos = 0
                for cb, plano in checkboxes:
                    if cb.value:
                        plano_novo = dict(plano)
                        plano_novo.pop("id", None)
                        firestore_create_user_plan(uid, id_token, plano_novo)
                        novos += 1
                dialog.close()
                if callback:
                    callback(
                        True, f"Importação concluída! {novos} novos planos adicionados."
                    )

            ui.button("Importar Selecionados", on_click=confirmar_importacao).classes(
                "bg-green-600 text-white mt-4"
            )
            ui.button("Cancelar", on_click=dialog.close).classes("mt-2")
        dialog.open()

    except Exception as e:
        if callback:
            callback(False, f"Erro ao importar: {e}")
