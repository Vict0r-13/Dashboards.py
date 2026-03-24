# =============================================================================
#  figures.py — Todas as figuras Plotly do dashboard
# =============================================================================

import pandas as pd
import plotly.graph_objects as go

from src.config import (
    COLORS as C, FONT_BODY, FONT_MONO,
    COUNTRY_COORDS, SEVERITY_COLORS, AIRSPACE_STATUS_COLORS,
)
from src.data_loader import enrich_coords, resolve_coords

# ── Helper de layout ──────────────────────────────────────────────────────────

def _apply_layout(
    fig: go.Figure,
    height: int,
    margin: dict = None,
    barmode: str = None,
    legend_override: dict = None,
) -> None:
    """Aplica o design system dark ao layout de uma figura Plotly."""
    base_legend = dict(bgcolor="rgba(0,0,0,0)", font=dict(color=C["text2"]))
    if legend_override:
        base_legend.update(legend_override)

    kw = dict(
        plot_bgcolor=C["card"],
        paper_bgcolor=C["card"],
        font=dict(family=FONT_BODY, color=C["text2"], size=11),
        legend=base_legend,
        hoverlabel=dict(
            bgcolor=C["card2"], font_color=C["text"], bordercolor=C["border"]
        ),
        height=height,
        margin=margin or dict(l=12, r=12, t=8, b=40),
    )
    if barmode:
        kw["barmode"] = barmode

    fig.update_layout(**kw)
    fig.update_xaxes(
        gridcolor=C["border"], showline=False,
        color=C["text2"], tickfont=dict(color=C["text2"]),
    )
    fig.update_yaxes(
        gridcolor=C["border"], showline=False,
        color=C["text2"], tickfont=dict(color=C["text2"]),
    )


def _mapbox_base_layout(height: int, center_lat: float, center_lon: float, zoom: float) -> dict:
    """Retorna o dict de layout padrão para figuras Scattermapbox."""
    return dict(
        mapbox=dict(
            style="carto-darkmatter",
            center=dict(lat=center_lat, lon=center_lon),
            zoom=zoom,
        ),
        paper_bgcolor=C["card"],
        height=height,
        font=dict(family=FONT_BODY, color=C["text2"], size=10),
        legend=dict(
            orientation="h", y=-0.05, x=0.5, xanchor="center",
            bgcolor="rgba(0,0,0,0)", font=dict(color=C["text2"], size=10),
        ),
        margin=dict(l=0, r=0, t=4, b=4),
        hoverlabel=dict(
            bgcolor=C["card2"], font_color=C["text"], bordercolor=C["border"]
        ),
    )


# ── Gráficos de tendência ─────────────────────────────────────────────────────

def fig_airline_losses(df_losses: pd.DataFrame) -> go.Figure:
    """Barras horizontais — perdas financeiras diárias por companhia."""
    if df_losses.empty or "estimated_daily_loss_usd" not in df_losses.columns:
        return go.Figure()

    df = df_losses.sort_values("estimated_daily_loss_usd", ascending=True).tail(12)
    vals = df["estimated_daily_loss_usd"]
    norm = (vals - vals.min()) / (vals.max() - vals.min() + 1)
    colors = [f"rgba(248,81,73,{0.35 + 0.65*n:.2f})" for n in norm]

    fig = go.Figure(go.Bar(
        x=vals / 1e6, y=df["airline"], orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"${v/1e6:.1f}M" for v in vals],
        textposition="outside",
        textfont=dict(color=C["text2"], size=10),
        hovertemplate="<b>%{y}</b><br>Perda: US$ %{x:.2f}M/dia<extra></extra>",
    ))
    _apply_layout(fig, height=330, margin=dict(l=10, r=55, t=8, b=35))
    fig.update_xaxes(title="US$ Milhões/dia", tickprefix="$")
    fig.update_yaxes(tickfont=dict(size=10, color=C["text3"]))
    return fig


