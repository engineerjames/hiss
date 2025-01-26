from ollama import chat
from ollama import ChatResponse
from ollama import AsyncClient
from nicegui import ui
from nicegui.events import ValueChangeEventArguments

#chat()
#ollama = AsyncClient(base_url="http://<remote-server-ip>:11434")
#OLLAMA_HOST
# response: ChatResponse = chat(model='deepseek-r1:32b', messages=[
#   {
#     'role': 'user',
#     'content': 'Why is the sky blue?',
#   },
# ])
# #print(response['message']['content'])
# # or access fields directly from the response object
# print(response.message.content)

from pages import main_page

if __name__ in { "__main__", "__mp_main__"}:
    ui.run(native=True)
