"""
Dashboard — Análise de Preços da Gasolina no Brasil (2004–2021)
Autor  : Ivanildo Victor
GitHub : https://github.com/Vict0r-13
Stack  : Python · Dash · Plotly · Pandas
"""

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

# ═══════════════════════════════════════════════════════════════
#  CONFIGURAÇÃO
# ═══════════════════════════════════════════════════════════════

COLORS = {
    "navy":      "#0D1F3C",
    "navy_mid":  "#162B52",
    "electric":  "#2D8CFF",
    "electric2": "#60AEFF",
    "white":     "#FFFFFF",
    "off_white": "#F0F4FB",
    "silver":    "#C8D8F0",
    "text_mid":  "#3A5080",
    "success":   "#22C55E",
    "danger":    "#EF4444",
    "warn":      "#F59E0B",
    "bg":        "#0A1628",
    "card_bg":   "#111E35",
    "card_brd":  "#1E3A6E",
}

PLOTLY_TEMPLATE = dict(
    layout=dict(
        paper_bgcolor=COLORS["card_bg"],
        plot_bgcolor=COLORS["card_bg"],
        font=dict(color=COLORS["silver"], family="Calibri, sans-serif"),
        xaxis=dict(gridcolor="#1E3A6E", zerolinecolor="#1E3A6E"),
        yaxis=dict(gridcolor="#1E3A6E", zerolinecolor="#1E3A6E"),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=COLORS["card_brd"]),
        margin=dict(t=50, r=20, b=40, l=50),
    )
)

# Mapeamento estado → sigla para mapa coroplético
ESTADO_SIGLA = {
    "ACRE": "AC", "ALAGOAS": "AL", "AMAPA": "AP", "AMAZONAS": "AM",
    "BAHIA": "BA", "CEARA": "CE", "DISTRITO FEDERAL": "DF",
    "ESPIRITO SANTO": "ES", "GOIAS": "GO", "MARANHAO": "MA",
    "MATO GROSSO": "MT", "MATO GROSSO DO SUL": "MS", "MINAS GERAIS": "MG",
    "PARA": "PA", "PARAIBA": "PB", "PARANA": "PR", "PERNAMBUCO": "PE",
    "PIAUI": "PI", "RIO DE JANEIRO": "RJ", "RIO GRANDE DO NORTE": "RN",
    "RIO GRANDE DO SUL": "RS", "RONDONIA": "RO", "RORAIMA": "RR",
    "SANTA CATARINA": "SC", "SAO PAULO": "SP", "SERGIPE": "SE",
    "TOCANTINS": "TO",
}

EVENTO_ANOS = {
    2015: "Reajuste PETROBRAS",
    2018: "Greve Caminhoneiros",
    2020: "Pandemia COVID-19",
    2021: "Alta histórica",
}

# ═══════════════════════════════════════════════════════════════
#  CARREGAMENTO E PREPARAÇÃO DOS DADOS
# ═══════════════════════════════════════════════════════════════

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "data_clean.csv")

df = pd.read_csv(DATA_PATH)
df.rename(columns={"VALOR REVENDA (R$/L)": "PRECO"}, inplace=True)
df["DATA"] = pd.to_datetime(df["DATA"])
df["SIGLA"] = df["ESTADO"].map(ESTADO_SIGLA)

# Agregados reutilizados
df_anual    = df.groupby("ANO")["PRECO"].mean().reset_index()
df_estado   = df.groupby(["ESTADO", "SIGLA"])["PRECO"].mean().reset_index().sort_values("PRECO")
df_regiao   = df.groupby("REGIÃO")["PRECO"].mean().reset_index().sort_values("PRECO", ascending=False)
df_anual_est= df.groupby(["ANO", "ESTADO"])["PRECO"].mean().reset_index()

preco_atual  = df_anual.iloc[-1]["PRECO"]
preco_inicio = df_anual.iloc[0]["PRECO"]
variacao_pct = (preco_atual / preco_inicio - 1) * 100
estado_caro  = df_estado.iloc[-1]["ESTADO"].title()
preco_caro   = df_estado.iloc[-1]["PRECO"]
estado_barato= df_estado.iloc[0]["ESTADO"].title()
preco_barato = df_estado.iloc[0]["PRECO"]
estados_opts = [{"label": e.title(), "value": e} for e in sorted(df["ESTADO"].unique())]
anos_opts    = [int(a) for a in sorted(df["ANO"].unique())]

