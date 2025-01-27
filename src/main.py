from nicegui import Client, ui
from nicegui.events import ValueChangeEventArguments
from ollama import AsyncClient, ChatResponse, chat

import home
from ui import UI

# chat()
# ollama = AsyncClient(base_url="http://<remote-server-ip>:11434")
# OLLAMA_HOST
# response: ChatResponse = chat(model='deepseek-r1:32b', messages=[
#   {
#     'role': 'user',
#     'content': 'Why is the sky blue?',
#   },
# ])
# #print(response['message']['content'])
# # or access fields directly from the response object
# print(response.message.content)


class HissApp:
    def __init__(self) -> None:
        self.main_ui = UI()
        self.main_ui.generate_ui()


@ui.page("/")
async def main_page(client: Client) -> None:
    await client.connected()

    app = HissApp()


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(native=True, dark=True, frameless=False, window_size=(1024, 768))
