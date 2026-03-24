# =============================================================================
#  data_loader.py — Carregamento, limpeza e KPIs
# =============================================================================

import os
import pandas as pd
import kagglehub

from src.config import DATASET_ID, CSV_FILES, AIRPORT_COORDS, COUNTRY_COORDS


def download_dataset() -> str:
    """Baixa o dataset do Kaggle e retorna o caminho local."""
    print("⏳ Baixando dataset do Kaggle...")
    path = kagglehub.dataset_download(DATASET_ID)
    print(f"✅ Dataset em: {path}")
    return path


def load_csv(path: str, filename: str) -> pd.DataFrame:
    """Carrega um CSV do diretório do dataset. Retorna DataFrame vazio se não encontrado."""
    filepath = os.path.join(path, filename)
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        print(f"  ✔ {filename} → {df.shape[0]} linhas")
        return df
    print(f"  ✘ {filename} não encontrado")
    return pd.DataFrame()


def load_all(path: str) -> dict[str, pd.DataFrame]:
    """Carrega todos os CSVs do dataset e retorna um dicionário de DataFrames."""
    return {key: load_csv(path, fname) for key, fname in CSV_FILES.items()}


def enrich_coords(df: pd.DataFrame, col: str, coord_dict: dict) -> pd.DataFrame:
    """
    Adiciona colunas 'lat' e 'lon' ao DataFrame buscando correspondências
    pelo conteúdo da coluna `col` no dicionário `coord_dict`.
    """
    lats, lons = [], []
    for val in df[col]:
        found = False
        for key, (lat, lon) in coord_dict.items():
            if isinstance(val, str) and key.lower() in val.lower():
                lats.append(lat)
                lons.append(lon)
                found = True
                break
        if not found:
            lats.append(None)
            lons.append(None)
    df = df.copy()
    df["lat"] = pd.to_numeric(lats, errors="coerce")
    df["lon"] = pd.to_numeric(lons, errors="coerce")
    return df


def resolve_coords(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tenta enriquecer coordenadas em cascata:
    iata_code → airport_name → country
    """
    if "iata_code" in df.columns:
        df = enrich_coords(df, "iata_code", AIRPORT_COORDS)
    mask = df["lat"].isna() if "lat" in df.columns else pd.Series([True] * len(df))
    if mask.any() and "airport_name" in df.columns:
        df2 = enrich_coords(df[mask], "airport_name", AIRPORT_COORDS)
        df.loc[mask, "lat"] = pd.to_numeric(df2["lat"].values, errors="coerce")
        df.loc[mask, "lon"] = pd.to_numeric(df2["lon"].values, errors="coerce")
    mask = df["lat"].isna()
    if mask.any() and "country" in df.columns:
        df2 = enrich_coords(df[mask], "country", COUNTRY_COORDS)
        df.loc[mask, "lat"] = pd.to_numeric(df2["lat"].values, errors="coerce")
        df.loc[mask, "lon"] = pd.to_numeric(df2["lon"].values, errors="coerce")
    return df


# ── Funções auxiliares para KPIs ──────────────────────────────────────────────

def safe_sum(df: pd.DataFrame, col: str) -> float:
    if df.empty or col not in df.columns:
        return 0.0
    return pd.to_numeric(df[col], errors="coerce").sum()


def safe_nunique(df: pd.DataFrame, col: str) -> int:
    if df.empty or col not in df.columns:
        return 0
    return df[col].nunique()


def compute_kpis(data: dict[str, pd.DataFrame]) -> dict:
    """Calcula os 6 KPIs principais do dashboard."""
    kpis = {
        "total_loss_usd":          safe_sum(data["losses"],   "estimated_daily_loss_usd"),
        "total_cancelled":         len(data["cancel"])   if not data["cancel"].empty   else 0,
        "total_rerouted":          len(data["reroutes"])  if not data["reroutes"].empty else 0,
        "total_airports_affected": safe_nunique(data["airports"], "airport_name"),
        "total_airlines_affected": safe_nunique(data["losses"],   "airline"),
        "total_airspace_closed":   len(data["airspace"]) if not data["airspace"].empty else 0,
    }
    print(
        f"\n📊 KPIs carregados:\n"
        f"   Perda diária   : US$ {kpis['total_loss_usd']/1e6:.1f}M\n"
        f"   Cancelamentos  : {kpis['total_cancelled']:,}\n"
        f"   Desvios        : {kpis['total_rerouted']:,}\n"
        f"   Aeroportos     : {kpis['total_airports_affected']}\n"
        f"   Companhias     : {kpis['total_airlines_affected']}\n"
        f"   Espaços aéreos : {kpis['total_airspace_closed']}\n"
    )
    return kpis
