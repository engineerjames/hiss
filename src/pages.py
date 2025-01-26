from nicegui import ui

@ui.page('/')
def main_page() -> None:
    ui.label('CONTENT')
    [ui.label(f'Line {i}') for i in range(50)]
    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
        ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat color=white')
        ui.label('HEADER')
    with ui.left_drawer(fixed=True, top_corner=True, bottom_corner=True, elevated=True).style('background-color: #ebf1fa').props('bordered').classes("lg:hidden") as right_drawer:
        ui.label('RIGHT DRAWER')
    with ui.footer().style('background-color: #3874c8'):
        ui.label('FOOTER')