# ═══════════════════════════════════════════════════════════════
#  COMPONENTES UI
# ═══════════════════════════════════════════════════════════════

CARD_STYLE = {
    "backgroundColor": COLORS["card_bg"],
    "border": f"1px solid {COLORS['card_brd']}",
    "borderRadius": "10px",
    "padding": "20px",
    "height": "100%",
}

def kpi_card(title, value, subtitle="", color=None, icon=""):
    clr = color or COLORS["electric"]
    return dbc.Card(
        dbc.CardBody([
            html.P(icon + "  " + title, style={"color": COLORS["silver"], "fontSize": "11px",
                                                 "textTransform": "uppercase", "letterSpacing": "1px",
                                                 "marginBottom": "6px"}),
            html.H3(value, style={"color": clr, "fontWeight": "bold", "marginBottom": "4px"}),
            html.P(subtitle, style={"color": COLORS["text_mid"], "fontSize": "12px", "marginBottom": 0}),
        ]),
        style={**CARD_STYLE, "borderTop": f"3px solid {clr}"},
    )

def section_header(title, subtitle=""):
    return html.Div([
        html.H5(title, style={"color": COLORS["white"], "fontWeight": "bold", "marginBottom": "2px"}),
        html.P(subtitle, style={"color": COLORS["text_mid"], "fontSize": "12px", "marginBottom": "12px"}),
    ])

# ═══════════════════════════════════════════════════════════════
#  LAYOUT
# ═══════════════════════════════════════════════════════════════

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title="Gasolina Brasil · Ivanildo Victor",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server

# ── HEADER ──────────────────────────────────────────────────────
header = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Span("⛽", style={"fontSize": "28px", "marginRight": "12px"}),
                    html.Span("Preços da Gasolina no Brasil",
                              style={"fontSize": "22px", "fontWeight": "bold",
                                     "color": COLORS["white"]}),
                ], style={"display": "flex", "alignItems": "center"}),
                html.P("Série histórica 2004–2021 · 27 estados · 23.570 registros",
                       style={"color": COLORS["silver"], "fontSize": "13px",
                              "marginBottom": 0, "marginTop": "4px"}),
            ], md=8),
            dbc.Col([
                html.Div([
                    html.Span("Ivanildo Victor", style={"color": COLORS["electric"], "fontSize": "13px"}),
                    html.Br(),
                    html.A("github.com/Vict0r-13", href="https://github.com/Vict0r-13",
                           target="_blank", style={"color": COLORS["silver"], "fontSize": "11px"}),
                ], style={"textAlign": "right"}),
            ], md=4),
        ], align="center"),
    ], fluid=True),
], style={
    "background": f"linear-gradient(135deg, {COLORS['navy']} 0%, {COLORS['navy_mid']} 100%)",
    "padding": "18px 0",
    "borderBottom": f"3px solid {COLORS['electric']}",
    "marginBottom": "24px",
})

# ── KPI CARDS ───────────────────────────────────────────────────
kpi_row = dbc.Container([
    dbc.Row([
        dbc.Col(kpi_card(
            "Média Nacional 2021",
            f"R$ {preco_atual:.3f}/L",
            "último ano da série",
            COLORS["electric"], "📊"
        ), md=3, sm=6, className="mb-3"),
        dbc.Col(kpi_card(
            "Variação Total",
            f"+{variacao_pct:.1f}%",
            "de 2004 a 2021",
            COLORS["warn"], "📈"
        ), md=3, sm=6, className="mb-3"),
        dbc.Col(kpi_card(
            "Estado Mais Caro",
            estado_caro,
            f"média R$ {preco_caro:.3f}/L",
            COLORS["danger"], "🔺"
        ), md=3, sm=6, className="mb-3"),
        dbc.Col(kpi_card(
            "Estado Mais Barato",
            estado_barato,
            f"média R$ {preco_barato:.3f}/L",
            COLORS["success"], "🔻"
        ), md=3, sm=6, className="mb-3"),
    ]),
], fluid=True)

