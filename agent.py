from playwright.async_api import async_playwright
from langchain.agents import AgentType, initialize_agent
from langchain_community.agent_toolkits.playwright.toolkit import PlayWrightBrowserToolkit
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain_community.llms import HuggingFacePipeline


import torch # type: ignore

async def create_browser():
    playwright = await async_playwright().start()
    browser = await create_sync_playwright_browser()
    context = await browser.new_context()
    page = await context.new_page()
    return browser, page, playwright

def load_local_llm():
    model_id = "google/flan-t5-large"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

    pipe = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
        device=0 if torch.cuda.is_available() else -1,
        max_new_tokens=256,
    )

    return HuggingFacePipeline(pipeline=pipe)

async def get_agent():
    print("🌐 Iniciando criação do navegador...")
    browser, page, playwright = await create_browser()
    print("✅ Navegador criado!")

    toolkit = PlaywrightBrowserToolkit.from_browser(browser=browser, page=page)  # type: ignore
    tools = toolkit.get_tools()
    print("🧰 Ferramentas carregadas!")

    llm = load_local_llm()
    print("🧠 Modelo carregado!")

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    print("✅ Agente criado com sucesso!")
    return agent, browser, playwright
