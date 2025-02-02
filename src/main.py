import datetime
import logging
from asyncio.tasks import Task, create_task
from collections.abc import AsyncIterator
from typing import Any

from nicegui import Client, ui
from ollama import AsyncClient, ChatResponse, ListResponse, Message

messages: list[tuple[str, str, str]] = []


@ui.refreshable
def chat_messages(client_id: str) -> None:
    if messages:
        for text, stamp, sent_id in messages:
            ui.chat_message(text=text, stamp=stamp, sent=sent_id == client_id)
    else:
        ui.label("No messages yet").classes("mx-auto my-36")
    ui.run_javascript("window.scrollTo(0, document.body.scrollHeight)")


async def get_models() -> ListResponse:
    ollama = AsyncClient(host="10.0.0.10")
    return await ollama.list()


async def get_response(text: str, model_name: str) -> AsyncIterator[ChatResponse]:
    ollama = AsyncClient(host="10.0.0.10")
    async for response in await ollama.chat(
        model=model_name,
        stream=True,
        messages=[Message(role="user", content=text)],
    ):
        yield response


async def process_response(text: str, model_name: str) -> None:
    is_thinking = False
    messages.append(("", datetime.datetime.now(tz=datetime.UTC).strftime("%X"), "ollama"))

    message_content = ""
    async for response in get_response(text, model_name):
        content = response.message.content
        if not content:
            continue

        content = content.lstrip("\n")

        if content.strip() == "<think>":
            is_thinking = True
            messages[-1] = ("Thinking...", messages[-1][1], messages[-1][2])
        elif content.strip() == "</think>":
            is_thinking = False
        elif not is_thinking:
            message_content += content
            messages[-1] = (message_content, messages[-1][1], messages[-1][2])

        chat_messages.refresh()


class State:
    selected_model_name: str | None = None


id_to_state: dict[str, State] = {}
chat_tasks: set[Task[Any]] = set()


@ui.page("/")
async def main_page(client: Client) -> None:
    def send(text: ui.input) -> None:
        if not text.value:
            return

        if text.value.lower() == "/clear":
            messages.clear()
            chat_messages.refresh()
            return

        stamp = datetime.datetime.now(tz=datetime.UTC).strftime("%X")
        messages.append((text.value, stamp, ui.context.client.id))

        client_state = id_to_state[ui.context.client.id]
        if not client_state.selected_model_name:
            messages.append(("Please select a model", stamp, "ollama"))
            chat_messages.refresh()
            return

        chat_tasks.add(create_task(process_response(text.value, client_state.selected_model_name)))
        text.value = ""
        chat_messages.refresh()

    with ui.header().classes("flex items-center justify-between"):
        ui.label("hiss").classes("lg:text-xl font-bold font-sans vertical-align")

        ui.space()

        ui.button().props("flat color=white icon=settings").classes("ml-auto").on_click(
            lambda: right_drawer.toggle(),  # type: ignore[has-type]
        )

    with ui.right_drawer(value=False, bordered=True) as right_drawer:
        ui.label("Loading model list...").classes("text-center")
        ui.skeleton("rect").classes("w-64")

        ui.add_css(r"a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}")
    with ui.row().classes("w-full no-wrap items-center"):
        text = (
            ui.input(placeholder="What would you like to know?").props("outlined input-class=mx-3").classes("flex-grow")
        )
        text.on("keydown.enter", lambda: send(text))

    await client.connected()

    with ui.column().classes("w-full max-w-2xl mx-auto items-stretch"):
        chat_messages(ui.context.client.id)

    if ui.context.client.id not in id_to_state:
        id_to_state[ui.context.client.id] = State()

    client_state = id_to_state[ui.context.client.id]

    models = await get_models()

    right_drawer.clear()
    with right_drawer:
        ui.select(options=[m.model for m in models.models], label="Model").classes("w-64").bind_value_to(
            client_state,
            "selected_model_name",
        )


async def test_run() -> None:
    models = await get_models()
    the_model = models.models[0].model

    if the_model is None:
        logger.error("No model found")
        return

    is_thinking = False
    async for response in get_response("What is 1+1?", the_model):
        content = response.message.content
        if not content:
            continue

        if content.strip() == "<think>":
            is_thinking = True
        elif content.strip() == "</think>":
            is_thinking = False
        elif not is_thinking:
            logger.info(content)


if __name__ in {"__main__", "__mp_main__"}:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    ui.run(native=True, dark=True, frameless=False, window_size=(1024, 768))