# ── TABS ────────────────────────────────────────────────────────
tabs = dbc.Container([
    dbc.Tabs([

        # ── TAB 1: VISÃO GERAL ──────────────────────────────────
        dbc.Tab(label="📈 Visão Geral", tab_id="geral", children=[
            dbc.Row([
                # Gráfico principal: evolução anual
                dbc.Col([
                    html.Div([
                        section_header(
                            "Evolução histórica do preço médio nacional",
                            "Média anual de todos os estados · marcadores em eventos críticos"
                        ),
                        dcc.Graph(id="grafico-anual", config={"displayModeBar": False}),
                    ], style=CARD_STYLE),
                ], md=8, className="mb-3"),

                # Ranking de regiões
                dbc.Col([
                    html.Div([
                        section_header(
                            "Preço médio por região",
                            "Média histórica 2004–2021"
                        ),
                        dcc.Graph(id="grafico-regiao", config={"displayModeBar": False}),
                    ], style=CARD_STYLE),
                ], md=4, className="mb-3"),
            ]),

            # Dois gráficos lado a lado — extremos + variação
            dbc.Row([
                # Esquerda: Top 5 caros vs Top 5 baratos
                dbc.Col([
                    html.Div([
                        section_header(
                            "Extremos de preço por estado",
                            "Top 5 mais caros e Top 5 mais baratos · média histórica 2004–2021"
                        ),
                        dcc.Graph(id="grafico-extremos", config={"displayModeBar": False},
                                  style={"height": "380px"}),
                    ], style=CARD_STYLE),
                ], md=6, className="mb-3"),

                # Direita: Maior variação % total 2004→2021
                dbc.Col([
                    html.Div([
                        section_header(
                            "Quais estados mais encareceram?",
                            "Variação % acumulada do preço de 2004 a 2021 · Top 10"
                        ),
                        dcc.Graph(id="grafico-variacao-total", config={"displayModeBar": False},
                                  style={"height": "380px"}),
                    ], style=CARD_STYLE),
                ], md=6, className="mb-3"),
            ]),
        ]),

        # ── TAB 2: COMPARADOR DE ESTADOS ───────────────────────
        dbc.Tab(label="🗺️ Comparar Estados", tab_id="estados", children=[
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.P("Selecione os estados:", style={"color": COLORS["silver"],
                                                               "fontSize": "12px", "marginBottom": "6px"}),
                        dcc.Dropdown(
                            id="estados-multi",
                            options=estados_opts,
                            value=["SAO PAULO", "CEARA", "ACRE", "PARANA"],
                            multi=True,
                            placeholder="Escolha os estados...",
                            style={"fontSize": "13px"},
                        ),
                    ], style={**CARD_STYLE, "padding": "16px"}),
                ], md=8),
                dbc.Col([
                    html.Div([
                        html.P("Intervalo de anos:", style={"color": COLORS["silver"],
                                                             "fontSize": "12px", "marginBottom": "12px"}),
                        dcc.RangeSlider(
                            id="range-anos",
                            min=anos_opts[0], max=anos_opts[-1],
                            step=1, value=[2004, 2021],
                            marks={a: str(a) for a in anos_opts if a % 4 == 0},
                            tooltip={"always_visible": False, "placement": "bottom"},
                        ),
                    ], style={**CARD_STYLE, "padding": "16px"}),
                ], md=4),
            ], className="mt-3 mb-3"),

            dbc.Row([
                dbc.Col([
                    html.Div([
                        section_header("Evolução temporal por estado", "Série histórica anual"),
                        dcc.Graph(id="grafico-linha", config={"displayModeBar": False}),
                    ], style=CARD_STYLE),
                ], md=8, className="mb-3"),
                dbc.Col([
                    html.Div([
                        section_header("Preço atual vs. média nacional", "Último ano disponível"),
                        dcc.Graph(id="grafico-delta", config={"displayModeBar": False}),
                    ], style=CARD_STYLE),
                ], md=4, className="mb-3"),
            ]),
        ]),

        # ── TAB 3: ANÁLISE REGIONAL ─────────────────────────────
        dbc.Tab(label="🌎 Análise Regional", tab_id="regional", children=[
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.P("Selecione a região:", style={"color": COLORS["silver"],
                                                              "fontSize": "12px", "marginBottom": "6px"}),
                        dcc.Dropdown(
                            id="regiao-select",
                            options=[{"label": r, "value": r} for r in sorted(df["REGIÃO"].unique())],
                            value="NORDESTE",
                            clearable=False,
                            style={"fontSize": "13px"},
                        ),
                    ], style={**CARD_STYLE, "padding": "16px"}),
                ], md=4, className="mt-3 mb-3"),
            ]),

            dbc.Row([
                dbc.Col([
                    html.Div([
                        section_header("Evolução por estado dentro da região",
                                       "Série anual comparativa"),
                        dcc.Graph(id="grafico-regional-linha", config={"displayModeBar": False}),
                    ], style=CARD_STYLE),
                ], md=8, className="mb-3"),
                dbc.Col([
                    html.Div([
                        section_header("Dispersão de preços",
                                       "Box plot: mediana, quartis e outliers"),
                        dcc.Graph(id="grafico-box", config={"displayModeBar": False}),
                    ], style=CARD_STYLE),
                ], md=4, className="mb-3"),
            ]),

            dbc.Row([
                dbc.Col([
                    html.Div([
                        section_header("Variação anual % vs. ano anterior",
                                       "Identifica choques de preço por estado"),
                        dcc.Graph(id="grafico-variacao", config={"displayModeBar": False}),
                    ], style=CARD_STYLE),
                ]),
            ], className="mb-3"),
        ]),

    ], id="tabs", active_tab="geral",
       style={"borderBottom": f"2px solid {COLORS['card_brd']}"},
    ),
], fluid=True)