def fig_cancellations_trend(df_cancel: pd.DataFrame) -> go.Figure:
    """Barras + linha MA7 — cancelamentos diários de voos."""
    if df_cancel.empty:
        return go.Figure()

    df = df_cancel.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    daily = df.groupby("date").size().reset_index(name="n").sort_values("date")
    daily["ma7"] = daily["n"].rolling(7, min_periods=1).mean()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=daily["date"], y=daily["n"], name="Cancelamentos",
        marker_color="rgba(248,81,73,0.18)",
        hovertemplate="%{x|%d/%m/%y}: <b>%{y}</b> voos<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=daily["date"], y=daily["ma7"], name="Média 7 dias",
        line=dict(color=C["danger"], width=2),
        hovertemplate="MA7: <b>%{y:.0f}</b><extra></extra>",
    ))
    _apply_layout(
        fig, height=240, margin=dict(l=12, r=12, t=5, b=35),
        barmode="overlay",
        legend_override=dict(orientation="h", y=1.08, x=1, xanchor="right"),
    )
    fig.update_yaxes(title="Voos cancelados")
    return fig


def fig_reroutes_trend(df_reroutes: pd.DataFrame) -> go.Figure:
    """Área preenchida — voos desviados ao longo do tempo."""
    if df_reroutes.empty:
        return go.Figure()

    df = df_reroutes.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    daily = df.groupby("date").size().reset_index(name="n").sort_values("date")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily["date"], y=daily["n"], name="Voos Desviados",
        fill="tozeroy", fillcolor="rgba(47,129,247,0.10)",
        line=dict(color=C["primary"], width=2),
        hovertemplate="%{x|%d/%m/%y}: <b>%{y}</b> voos<extra></extra>",
    ))
    _apply_layout(fig, height=220, margin=dict(l=12, r=12, t=5, b=35))
    fig.update_yaxes(title="Voos desviados")
    return fig


def fig_passengers_by_airline(df_losses: pd.DataFrame) -> go.Figure:
    """Barras verticais — passageiros afetados por companhia."""
    if df_losses.empty or "passengers_impacted" not in df_losses.columns:
        return go.Figure()

    df = df_losses.sort_values("passengers_impacted", ascending=False).head(10)
    vals = df["passengers_impacted"]
    norm = (vals - vals.min()) / (vals.max() - vals.min() + 1)
    colors = [f"rgba(47,129,247,{0.3 + 0.7*n:.2f})" for n in norm]

    fig = go.Figure(go.Bar(
        x=df["airline"], y=vals,
        marker=dict(color=colors, line=dict(width=0)),
        hovertemplate="<b>%{x}</b><br>Passageiros: %{y:,.0f}<extra></extra>",
    ))
    _apply_layout(fig, height=245, margin=dict(l=12, r=12, t=8, b=65))
    fig.update_yaxes(title="Passageiros afetados")
    fig.update_xaxes(tickangle=-38, tickfont=dict(size=9, color=C["text2"]))
    return fig


# ── Mapas ─────────────────────────────────────────────────────────────────────

