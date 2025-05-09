from nicegui import ui

# Não se esqueçam de instalar o nicegui com o comando: pip install nicegui (no terminal)
# Depois de instalar: pip install --upgrade nicegui

ui.label("Hello, NiceGUI!").style("font-size: 2em; color: blue;")

ui.button("Click me!", on_click=lambda: ui.notify("Button clicked!")).style(
    "font-size: 1.5em; color: green;"
)

ui.input("Type something:").style("font-size: 1.2em; color: purple;")

ui.button("Submit", on_click=lambda: ui.notify("Submitted!")).style(
    "font-size: 1.5em; color: red;"
)
def shutdown():
    ui.notify("Shutting down...")

ui.button("Close", on_click=shutdown).style("font-size: 1.5em; color: orange;")

ui.run()