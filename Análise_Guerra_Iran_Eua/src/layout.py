# =============================================================================
#  layout.py — Componentes de UI e layout principal do Dash
# =============================================================================

from dash import dcc, html

from src.config import COLORS as C, FONT_DISPLAY, FONT_BODY, FONT_MONO


# ── CSS injetado no index_string ──────────────────────────────────────────────

def build_css() -> str:
    return f"""
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

body {{
    background: {C['bg']};
    color: {C['text']};
    font-family: {FONT_BODY};
    font-size: 14px;
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
}}

::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: {C['bg']}; }}
::-webkit-scrollbar-thumb {{ background: {C['border']}; border-radius: 3px; }}
::-webkit-scrollbar-thumb:hover {{ background: {C['text2']}; }}

.sidebar {{
    width: 220px;
    min-height: 100vh;
    background: {C['sidebar']};
    border-right: 1px solid {C['border']};
    position: fixed;
    top: 0; left: 0;
    z-index: 100;
    display: flex;
    flex-direction: column;
}}

.main-content {{
    margin-left: 220px;
    min-height: 100vh;
    background: {C['bg']};
}}

.nav-item {{
    display: flex;
    align-items: center;
    padding: 9px 20px;
    font-size: 12.5px;
    font-weight: 500;
    color: {C['text2']};
    cursor: pointer;
    border-radius: 6px;
    margin: 2px 10px;
    transition: all 0.15s ease;
    font-family: {FONT_BODY};
    text-decoration: none;
}}
.nav-item:hover {{ background: rgba(255,255,255,0.06); color: {C['text']}; }}
.nav-item.active {{
    background: rgba(47,129,247,0.12);
    color: {C['primary']};
    border: 1px solid rgba(47,129,247,0.20);
}}
.nav-icon {{ margin-right: 10px; font-size: 14px; opacity: 0.8; }}

.pulse {{
    width: 7px; height: 7px;
    border-radius: 50%;
    background: {C['danger']};
    animation: pulse 1.8s ease-in-out infinite;
    display: inline-block;
}}
@keyframes pulse {{
    0%, 100% {{ opacity: 1; transform: scale(1); }}
    50%       {{ opacity: 0.5; transform: scale(0.85); }}
}}

.kpi-grid {{
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 12px;
    margin-bottom: 20px;
}}
@media (max-width: 1400px) {{ .kpi-grid {{ grid-template-columns: repeat(3, 1fr); }} }}
@media (max-width: 900px)  {{
    .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }}
    .sidebar  {{ display: none; }}
    .main-content {{ margin-left: 0; }}
}}

.divider {{ height: 1px; background: {C['border']}; margin: 6px 0; }}

/* ── Chatbot Floating ─────────────────────────────────────────────────────── */

.chat-fab {{
    position: fixed;
    bottom: 28px;
    right: 28px;
    width: 52px;
    height: 52px;
    border-radius: 50%;
    background: linear-gradient(135deg, {C['primary']}, #1a4fa8);
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    box-shadow: 0 4px 20px rgba(47,129,247,0.45);
    z-index: 999;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}
.chat-fab:hover {{
    transform: scale(1.08);
    box-shadow: 0 6px 28px rgba(47,129,247,0.60);
}}

.chat-window {{
    position: fixed;
    bottom: 92px;
    right: 28px;
    width: 380px;
    height: 540px;
    background: {C['card']};
    border: 1px solid {C['border']};
    border-radius: 14px;
    box-shadow: 0 16px 48px rgba(0,0,0,0.55);
    display: flex;
    flex-direction: column;
    z-index: 998;
    overflow: hidden;
    transition: opacity 0.2s ease, transform 0.2s ease;
}}
.chat-window.hidden {{
    opacity: 0;
    pointer-events: none;
    transform: translateY(12px) scale(0.97);
}}

.chat-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 16px;
    background: {C['card2']};
    border-bottom: 1px solid {C['border']};
    flex-shrink: 0;
}}

.chat-messages {{
    flex: 1;
    overflow-y: auto;
    padding: 14px 14px 6px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}}

.chat-bubble {{
    max-width: 88%;
    padding: 9px 13px;
    border-radius: 12px;
    font-size: 12.5px;
    line-height: 1.6;
    font-family: {FONT_BODY};
    word-break: break-word;
    white-space: pre-wrap;
}}
.chat-bubble.user {{
    align-self: flex-end;
    background: rgba(47,129,247,0.18);
    border: 1px solid rgba(47,129,247,0.28);
    color: {C['text']};
    border-bottom-right-radius: 3px;
}}
.chat-bubble.assistant {{
    align-self: flex-start;
    background: {C['card2']};
    border: 1px solid {C['border']};
    color: {C['text3']};
    border-bottom-left-radius: 3px;
}}
.chat-bubble.typing {{
    align-self: flex-start;
    background: {C['card2']};
    border: 1px solid {C['border']};
    color: {C['text2']};
    font-style: italic;
    font-size: 12px;
}}

.chat-input-area {{
    display: flex;
    gap: 8px;
    padding: 12px 12px;
    border-top: 1px solid {C['border']};
    flex-shrink: 0;
    background: {C['card']};
}}
.chat-input {{
    flex: 1;
    background: {C['card2']};
    border: 1px solid {C['border']};
    border-radius: 8px;
    color: {C['text']};
    font-family: {FONT_BODY};
    font-size: 12.5px;
    padding: 8px 12px;
    resize: none;
    outline: none;
    transition: border-color 0.15s;
    height: 38px;
    line-height: 1.4;
}}
.chat-input:focus {{
    border-color: {C['primary']};
}}
.chat-send-btn {{
    background: {C['primary']};
    border: none;
    border-radius: 8px;
    color: white;
    cursor: pointer;
    padding: 0 14px;
    font-size: 16px;
    transition: background 0.15s, transform 0.1s;
    flex-shrink: 0;
}}
.chat-send-btn:hover  {{ background: #1a4fa8; }}
.chat-send-btn:active {{ transform: scale(0.95); }}
.chat-send-btn:disabled {{ background: {C['border']}; cursor: not-allowed; }}

.chat-suggestions {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    padding: 8px 14px 2px;
}}
.chat-suggestion-btn {{
    background: rgba(47,129,247,0.10);
    border: 1px solid rgba(47,129,247,0.22);
    border-radius: 20px;
    color: {C['primary']};
    font-size: 11px;
    font-family: {FONT_BODY};
    padding: 4px 10px;
    cursor: pointer;
    transition: background 0.15s;
}}
.chat-suggestion-btn:hover {{ background: rgba(47,129,247,0.22); }}

@media (max-width: 480px) {{
    .chat-window {{ width: calc(100vw - 24px); right: 12px; bottom: 80px; }}
    .chat-fab    {{ right: 16px; bottom: 16px; }}
}}
"""