def fig_airport_map(df_airports: pd.DataFrame) -> go.Figure:
    """
    Mapa interativo de aeroportos afetados.
    Usa Scattermapbox com tile carto-darkmatter.
    Tamanho dos marcadores proporcional aos voos afetados.
    """
    if df_airports.empty:
        return go.Figure()

    df = resolve_coords(df_airports.copy())
    df_valid = df.dropna(subset=["lat", "lon"])

    sev_col = "severity_level" if "severity_level" in df_valid.columns else None
    severity_vals = (
        df_valid[sev_col]
        if sev_col
        else pd.Series(["Low"] * len(df_valid), index=df_valid.index)
    )

    fc_col = "flights_affected" if "flights_affected" in df_valid.columns else None
    sizes = [14.0] * len(df_valid)
    if fc_col:
        fc = pd.to_numeric(df_valid[fc_col], errors="coerce").fillna(30)
        if fc.max() > 0:
            sizes = (8 + (fc / fc.max()) * 22).tolist()

    fig = go.Figure()

    # Zona de conflito — dois anéis concêntricos sobre o Irã
    fig.add_trace(go.Scattermapbox(
        lon=[51.39], lat=[35.69], mode="markers",
        marker=dict(size=42, color="rgba(248,81,73,0.12)"),
        name="🔴 Zona de Conflito (Irã)",
        hovertemplate="<b>Zona de Conflito — Irã</b><br>Espaço aéreo fechado<extra></extra>",
    ))
    fig.add_trace(go.Scattermapbox(
        lon=[51.39], lat=[35.69], mode="markers",
        marker=dict(size=22, color="rgba(248,81,73,0.30)"),
        showlegend=False, hoverinfo="skip",
    ))

    for sev, color in SEVERITY_COLORS.items():
        mask = severity_vals == sev
        if not mask.any():
            continue
        sub = df_valid[mask]
        idx_list = [i for i, v in enumerate(mask) if v]
        sub_sizes = [sizes[i] for i in idx_list]
        hover_texts = [
            f"<b>{row.get('airport_name', '')}</b> ({row.get('iata_code', '')})<br>"
            f"País: {row.get('country', '')}<br>"
            f"Severidade: {sev}<br>"
            f"Voos afetados: {row.get('flights_affected', '')}"
            for _, row in sub.iterrows()
        ]
        fig.add_trace(go.Scattermapbox(
            lon=sub["lon"].tolist(), lat=sub["lat"].tolist(),
            mode="markers", name=sev,
            marker=dict(size=sub_sizes, color=color, opacity=0.9),
            text=hover_texts,
            hovertemplate="%{text}<extra></extra>",
        ))

    fig.update_layout(**_mapbox_base_layout(400, 28, 52, 3.6))
    return fig


def fig_airspace_map(df_airspace: pd.DataFrame) -> go.Figure:
    """
    Mapa de fechamentos e restrições de espaço aéreo (FIRs/UIRs).
    Status derivado das datas de fechamento.
    """
    if df_airspace.empty:
        return go.Figure()

    df = enrich_coords(df_airspace.copy(), "country", COUNTRY_COORDS)
    df_valid = df.dropna(subset=["lat", "lon"]).copy()

    now = pd.Timestamp.now()
    if "closure_end_date" in df_valid.columns:
        df_valid["end_dt"] = pd.to_datetime(df_valid["closure_end_date"], errors="coerce")
        df_valid["status"] = df_valid["end_dt"].apply(
            lambda x: "Fechado" if pd.isna(x) or x > now else "NOTAM Ativo"
        )
    else:
        df_valid["status"] = "Fechado"

    name_col = "airspace_zone" if "airspace_zone" in df_valid.columns else "country"
    fig = go.Figure()

    for status, (color, sz) in AIRSPACE_STATUS_COLORS.items():
        mask = df_valid["status"] == status
        if not mask.any():
            continue
        sub = df_valid[mask]
        hover_texts = [
            f"<b>{row.get('airspace_zone', row.get('country', ''))}</b><br>"
            f"País: {row.get('country', '')}<br>"
            f"Status: {status}<br>"
            f"Voos afetados: {row.get('flights_affected', '')}<br>"
            f"Motivo: {str(row.get('reason', ''))[:60]}"
            for _, row in sub.iterrows()
        ]
        # Halo externo semitransparente
        fig.add_trace(go.Scattermapbox(
            lon=sub["lon"].tolist(), lat=sub["lat"].tolist(),
            mode="markers", name=status,
            marker=dict(size=sz * 2, color=color, opacity=0.15),
            showlegend=False, hoverinfo="skip",
        ))
        # Marcador principal com rótulo
        fig.add_trace(go.Scattermapbox(
            lon=sub["lon"].tolist(), lat=sub["lat"].tolist(),
            mode="markers+text", name=status,
            marker=dict(size=sz, color=color, opacity=0.75),
            text=sub[name_col].astype(str).str[:14].tolist(),
            textfont=dict(size=9, color=color),
            customdata=hover_texts,
            hovertemplate="%{customdata}<extra></extra>",
        ))

    fig.update_layout(**_mapbox_base_layout(340, 28, 50, 4.0))
    return fig


