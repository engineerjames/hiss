from nicegui import Client, ui


class UI:
    def __init__(self) -> None:
        self.current_path = "/"
        self.home_button: ui.button | None = None
        self.settings_button: ui.button | None = None

    def generate_ui(self, client: Client) -> None:
        self.current_path = client.page.path

        with ui.header().style("background-color: #3874c8").classes("items-center"):
            ui.button(on_click=lambda: left_drawer.toggle(), icon="menu").props("flat color=white")
            ui.label("hiss").classes("text-center lg:text-xl font-bold font-sans")
        with (
            ui.left_drawer(bordered=True).props("width=auto") as left_drawer,
            ui.column().classes("w-auto content-start"),
        ):
            self.home_button = (
                ui.button(
                    "Home",
                    color="primary" if self.current_path == "/" else None,
                    icon="home",
                    on_click=lambda: ui.navigate.to("/"),
                )
                .props("flat align=left")
                .classes("w-full")
            )

            self.settings_button = (
                ui.button(
                    "Settings",
                    color="primary" if self.current_path == "/settings" else None,
                    icon="settings",
                    on_click=lambda: ui.navigate.to("/settings"),
                )
                .props("flat align=left")
                .classes("w-full")
            )