def build_index_string(css: str) -> str:
    return f"""<!DOCTYPE html>
<html>
<head>
{{%metas%}}
<title>{{%title%}}</title>
{{%favicon%}}
{{%css%}}
<style>{css}</style>
</head>
<body>
{{%app_entry%}}
<footer>{{%config%}}{{%scripts%}}{{%renderer%}}</footer>
</body>
</html>"""


# ── Componentes reutilizáveis ─────────────────────────────────────────────────

def kpi_card(label: str, value: str, sub: str, color: str, icon: str) -> html.Div:
    return html.Div([
        html.Div([
            html.Span(icon, style={"fontSize": "18px"}),
            html.Span(label, style={
                "fontSize": "10px", "fontWeight": "600", "color": C["text2"],
                "fontFamily": FONT_BODY, "textTransform": "uppercase",
                "letterSpacing": "0.07em", "marginLeft": "6px",
            }),
        ], style={"display": "flex", "alignItems": "center", "marginBottom": "10px"}),
        html.Div(value, style={
            "fontSize": "26px", "fontWeight": "700", "color": color,
            "fontFamily": FONT_DISPLAY, "letterSpacing": "-0.02em",
            "lineHeight": "1", "marginBottom": "5px",
        }),
        html.Div(sub, style={
            "fontSize": "11px", "color": C["text2"], "fontFamily": FONT_BODY,
        }),
        html.Div(style={
            "position": "absolute", "bottom": "0", "left": "0", "right": "0",
            "height": "2px", "background": color, "borderRadius": "0 0 8px 8px",
        }),
    ], style={
        "background": C["card"],
        "border": f"1px solid {C['border']}",
        "borderRadius": "8px",
        "padding": "16px 18px 14px",
        "position": "relative",
        "overflow": "hidden",
        "flex": "1",
        "minWidth": "0",
    })