# ── FOOTER ──────────────────────────────────────────────────────
footer = html.Div([
    html.P(
        ["Fonte: ANP — Agência Nacional do Petróleo, Gás Natural e Biocombustíveis  ·  "
         "Desenvolvido por ", html.A("Ivanildo Victor", href="https://github.com/Vict0r-13",
                                      style={"color": COLORS["electric"]}),
         "  ·  Stack: Python · Dash · Plotly · Pandas"],
        style={"color": COLORS["text_mid"], "fontSize": "11px", "textAlign": "center",
               "margin": "32px 0 16px 0"},
    )
])

app.layout = html.Div([
    header,
    kpi_row,
    tabs,
    footer,
], style={"backgroundColor": COLORS["bg"], "minHeight": "100vh", "fontFamily": "Calibri, sans-serif"})

# ═══════════════════════════════════════════════════════════════
#  CALLBACKS
# ═══════════════════════════════════════════════════════════════

def apply_template(fig):
    """Apply custom dark theme to any plotly figure."""
    fig.update_layout(
        paper_bgcolor=COLORS["card_bg"],
        plot_bgcolor=COLORS["card_bg"],
        font=dict(color=COLORS["silver"], family="Calibri, sans-serif"),
        xaxis=dict(gridcolor=COLORS["card_brd"], zerolinecolor=COLORS["card_brd"]),
        yaxis=dict(gridcolor=COLORS["card_brd"], zerolinecolor=COLORS["card_brd"]),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=40, r=20, b=40, l=60),
    )
    return fig


# ── TAB 1 ── evolução anual ──────────────────────────────────────
@app.callback(Output("grafico-anual", "figure"), Input("tabs", "active_tab"))
def grafico_anual(_):
    media_nacional = df_anual["PRECO"].mean()

    fig = go.Figure()

    # Área de fundo suave
    fig.add_trace(go.Scatter(
        x=df_anual["ANO"], y=df_anual["PRECO"],
        fill="tozeroy", mode="none",
        fillcolor=f"rgba(45,140,255,0.08)",
        showlegend=False,
    ))

    # Linha principal
    fig.add_trace(go.Scatter(
        x=df_anual["ANO"], y=df_anual["PRECO"],
        mode="lines+markers",
        name="Média nacional",
        line=dict(color=COLORS["electric"], width=3),
        marker=dict(size=7, color=COLORS["electric2"]),
        hovertemplate="<b>%{x}</b><br>R$ %{y:.3f}/L<extra></extra>",
    ))

    # Linha de referência — média histórica
    fig.add_hline(
        y=media_nacional, line_dash="dot",
        line_color=COLORS["silver"], opacity=0.5,
        annotation_text=f"Média histórica R$ {media_nacional:.3f}",
        annotation_font_color=COLORS["silver"],
        annotation_font_size=11,
    )

    # Anotações de eventos
    for ano, label in EVENTO_ANOS.items():
        preco = df_anual[df_anual["ANO"] == ano]["PRECO"].values[0]
        fig.add_annotation(
            x=ano, y=preco,
            text=f"⚡ {label}",
            showarrow=True, arrowhead=2,
            arrowcolor=COLORS["warn"], arrowwidth=1.5,
            font=dict(size=10, color=COLORS["warn"]),
            ax=0, ay=-45,
            bgcolor=COLORS["navy_mid"],
            bordercolor=COLORS["warn"],
            borderwidth=1,
        )

    fig.update_xaxes(title_text="Ano", dtick=1)
    fig.update_yaxes(title_text="R$/Litro", tickprefix="R$ ")
    return apply_template(fig)


