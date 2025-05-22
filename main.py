from nicegui import ui, app
import asyncio
from agent import get_agent
import sys
import nest_asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

nest_asyncio.apply()

agent_instance = {
    "agent": None,
    "browser": None,
    "playwright": None,
}

@app.on_startup
async def startup():
    print("🚀 Inicializando o agente com navegador...")
    agent, browser, playwright = await get_agent()
    agent_instance["agent"] = agent
    agent_instance["browser"] = browser
    agent_instance["playwright"] = playwright
    print("✅ Agente pronto!")

@app.on_shutdown
async def shutdown():
    print("🛑 Encerrando recursos...")
    if agent_instance["browser"]:
        await agent_instance["browser"].close()
    if agent_instance["playwright"]:
        await agent_instance["playwright"].stop()


@ui.page("/")
async def main_page():
    ui.label("🤖 LlamaScrape Chatbot").classes("text-2xl mb-4")

    messages = ui.column().classes('w-full h-80 overflow-auto border rounded p-2 bg-gray-100')

    def add_message(text, sender="bot"):
        color = "blue" if sender == "user" else "gray"
        alignment = "self-end" if sender == "user" else "self-start"
        messages.clear()
        with messages:
            for msg in chat_history:
                ui.label(msg["text"]).classes(f'{alignment} px-3 py-1 rounded bg-{msg["color"]}-200 mb-1')

    chat_history = []

    input_field = ui.input(placeholder="Digite sua pergunta...").props("clearable").classes("w-full")

    async def handle_question(question: str):
        if not question.strip():
            return
        chat_history.append({"text": question, "color": "blue"})
        add_message(question, "user")
        input_field.value = ""

        agent = agent_instance["agent"]
        if not agent:
            bot_reply = "Erro: agente ainda não foi iniciado."
            chat_history.append({"text": bot_reply, "color": "gray"})
            add_message(bot_reply, "bot")
            return

        bot_reply = "Pesquisando... ⏳"
        chat_history.append({"text": bot_reply, "color": "gray"})
        add_message(bot_reply, "bot")

        await asyncio.sleep(0.5)
        try:
            resposta = await asyncio.to_thread(agent.run, question)
        except Exception as e:
            resposta = f"Erro ao processar: {str(e)}"

        chat_history.append({"text": resposta, "color": "gray"})
        add_message(resposta, "bot")

    input_field.on("keydown.enter", lambda e: asyncio.create_task(handle_question(input_field.value)))

ui.run(title="LlamaScrape Chat", reload=True)
