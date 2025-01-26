from nicegui import ui

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


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(native=True, dark=True, frameless=False, window_size=(1024, 768))