# ── TAB 1 ── ranking regiões ─────────────────────────────────────
@app.callback(Output("grafico-regiao", "figure"), Input("tabs", "active_tab"))
def grafico_regiao(_):
    colors = [COLORS["danger"] if r == df_regiao["PRECO"].max()
              else COLORS["success"] if r == df_regiao["PRECO"].min()
              else COLORS["electric"] for r in df_regiao["PRECO"]]

    fig = go.Figure(go.Bar(
        x=df_regiao["PRECO"],
        y=df_regiao["REGIÃO"],
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"R$ {v:.3f}" for v in df_regiao["PRECO"]],
        textposition="outside",
        textfont=dict(color=COLORS["silver"], size=11),
        hovertemplate="<b>%{y}</b><br>R$ %{x:.3f}/L<extra></extra>",
    ))

    fig.update_xaxes(visible=False)
    fig.update_yaxes(tickfont=dict(size=12))
    fig.update_layout(showlegend=False, bargap=0.3)
    return apply_template(fig)


# ── TAB 1 ── extremos: top 5 caros + top 5 baratos ──────────────
@app.callback(Output("grafico-extremos", "figure"), Input("tabs", "active_tab"))
def grafico_extremos(_):
    top5_caros   = df_estado.nlargest(5, "PRECO").sort_values("PRECO")
    top5_baratos = df_estado.nsmallest(5, "PRECO").sort_values("PRECO", ascending=False)

    fig = go.Figure()

    # Barras dos mais caros (vermelho)
    fig.add_trace(go.Bar(
        x=top5_caros["PRECO"],
        y=top5_caros["ESTADO"].str.title(),
        orientation="h",
        name="🔺 Mais caros",
        marker=dict(
            color=COLORS["danger"],
            opacity=0.85,
            line=dict(width=0),
        ),
        text=[f"R$ {v:.3f}" for v in top5_caros["PRECO"]],
        textposition="outside",
        textfont=dict(size=11, color=COLORS["danger"]),
        hovertemplate="<b>%{y}</b><br>R$ %{x:.3f}/L<extra></extra>",
    ))

    # Barras dos mais baratos (verde)
    fig.add_trace(go.Bar(
        x=top5_baratos["PRECO"],
        y=top5_baratos["ESTADO"].str.title(),
        orientation="h",
        name="🔻 Mais baratos",
        marker=dict(
            color=COLORS["success"],
            opacity=0.85,
            line=dict(width=0),
        ),
        text=[f"R$ {v:.3f}" for v in top5_baratos["PRECO"]],
        textposition="outside",
        textfont=dict(size=11, color=COLORS["success"]),
        hovertemplate="<b>%{y}</b><br>R$ %{x:.3f}/L<extra></extra>",
    ))

    media = df_estado["PRECO"].mean()
    fig.add_vline(
        x=media, line_dash="dot", line_color=COLORS["warn"], opacity=0.7,
        annotation_text=f"Média R$ {media:.3f}",
        annotation_font_color=COLORS["warn"],
        annotation_font_size=10,
        annotation_position="top right",
    )

    fig.update_xaxes(tickprefix="R$ ", range=[2.5, 3.9])
    fig.update_yaxes(tickfont=dict(size=12, color=COLORS["silver"]))
    fig.update_layout(
        barmode="overlay",
        showlegend=True,
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="right", x=1,
            font=dict(size=11, color=COLORS["silver"]),
        ),
        bargap=0.35,
    )
    return apply_template(fig)


