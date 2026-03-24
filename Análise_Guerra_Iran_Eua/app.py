# =============================================================================
#  app.py — Ponto de entrada do dashboard + callbacks do chatbot
#
#  Variáveis de ambiente (.env):
#    GOOGLE_API_KEY   — console.cloud.google.com  (Gemini)
#    TAVILY_API_KEY   — app.tavily.com             (busca em tempo real)
#
#  Como executar:
#    python app.py
#    Acesse: http://127.0.0.1:8050
# =============================================================================

import os
from dotenv import load_dotenv
load_dotenv()

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, ctx, ALL

from src.config import COLORS as C, FONT_BODY
from src.data_loader import download_dataset, load_all, compute_kpis
from src.figures import (
    fig_airline_losses, fig_cancellations_trend, fig_reroutes_trend,
    fig_passengers_by_airline, fig_airport_map, fig_airspace_map,
    fig_losses_bubble_map, build_timeline_items,
)
from src.layout import build_css, build_index_string, build_layout
from src.chatbot import build_agent, chat

# ── 1. Dados ──────────────────────────────────────────────────────────────────
dataset_path = download_dataset()
data         = load_all(dataset_path)
kpis         = compute_kpis(data)

# ── 2. Figuras ────────────────────────────────────────────────────────────────
figures = {
    "losses":        fig_airline_losses(data["losses"]),
    "cancellations": fig_cancellations_trend(data["cancel"]),
    "reroutes":      fig_reroutes_trend(data["reroutes"]),
    "passengers":    fig_passengers_by_airline(data["losses"]),
    "airport_map":   fig_airport_map(data["airports"]),
    "airspace_map":  fig_airspace_map(data["airspace"]),
    "losses_map":    fig_losses_bubble_map(data["losses"]),
}
timeline = build_timeline_items(data["timeline"])

# ── 3. Agente LangChain (inicializa uma vez) ──────────────────────────────────
try:
    agent = build_agent()
    print("✅ Agente LangChain (Gemini + Tavily) inicializado")
except Exception as e:
    agent = None
    print(f"⚠️  Agente não inicializado: {e}")
    print("   Verifique GOOGLE_API_KEY e TAVILY_API_KEY no arquivo .env")

# ── 4. App ────────────────────────────────────────────────────────────────────
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title="AviWatch · War Impact 2026",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    index_string=build_index_string(build_css()),
)

app.layout = build_layout(kpis, figures, timeline)


# ── 5. Callbacks do Chatbot ───────────────────────────────────────────────────

def _make_bubble(role: str, text: str) -> html.Div:
    """Cria um balão de mensagem para o chat."""
    icon = "🧑 " if role == "user" else "🤖 "
    return html.Div(
        [html.Span(icon, style={"fontSize": "13px"}), text],
        className=f"chat-bubble {role}",
    )


@app.callback(
    Output("chat-window", "className"),
    Output("chat-open-store", "data"),
    Input("chat-fab-btn",   "n_clicks"),
    Input("chat-close-btn", "n_clicks"),
    State("chat-open-store", "data"),
    prevent_initial_call=True,
)
def toggle_chat(fab_clicks, close_clicks, is_open):
    """Abre e fecha a janela do chatbot."""
    triggered = ctx.triggered_id
    if triggered == "chat-fab-btn":
        new_open = not is_open
    else:
        new_open = False
    cls = "chat-window" if new_open else "chat-window hidden"
    return cls, new_open


@app.callback(
    Output("chat-messages-area",  "children"),
    Output("chat-history-store",  "data"),
    Output("chat-input",          "value"),
    Output("chat-loading-output", "children"),
    Input("chat-send-btn",                    "n_clicks"),
    Input({"type": "chat-suggestion", "index": ALL}, "n_clicks"),
    State("chat-input",          "value"),
    State("chat-history-store",  "data"),
    State("chat-messages-area",  "children"),
    prevent_initial_call=True,
)
def handle_message(send_clicks, suggestion_clicks, user_input, history, current_messages):
    """
    Processa mensagem do usuário (digitada ou sugestão),
    chama o agente LangChain e atualiza o chat.
    """
    triggered = ctx.triggered_id

    # Determina qual mensagem enviar
    message = ""
    if triggered == "chat-send-btn":
        message = (user_input or "").strip()
    elif isinstance(triggered, dict) and triggered.get("type") == "chat-suggestion":
        idx = triggered["index"]
        from src.layout import SUGGESTIONS
        message = SUGGESTIONS[idx]

    if not message:
        return current_messages, history, "", None

    # Adiciona bubble do usuário imediatamente
    messages = list(current_messages or [])
    messages.append(_make_bubble("user", message))

    # Indicador de digitação
    typing_bubble = html.Div(
        [html.Span("🤖 ", style={"fontSize": "13px"}), "Buscando notícias e analisando..."],
        className="chat-bubble typing",
    )
    messages.append(typing_bubble)

    # Chama o agente
    if agent is None:
        response = (
            "⚠️ O agente não está disponível.\n"
            "Verifique se GOOGLE_API_KEY e TAVILY_API_KEY estão configurados no arquivo .env"
        )
        updated_history = history
    else:
        response, updated_history = chat(agent, history or [], message)

    # Remove typing bubble e adiciona resposta real
    messages = [m for m in messages if not (
        hasattr(m, "props") and
        "typing" in str(m.props.get("className", ""))
    )]
    messages.append(_make_bubble("assistant", response))

    return messages, updated_history, "", None


# ── 6. Run ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n🚀 Dashboard iniciando em http://127.0.0.1:8050\n")
    app.run(debug=False, host="0.0.0.0", port=8050, use_reloader=False)
