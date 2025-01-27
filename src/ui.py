from typing import Literal

from nicegui import ui


def _get_settings_content() -> None:
    ui.label("Settings").classes("text-lg font-bold")


def _get_main_content() -> None:
    ui.label("Main").classes("text-lg font-bold")


@ui.refreshable
def _get_content(current_view: Literal["settings", "main"]) -> None:
    with ui.column():
        if current_view == "settings":
            _get_settings_content()
        elif current_view == "main":
            _get_main_content()


class UI:
    def __init__(self) -> None:
        self.current_view: Literal["settings", "main"] = "main"
        self.settings_drawer = ui.right_drawer(value=False, bordered=True)

    def generate_ui(self) -> None:
        with ui.header().classes("flex items-center justify-between"):
            ui.label("hiss").classes("lg:text-xl font-bold font-sans vertical-align")

            ui.space()

            ui.button().props("flat color=white icon=settings").classes("ml-auto").on_click(
                lambda: self.settings_drawer.toggle(),
            )

        with self.settings_drawer:
            ui.select(["Fun", "Zoos"], label="Model").classes("w-64")

        _get_content(self.current_view)