def card(title: str, children, subtitle: str = None) -> html.Div:
    return html.Div([
        html.Div([
            html.Div([
                html.Span(title, style={
                    "fontSize": "13px", "fontWeight": "600", "color": C["text"],
                    "fontFamily": FONT_BODY, "letterSpacing": "-0.01em",
                }),
                html.Span(subtitle, style={
                    "fontSize": "10px", "color": C["text2"],
                    "fontFamily": FONT_BODY, "marginLeft": "10px",
                }) if subtitle else None,
            ], style={"display": "flex", "alignItems": "baseline"}),
        ], style={"padding": "14px 16px 12px", "borderBottom": f"1px solid {C['border']}"}),
        html.Div(children, style={"padding": "12px 10px 10px"}),
    ], style={
        "background": C["card"],
        "border": f"1px solid {C['border']}",
        "borderRadius": "10px",
        "overflow": "hidden",
        "height": "100%",
    })


# ── Sidebar ───────────────────────────────────────────────────────────────────

def build_sidebar() -> html.Div:
    return html.Div([
        # Logo
        html.Div([
            html.Div([
                html.Span("✈", style={"fontSize": "20px", "color": C["primary"]}),
            ], style={
                "width": "36px", "height": "36px",
                "background": "rgba(47,129,247,0.12)",
                "border": "1px solid rgba(47,129,247,0.25)",
                "borderRadius": "8px",
                "display": "flex", "alignItems": "center", "justifyContent": "center",
            }),
            html.Div([
                html.Div("AviWatch", style={
                    "fontSize": "14px", "fontWeight": "700", "color": C["text"],
                    "fontFamily": FONT_DISPLAY, "letterSpacing": "-0.02em",
                }),
                html.Div("War Impact 2026", style={
                    "fontSize": "10px", "color": C["text2"], "fontFamily": FONT_BODY,
                }),
            ], style={"marginLeft": "10px"}),
        ], style={
            "display": "flex", "alignItems": "center",
            "padding": "18px 20px 16px",
            "borderBottom": f"1px solid {C['border']}",
            "marginBottom": "8px",
        }),

        # Badge conflito ativo
        html.Div([
            html.Div([
                html.Span(className="pulse"),
                html.Span("CONFLITO ATIVO", style={
                    "fontSize": "9px", "fontWeight": "700", "color": C["danger"],
                    "letterSpacing": "0.08em", "fontFamily": FONT_BODY,
                }),
            ], style={
                "display": "flex", "alignItems": "center", "gap": "6px",
                "background": "rgba(248,81,73,0.10)",
                "border": "1px solid rgba(248,81,73,0.25)",
                "borderRadius": "6px", "padding": "6px 12px",
                "margin": "0 12px 14px",
            }),
        ]),

        # Navegação
        html.Div([
            html.Div("VISÃO GERAL", style={
                "fontSize": "9px", "fontWeight": "700", "color": C["text2"],
                "letterSpacing": "0.1em", "padding": "4px 20px 6px",
                "fontFamily": FONT_BODY,
            }),
            html.A([html.Span("📊", className="nav-icon"), "Dashboard"],
                   className="nav-item active"),
            html.A([html.Span("🗺️", className="nav-icon"), "Mapas Interativos"],
                   className="nav-item"),
            html.A([html.Span("📉", className="nav-icon"), "Tendências"],
                   className="nav-item"),
        ]),

        html.Div(className="divider", style={"margin": "10px 12px"}),

        html.Div([
            html.Div("ANÁLISES", style={
                "fontSize": "9px", "fontWeight": "700", "color": C["text2"],
                "letterSpacing": "0.1em", "padding": "4px 20px 6px",
                "fontFamily": FONT_BODY,
            }),
            html.A([html.Span("✈", className="nav-icon"), "Companhias Aéreas"],
                   className="nav-item"),
            html.A([html.Span("🏢", className="nav-icon"), "Aeroportos"],
                   className="nav-item"),
            html.A([html.Span("🌍", className="nav-icon"), "Impacto por País"],
                   className="nav-item"),
            html.A([html.Span("📅", className="nav-icon"), "Timeline"],
                   className="nav-item"),
        ]),

        html.Div(className="divider", style={"margin": "10px 12px"}),

        # Rodapé da sidebar
        html.Div([
            html.Div("Fonte dos dados", style={
                "fontSize": "9px", "color": C["text2"], "fontWeight": "600",
                "letterSpacing": "0.06em", "marginBottom": "4px",
                "fontFamily": FONT_BODY,
            }),
            html.Div("Kaggle · zkskhurram", style={
                "fontSize": "10px", "color": C["text2"], "fontFamily": FONT_MONO,
            }),
            html.Div("Jan – Mar 2026", style={
                "fontSize": "10px", "color": C["text2"],
                "fontFamily": FONT_BODY, "marginTop": "2px",
            }),
        ], style={
            "padding": "10px 20px", "marginTop": "auto",
            "borderTop": f"1px solid {C['border']}",
        }),
    ], className="sidebar")


