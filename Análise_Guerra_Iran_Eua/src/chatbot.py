# =============================================================================
#  chatbot.py — Chatbot com LangChain + Gemini + Tavily Search
#
#  Variáveis de ambiente necessárias (.env):
#    GOOGLE_API_KEY   — console.cloud.google.com (Gemini)
#    TAVILY_API_KEY   — app.tavily.com (busca em tempo real)
# =============================================================================

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage


# ── Prompt do sistema ─────────────────────────────────────────────────────────

SYSTEM_PROMPT = """Você é o AviWatch Intelligence, um analista especializado em \
aviação civil e geopolítica do Oriente Médio.

Seu foco principal é o conflito Iran–EUA de 2026 e seus impactos na aviação civil global.

Quando o usuário fizer uma pergunta:
1. Use a ferramenta de busca para encontrar as notícias mais recentes e relevantes.
2. Cruze as informações encontradas com o contexto do dashboard:
   - 680+ voos cancelados, 420+ desviados
   - US$ 48,8M em perdas diárias
   - Fechamentos de FIRs/UIRs no Golfo Pérsico
   - Aeroportos críticos: IKA (Tehran), BGW (Baghdad), BEY (Beirut)
3. Responda de forma clara, objetiva e em português do Brasil.
4. Sempre cite a fonte das notícias quando disponível.
5. Separe fatos confirmados de especulações.

Tópicos que você domina:
- Operações de espaço aéreo (FIR, UIR, NOTAM, espaço aéreo restrito)
- Impacto financeiro em companhias aéreas
- Rotas alternativas e desvios
- Histórico do conflito Iran–EUA
- Segurança de voos em zonas de conflito
- Acordos e negociações de paz relacionados à aviação

Seja direto, use dados quando possível e mantenha um tom analítico e profissional.
Se não encontrar informações recentes, diga isso claramente e ofereça contexto histórico."""


# ── Inicialização do agente ───────────────────────────────────────────────────

def build_agent() -> AgentExecutor:
    """
    Constrói e retorna o AgentExecutor com:
    - LLM: Gemini 1.5 Flash (rápido e eficiente)
    - Tool: Tavily Search (notícias em tempo real)
    - Memória: histórico de mensagens por sessão
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.environ["GOOGLE_API_KEY"],
        temperature=0.3,
        max_output_tokens=1024,
    )

    search_tool = TavilySearch(
        max_results=5,
        tavily_api_key=os.environ["TAVILY_API_KEY"],
        search_depth="advanced",
        include_answer=True,
        include_raw_content=False,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, [search_tool], prompt)

    return AgentExecutor(
        agent=agent,
        tools=[search_tool],
        verbose=False,
        max_iterations=3,
        handle_parsing_errors=True,
    )


def chat(agent: AgentExecutor, history: list[dict], user_message: str) -> tuple[str, list[dict]]:
    """
    Executa uma rodada de conversa com o agente.

    Parameters
    ----------
    agent   : AgentExecutor já inicializado
    history : lista de {'role': 'user'|'assistant', 'content': str}
    user_message : mensagem do usuário

    Returns
    -------
    (resposta_str, history_atualizado)
    """
    # Converte histórico para formato LangChain
    lc_history = []
    for msg in history:
        if msg["role"] == "user":
            lc_history.append(HumanMessage(content=msg["content"]))
        else:
            lc_history.append(AIMessage(content=msg["content"]))

    try:
        result = agent.invoke({
            "input": user_message,
            "chat_history": lc_history,
        })
        response = result.get("output", "Não consegui processar sua pergunta. Tente novamente.")
    except Exception as e:
        response = f"⚠️ Erro ao consultar o agente: {str(e)[:200]}"

    # Atualiza histórico
    updated_history = history + [
        {"role": "user",      "content": user_message},
        {"role": "assistant", "content": response},
    ]

    return response, updated_history
