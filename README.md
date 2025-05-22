
# LlamaScrape Async 🦙🌐

Este projeto é uma prova de conceito (PoC) que integra um modelo de linguagem local da Hugging Face com ferramentas de automação de navegador fornecidas pela biblioteca Playwright, tudo envolvido em uma interface amigável com o NiceGUI.

O objetivo principal é permitir a um agente de linguagem natural controlar um navegador de forma autônoma para buscar informações, realizar raspagens e interagir com páginas da web, com uma interface web simples para fins educacionais e de diversão pessoal.

## Tecnologias Utilizadas

- [LangChain](https://python.langchain.com/) (Community)
- [Transformers - HuggingFace](https://huggingface.co/transformers/)
- [Playwright](https://playwright.dev/python/)
- [NiceGUI](https://nicegui.io/)
- [Google FLAN-T5 Large](https://huggingface.co/google/flan-t5-large)

## Como rodar

```bash
python -m venv .venv
.venv\Scripts\activate # Windows
pip install -r requirements.txt
python main.py
```

Acesse: [http://localhost:8080](http://localhost:8080)

## Dificuldades Encontradas e Soluções

### 1. Erro ao iniciar o Playwright com NiceGUI (AsyncIO)
**Erro:** `NotImplementedError` ao usar `asyncio.create_subprocess_exec` no Windows.

**Causa:** O loop de evento padrão no Windows para alguns contextos (como dentro de GUIs como NiceGUI) não suporta subprocessos nativamente.

**Solução:**
- Foi aplicado `nest_asyncio.apply()` para habilitar reentrância no loop do asyncio.
- Definido `WindowsSelectorEventLoopPolicy()` no início do script.

### 2. Execução correta dos testes isolados de Playwright
**Diagnóstico:** Um script de teste separado (`test_playwright_loop.py`) foi criado para verificar se a execução do Playwright de forma isolada estava funcional no ambiente.

**Solução:** O script foi rodado com sucesso, confirmando que o Playwright funciona fora do NiceGUI.

## Objetivo do Projeto

- Permitir a interação com um agente LLM que consegue navegar em uma página por vez.
- Aprender a integrar um modelo LLM local com navegador.
- Construir uma interface básica mas funcional para testes pessoais e estudos.

## Futuras Melhorias

- Adicionar opção de alternar entre o modo `async` e `sync`.
- Permitir execuções de comandos em lote (multi-páginas).
- Substituir FLAN-T5 por outro modelo local com maior capacidade ou fine-tuned.

## Autor
Jaime Martins Oliveira