# ── Topbar ────────────────────────────────────────────────────────────────────

def build_topbar() -> html.Div:
    return html.Div([
        html.Div([
            html.Div([
                html.Div("Global Civil Aviation Disruption", style={
                    "fontSize": "11px", "color": C["text2"],
                    "fontFamily": FONT_BODY, "letterSpacing": "0.04em",
                }),
                html.Div("Iran–US War Impact Monitor", style={
                    "fontSize": "20px", "fontWeight": "700", "color": C["text"],
                    "fontFamily": FONT_DISPLAY, "letterSpacing": "-0.03em",
                }),
            ]),
            html.Div([
                html.Div([
                    html.Span("📍", style={"marginRight": "4px"}),
                    html.Span("Oriente Médio · Sul da Ásia · Golfo Pérsico", style={
                        "fontSize": "11px", "color": C["text2"], "fontFamily": FONT_BODY,
                    }),
                ], style={"marginBottom": "4px"}),
                html.Div([
                    html.Span("🗓", style={"marginRight": "4px"}),
                    html.Span("Jan – Mar 2026  ·  Dados: Kaggle", style={
                        "fontSize": "11px", "color": C["text2"], "fontFamily": FONT_BODY,
                    }),
                ]),
            ], style={"textAlign": "right"}),
        ], style={
            "display": "flex", "justifyContent": "space-between",
            "alignItems": "center", "maxWidth": "1600px", "margin": "0 auto",
        }),
    ], style={
        "background": C["sidebar"],
        "borderBottom": f"1px solid {C['border']}",
        "padding": "14px 28px",
    })



# ── Chatbot Floating UI ───────────────────────────────────────────────────────

SUGGESTIONS = [
    "Qual o status atual do conflito?",
    "Quais rotas estão fechadas?",
    "Como as companhias estão reagindo?",
    "Há previsão de cessar-fogo?",
]