def fig_losses_bubble_map(df_losses: pd.DataFrame) -> go.Figure:
    """
    Bubble map de perdas financeiras por país.
    Tamanho e cor dos círculos proporcionais ao valor em USD.
    """
    if df_losses.empty or "country" not in df_losses.columns:
        return go.Figure()

    df_grp = (
        df_losses.groupby("country")["estimated_daily_loss_usd"]
        .sum()
        .reset_index()
        .rename(columns={"estimated_daily_loss_usd": "total_loss"})
    )

    coords = []
    for _, row in df_grp.iterrows():
        match = next(
            (
                (lat, lon)
                for key, (lat, lon) in COUNTRY_COORDS.items()
                if key.lower() in row["country"].lower()
                or row["country"].lower() in key.lower()
            ),
            (None, None),
        )
        coords.append(match)

    df_grp["lat"] = [c[0] for c in coords]
    df_grp["lon"] = [c[1] for c in coords]
    df_valid = df_grp.dropna(subset=["lat", "lon"])

    max_loss = df_valid["total_loss"].max()
    norm = df_valid["total_loss"] / max_loss
    sizes = (10 + norm * 38).tolist()
    colors = [
        f"rgba(248,{int(81*(1-n))},{int(73*(1-n))},{0.4 + 0.55*n:.2f})"
        for n in norm
    ]

    fig = go.Figure(go.Scattermapbox(
        lon=df_valid["lon"].tolist(),
        lat=df_valid["lat"].tolist(),
        mode="markers",
        marker=dict(size=sizes, color=colors),
        text=[
            f"<b>{row['country']}</b><br>Perda diária: US$ {row['total_loss']:,.0f}"
            for _, row in df_valid.iterrows()
        ],
        hovertemplate="%{text}<extra></extra>",
        name="Perdas (USD/dia)",
    ))

    fig.update_layout(**_mapbox_base_layout(340, 28, 52, 3.0))
    return fig


# ── Timeline ──────────────────────────────────────────────────────────────────

def build_timeline_items(df_timeline: pd.DataFrame) -> list:
    """
    Constrói a lista de itens HTML para a timeline de eventos do conflito.
    Retorna lista de componentes Dash.
    """
    from dash import html  # import local para evitar dependência circular

    if df_timeline.empty:
        return [html.Div("Sem dados disponíveis.", style={"color": C["text2"]})]

    df = df_timeline.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"]).sort_values("date", ascending=False)

    sev_colors = {
        "Critical": C["danger"],
        "High":     "#FF6B35",
        "Medium":   C["warning"],
        "Low":      C["primary"],
    }

    items = []
    for _, row in df.iterrows():
        event  = str(row.get("event_type", ""))
        desc   = str(row.get("event_description", ""))
        impact = str(row.get("aviation_impact", ""))
        sev    = str(row.get("severity", "Low"))
        full_desc = desc + (" — " + impact if impact and impact != "nan" else "")
        color = sev_colors.get(sev, C["primary"])

        items.append(html.Div([
            html.Div([
                html.Span(
                    row["date"].strftime("%d %b %Y").upper(),
                    style={
                        "fontSize": "10px", "color": C["text2"],
                        "fontFamily": FONT_MONO, "letterSpacing": "0.06em",
                        "fontWeight": "500",
                    },
                ),
                html.Span(
                    sev,
                    style={
                        "fontSize": "9px", "fontWeight": "700",
                        "color": color, "fontFamily": FONT_BODY,
                        "background": f"rgba(0,0,0,0.25)",
                        "padding": "1px 7px", "borderRadius": "10px",
                        "border": f"1px solid {color}",
                        "letterSpacing": "0.04em",
                    },
                ),
            ], style={
                "display": "flex", "justifyContent": "space-between",
                "alignItems": "center", "marginBottom": "5px",
            }),
            html.Div(event, style={
                "fontSize": "12px", "fontWeight": "600", "color": C["text"],
                "fontFamily": FONT_BODY, "marginBottom": "4px",
            }),
            html.Div(
                full_desc[:140] + ("…" if len(full_desc) > 140 else ""),
                style={
                    "fontSize": "11px", "color": C["text2"],
                    "lineHeight": "1.55", "fontFamily": FONT_BODY,
                },
            ),
        ], style={
            "padding": "10px 12px 10px 14px",
            "borderLeft": f"2px solid {color}",
            "marginBottom": "8px",
            "background": C["card2"],
            "borderRadius": "0 6px 6px 0",
        }))

    return items