# ── TAB 1 ── variação % acumulada 2004 → 2021 ──────────────────
@app.callback(Output("grafico-variacao-total", "figure"), Input("tabs", "active_tab"))
def grafico_variacao_total(_):
    # Preço de cada estado em 2004 e 2021
    ano_ini = df[df["ANO"] == df["ANO"].min()].groupby("ESTADO")["PRECO"].mean()
    ano_fim = df[df["ANO"] == df["ANO"].max()].groupby("ESTADO")["PRECO"].mean()

    var_df = pd.DataFrame({
        "ESTADO": ano_ini.index,
        "PRECO_INI": ano_ini.values,
        "PRECO_FIM": ano_fim.values,
    })
    var_df["VAR_PCT"] = (var_df["PRECO_FIM"] / var_df["PRECO_INI"] - 1) * 100
    var_df = var_df.sort_values("VAR_PCT", ascending=False).head(10)
    var_df = var_df.sort_values("VAR_PCT", ascending=True)  # menor → maior (barras de baixo p/ cima)

    media_var = var_df["VAR_PCT"].mean()

    # Gradiente de cor: quanto maior a variação, mais intenso o laranja
    max_v = var_df["VAR_PCT"].max()
    min_v = var_df["VAR_PCT"].min()
    bar_colors = [
        f"rgba(239,68,68,{0.5 + 0.5*(v - min_v)/(max_v - min_v + 0.001):.2f})"
        for v in var_df["VAR_PCT"]
    ]

    fig = go.Figure(go.Bar(
        x=var_df["VAR_PCT"],
        y=var_df["ESTADO"].str.title(),
        orientation="h",
        marker=dict(color=bar_colors, line=dict(width=0)),
        text=[f"+{v:.1f}%" for v in var_df["VAR_PCT"]],
        textposition="outside",
        textfont=dict(size=11, color=COLORS["warn"]),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Alta acumulada: +%{x:.1f}%<extra></extra>"
        ),
    ))

    fig.add_vline(
        x=media_var, line_dash="dot", line_color=COLORS["warn"], opacity=0.7,
        annotation_text=f"Média top10: +{media_var:.1f}%",
        annotation_font_color=COLORS["warn"],
        annotation_font_size=10,
        annotation_position="top right",
    )

    fig.update_xaxes(ticksuffix="%", title_text="Variação acumulada 2004 → 2021")
    fig.update_yaxes(tickfont=dict(size=12, color=COLORS["silver"]))
    fig.update_layout(showlegend=False, bargap=0.35)
    return apply_template(fig)


# ── TAB 2 ── linha comparativa ──────────────────────────────────
@app.callback(
    Output("grafico-linha", "figure"),
    Input("estados-multi", "value"),
    Input("range-anos", "value"),
)
def grafico_linha(estados, anos):
    if not estados:
        return go.Figure()

    mask = (df["ESTADO"].isin(estados)) & (df["ANO"] >= anos[0]) & (df["ANO"] <= anos[1])
    dados = df[mask].groupby(["ANO", "ESTADO"])["PRECO"].mean().reset_index()

    palette = px.colors.qualitative.Set2
    fig = go.Figure()

    for i, estado in enumerate(estados):
        d = dados[dados["ESTADO"] == estado]
        fig.add_trace(go.Scatter(
            x=d["ANO"], y=d["PRECO"],
            mode="lines+markers",
            name=estado.title(),
            line=dict(color=palette[i % len(palette)], width=2.5),
            marker=dict(size=6),
            hovertemplate=f"<b>{estado.title()}</b><br>%{{x}}: R$ %{{y:.3f}}/L<extra></extra>",
        ))

    fig.update_xaxes(dtick=2, title_text="Ano")
    fig.update_yaxes(title_text="R$/Litro", tickprefix="R$ ")
    return apply_template(fig)