def build_chatbot() -> html.Div:
    """
    Floating chatbot button + janela de chat.
    Controlado via callbacks em app.py.
    """
    return html.Div([
        # Store para histórico e estado
        dcc.Store(id="chat-history-store", data=[]),
        dcc.Store(id="chat-open-store",    data=False),

        # Janela de chat
        html.Div([
            # Header
            html.Div([
                html.Div([
                    html.Span("🤖", style={"fontSize": "16px", "marginRight": "8px"}),
                    html.Div([
                        html.Div("AviWatch Intelligence", style={
                            "fontSize": "13px", "fontWeight": "700",
                            "color": C["text"], "fontFamily": FONT_BODY,
                        }),
                        html.Div("Gemini · Notícias em tempo real", style={
                            "fontSize": "10px", "color": C["text2"],
                            "fontFamily": FONT_BODY,
                        }),
                    ]),
                ], style={"display": "flex", "alignItems": "center"}),
                html.Button("✕", id="chat-close-btn", style={
                    "background": "none", "border": "none",
                    "color": C["text2"], "fontSize": "16px",
                    "cursor": "pointer", "padding": "0 2px",
                    "lineHeight": "1",
                }),
            ], className="chat-header"),

            # Mensagens
            html.Div(id="chat-messages-area", className="chat-messages", children=[
                html.Div([
                    html.Span("🤖 ", style={"fontSize": "14px"}),
                    "Olá! Sou o AviWatch Intelligence. Posso te contar tudo sobre o conflito Iran–EUA e seus impactos na aviação — com base nas últimas notícias. O que você quer saber?",
                ], className="chat-bubble assistant"),
            ]),

            # Sugestões rápidas
            html.Div([
                html.Button(s, id={"type": "chat-suggestion", "index": i},
                            className="chat-suggestion-btn", n_clicks=0)
                for i, s in enumerate(SUGGESTIONS)
            ], className="chat-suggestions"),

            # Input
            html.Div([
                dcc.Textarea(
                    id="chat-input",
                    placeholder="Pergunte sobre o conflito, rotas, companhias...",
                    className="chat-input",
                    n_submit=0,
                    debounce=False,
                ),
                html.Button("➤", id="chat-send-btn",
                            className="chat-send-btn", n_clicks=0),
            ], className="chat-input-area"),

            # Loading indicator
            dcc.Loading(
                id="chat-loading",
                type="circle",
                color=C["primary"],
                children=html.Div(id="chat-loading-output"),
                style={"position": "absolute", "bottom": "60px", "left": "50%",
                       "transform": "translateX(-50%)"},
            ),

        ], id="chat-window", className="chat-window hidden"),

        # FAB button
        html.Button("💬", id="chat-fab-btn",
                    className="chat-fab", n_clicks=0,
                    title="AviWatch Intelligence — Notícias em tempo real"),
    ])


# ── Layout principal ──────────────────────────────────────────────────────────

