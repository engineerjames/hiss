from nicegui import Client, ui

from ui import UI


@ui.page("/")
async def main_page(client: Client) -> None:
    await client.connected()

    interface = UI()

    interface.generate_ui(client)


@ui.page("/settings")
async def settings_page(client: Client) -> None:
    await client.connected()

    interface = UI()

    interface.generate_ui(client)