# ── TAB 2 ── delta vs. média nacional ───────────────────────────
@app.callback(
    Output("grafico-delta", "figure"),
    Input("estados-multi", "value"),
)
def grafico_delta(estados):
    if not estados:
        return go.Figure()

    ano_max  = df["ANO"].max()
    media_nac= df[df["ANO"] == ano_max]["PRECO"].mean()
    dados    = df[(df["ESTADO"].isin(estados)) & (df["ANO"] == ano_max)]
    estado_m = dados.groupby("ESTADO")["PRECO"].mean().reset_index()
    estado_m["DELTA"] = estado_m["PRECO"] - media_nac
    estado_m = estado_m.sort_values("DELTA")

    bar_colors = [COLORS["success"] if d < 0 else COLORS["danger"] for d in estado_m["DELTA"]]

    fig = go.Figure(go.Bar(
        x=estado_m["DELTA"],
        y=estado_m["ESTADO"].str.title(),
        orientation="h",
        marker=dict(color=bar_colors),
        text=[f"{'+' if d >= 0 else ''}{d:.3f}" for d in estado_m["DELTA"]],
        textposition="outside",
        textfont=dict(size=10, color=COLORS["silver"]),
        hovertemplate="<b>%{y}</b><br>Desvio: R$ %{x:.3f}/L<extra></extra>",
    ))

    fig.add_vline(x=0, line_color=COLORS["warn"], line_width=1.5)
    fig.update_layout(
        title=dict(text=f"Desvio em relação à média nacional ({ano_max})<br>"
                        f"<span style='font-size:11px;color:{COLORS['silver']}'>Média: R$ {media_nac:.3f}/L</span>",
                   font=dict(size=13, color=COLORS["white"])),
        showlegend=False,
    )
    return apply_template(fig)


# ── TAB 3 ── linha regional ─────────────────────────────────────
@app.callback(
    Output("grafico-regional-linha", "figure"),
    Input("regiao-select", "value"),
)
def grafico_regional_linha(regiao):
    dados = df[df["REGIÃO"] == regiao].groupby(["ANO", "ESTADO"])["PRECO"].mean().reset_index()
    palette = px.colors.qualitative.Set2

    fig = go.Figure()
    for i, estado in enumerate(dados["ESTADO"].unique()):
        d = dados[dados["ESTADO"] == estado]
        fig.add_trace(go.Scatter(
            x=d["ANO"], y=d["PRECO"],
            mode="lines+markers",
            name=estado.title(),
            line=dict(color=palette[i % len(palette)], width=2),
            marker=dict(size=5),
            hovertemplate=f"<b>{estado.title()}</b><br>%{{x}}: R$ %{{y:.3f}}<extra></extra>",
        ))

    fig.update_xaxes(dtick=2)
    fig.update_yaxes(tickprefix="R$ ")
    return apply_template(fig)


# ── TAB 3 ── box plot ────────────────────────────────────────────
@app.callback(Output("grafico-box", "figure"), Input("regiao-select", "value"))
def grafico_box(regiao):
    dados = df[df["REGIÃO"] == regiao]

    fig = go.Figure()
    for estado in sorted(dados["ESTADO"].unique()):
        d = dados[dados["ESTADO"] == estado]["PRECO"]
        fig.add_trace(go.Box(
            y=d,
            name=estado.title()[:10],
            marker_color=COLORS["electric"],
            line_color=COLORS["electric2"],
            boxmean=True,
        ))

    fig.update_yaxes(tickprefix="R$ ")
    fig.update_layout(showlegend=False)
    return apply_template(fig)


# ── TAB 3 ── variação % anual ────────────────────────────────────
@app.callback(Output("grafico-variacao", "figure"), Input("regiao-select", "value"))
def grafico_variacao(regiao):
    dados = df[df["REGIÃO"] == regiao].groupby(["ANO", "ESTADO"])["PRECO"].mean().reset_index()
    dados = dados.sort_values(["ESTADO", "ANO"])
    dados["VAR_PCT"] = dados.groupby("ESTADO")["PRECO"].pct_change() * 100
    dados = dados.dropna()

    palette = px.colors.qualitative.Set2
    fig = go.Figure()

    for i, estado in enumerate(dados["ESTADO"].unique()):
        d = dados[dados["ESTADO"] == estado]
        fig.add_trace(go.Bar(
            x=d["ANO"], y=d["VAR_PCT"],
            name=estado.title(),
            marker_color=palette[i % len(palette)],
            hovertemplate=f"<b>{estado.title()}</b><br>%{{x}}: %{{y:+.1f}}%<extra></extra>",
        ))

    fig.add_hline(y=0, line_color=COLORS["silver"], line_width=1)
    fig.update_layout(barmode="group")
    fig.update_xaxes(dtick=2)
    fig.update_yaxes(ticksuffix="%", title_text="Variação % a.a.")
    return apply_template(fig)


# ═══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app.run(debug=True, port=8050)