def build_layout(kpis: dict, figures: dict, timeline_items: list) -> html.Div:
    """
    Monta o layout completo do dashboard.

    Parameters
    ----------
    kpis : dict
        Dicionário com os 6 KPIs calculados em data_loader.compute_kpis().
    figures : dict
        Dicionário com as figuras Plotly geradas em figures.py.
    timeline_items : list
        Lista de componentes Dash da timeline.
    """
    C_ = C  # alias local

    return html.Div([
        build_sidebar(),
        html.Div([
            build_topbar(),

            html.Div([

                # ── KPIs ──
                html.Div([
                    kpi_card("Perda Diária Total",
                             f"US$ {kpis['total_loss_usd']/1e6:.0f}M",
                             "Soma das perdas das companhias", C_["danger"], "💸"),
                    kpi_card("Voos Cancelados",
                             f"{kpis['total_cancelled']:,}",
                             "Total no período analisado", C_["warning"], "🚫"),
                    kpi_card("Voos Desviados",
                             f"{kpis['total_rerouted']:,}",
                             "Rotas alternativas adotadas", C_["primary"], "🔀"),
                    kpi_card("Aeroportos Afetados",
                             str(kpis["total_airports_affected"]),
                             "Fechados ou com restrições", C_["purple"], "🏢"),
                    kpi_card("Companhias Impactadas",
                             str(kpis["total_airlines_affected"]),
                             "Com perdas financeiras registradas", C_["success"], "✈"),
                    kpi_card("Espaços Aéreos Fechados",
                             str(kpis["total_airspace_closed"]),
                             "FIRs / UIRs encerrados", C_["orange"], "🚁"),
                ], className="kpi-grid"),

                # ── Mapa aeroportos + Timeline ──
                html.Div([
                    html.Div([
                        card("🗺️  Aeroportos Afetados",
                             dcc.Graph(figure=figures["airport_map"],
                                       config={"displayModeBar": False}),
                             subtitle="Oriente Médio · Sul da Ásia — tamanho ∝ voos afetados"),
                    ], style={"flex": "2", "minWidth": "0"}),
                    html.Div([
                        card("📅  Timeline do Conflito",
                             html.Div(timeline_items,
                                      style={"maxHeight": "390px", "overflowY": "auto",
                                             "paddingRight": "4px"})),
                    ], style={"flex": "1", "minWidth": "280px"}),
                ], style={"display": "flex", "gap": "16px", "marginBottom": "16px"}),

                # ── Tendências ──
                html.Div([
                    html.Div([
                        card("📉  Voos Cancelados por Dia",
                             dcc.Graph(figure=figures["cancellations"],
                                       config={"displayModeBar": False}),
                             subtitle="barras = diário  ·  linha = média 7 dias"),
                    ], style={"flex": "1", "minWidth": "0"}),
                    html.Div([
                        card("🔀  Voos Desviados ao Longo do Tempo",
                             dcc.Graph(figure=figures["reroutes"],
                                       config={"displayModeBar": False}),
                             subtitle="cada ponto = 1 voo redirecionado"),
                    ], style={"flex": "1", "minWidth": "0"}),
                ], style={"display": "flex", "gap": "16px", "marginBottom": "16px"}),

                # ── Perdas + Passageiros ──
                html.Div([
                    html.Div([
                        card("💸  Perdas Financeiras por Companhia",
                             dcc.Graph(figure=figures["losses"],
                                       config={"displayModeBar": False}),
                             subtitle="estimativa diária em USD"),
                    ], style={"flex": "7", "minWidth": "0"}),
                    html.Div([
                        card("👥  Passageiros Afetados",
                             dcc.Graph(figure=figures["passengers"],
                                       config={"displayModeBar": False}),
                             subtitle="top 10 companhias"),
                    ], style={"flex": "5", "minWidth": "0"}),
                ], style={"display": "flex", "gap": "16px", "marginBottom": "16px"}),

                # ── Espaço aéreo + Perdas por país ──
                html.Div([
                    html.Div([
                        card("🚁  Fechamentos de Espaço Aéreo",
                             dcc.Graph(figure=figures["airspace_map"],
                                       config={"displayModeBar": False}),
                             subtitle="FIRs / UIRs · círculos = zonas afetadas · hover = detalhes"),
                    ], style={"flex": "1", "minWidth": "0"}),
                    html.Div([
                        card("🌍  Perdas Financeiras por País",
                             dcc.Graph(figure=figures["losses_map"],
                                       config={"displayModeBar": False}),
                             subtitle="tamanho e cor ∝ US$ perdas diárias"),
                    ], style={"flex": "1", "minWidth": "0"}),
                ], style={"display": "flex", "gap": "16px", "marginBottom": "16px"}),

                # ── Footer ──
                html.Div([
                    html.Span(
                        "✈  AviWatch · Global Civil Aviation Disruption Dashboard 2026",
                        style={"fontWeight": "600", "color": C_["text2"],
                               "fontFamily": FONT_BODY, "fontSize": "11px"},
                    ),
                    html.Span(
                        "  ·  Dados: Kaggle / zkskhurram  ·  Python · Dash · Plotly",
                        style={"color": C_["text2"], "fontFamily": FONT_MONO,
                               "fontSize": "10px"},
                    ),
                ], style={
                    "padding": "16px 0 8px",
                    "borderTop": f"1px solid {C_['border']}",
                    "display": "flex", "alignItems": "center",
                    "gap": "4px", "flexWrap": "wrap",
                }),

            ], style={"padding": "20px 28px"}),
        ], className="main-content"),

        # ── Chatbot Floating ──
        build_chatbot(),
    ])
