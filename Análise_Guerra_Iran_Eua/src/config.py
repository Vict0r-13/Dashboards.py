# =============================================================================
#  config.py — Constantes, paleta de cores, coordenadas e tokens de design
# =============================================================================

# ── Kaggle Dataset ────────────────────────────────────────────────────────────
DATASET_ID = "zkskhurram/global-civil-aviation-disruption2026-iranus-war"

CSV_FILES = {
    "losses":    "airline_losses_estimate.csv",
    "airports":  "airport_disruptions.csv",
    "airspace":  "airspace_closures.csv",
    "cancel":    "flight_cancellations.csv",
    "reroutes":  "flight_reroutes.csv",
    "timeline":  "conflict_events.csv",
}

# ── Design System — Dark Premium ─────────────────────────────────────────────
COLORS = {
    "bg":        "#0D1117",
    "sidebar":   "#161B22",
    "card":      "#1C2128",
    "card2":     "#21262D",
    "border":    "#30363D",
    "primary":   "#2F81F7",
    "danger":    "#F85149",
    "warning":   "#D29922",
    "success":   "#3FB950",
    "purple":    "#BC8CFF",
    "orange":    "#FFA657",
    "text":      "#E6EDF3",
    "text2":     "#8B949E",
    "text3":     "#C9D1D9",
    "accent":    "#F85149",
    "highlight": "#388BFD",
}

FONT_DISPLAY = "'DM Sans', 'Segoe UI', sans-serif"
FONT_BODY    = "'IBM Plex Sans', 'Segoe UI', sans-serif"
FONT_MONO    = "'JetBrains Mono', 'Fira Code', monospace"

# ── Coordenadas de aeroportos (nome / código IATA → lat, lon) ─────────────────
AIRPORT_COORDS = {
    "Tehran":    (35.6892, 51.3890), "IKA":  (35.4161, 51.1522),
    "Mashhad":   (36.2350, 59.6400), "Isfahan": (32.7506, 51.8613),
    "Dubai":     (25.2532, 55.3657), "DXB":  (25.2532, 55.3657),
    "Doha":      (25.2731, 51.6081), "DOH":  (25.2731, 51.6081),
    "Riyadh":    (24.9578, 46.6988), "RUH":  (24.9578, 46.6988),
    "Kuwait":    (29.2267, 47.9689), "KWI":  (29.2267, 47.9689),
    "Bahrain":   (26.2702, 50.6337), "BAH":  (26.2702, 50.6337),
    "Abu Dhabi": (24.4330, 54.6511), "AUH":  (24.4330, 54.6511),
    "Muscat":    (23.5931, 58.2844), "MCT":  (23.5931, 58.2844),
    "Amman":     (31.7228, 35.9930), "AMM":  (31.7228, 35.9930),
    "Beirut":    (33.8225, 35.4884), "BEY":  (33.8225, 35.4884),
    "Baghdad":   (33.2625, 44.2346), "BGW":  (33.2625, 44.2346),
    "Kabul":     (34.5659, 69.2101), "KBL":  (34.5659, 69.2101),
    "Karachi":   (24.9065, 67.1557), "KHI":  (24.9065, 67.1557),
    "Mumbai":    (19.0887, 72.8679), "BOM":  (19.0887, 72.8679),
    "Delhi":     (28.5562, 77.1000), "DEL":  (28.5562, 77.1000),
    "Istanbul":  (41.2753, 28.7519), "IST":  (41.2753, 28.7519),
    "London":    (51.4775, -0.4614), "LHR":  (51.4775, -0.4614),
    "Frankfurt": (50.0333,  8.5706), "FRA":  (50.0333,  8.5706),
    "Paris":     (49.0097,  2.5479), "CDG":  (49.0097,  2.5479),
    "New York":  (40.6413, -73.7781),"JFK":  (40.6413,-73.7781),
    "Singapore": ( 1.3644, 103.9915),"SIN":  ( 1.3644,103.9915),
    "Bangkok":   (13.6811, 100.7470),"BKK":  (13.6811,100.7470),
}

# ── Coordenadas de países (centróide) ─────────────────────────────────────────
COUNTRY_COORDS = {
    "Iran":         (32.4279,  53.6880),
    "Iraq":         (33.2232,  43.6793),
    "UAE":          (23.4241,  53.8478),
    "Saudi Arabia": (23.8859,  45.0792),
    "Qatar":        (25.3548,  51.1839),
    "Kuwait":       (29.3117,  47.4818),
    "Bahrain":      (26.0275,  50.5500),
    "Oman":         (21.4735,  55.9754),
    "Pakistan":     (30.3753,  69.3451),
    "India":        (20.5937,  78.9629),
    "Turkey":       (38.9637,  35.2433),
    "Jordan":       (30.5852,  36.2384),
    "Lebanon":      (33.8547,  35.8623),
    "UK":           (55.3781,  -3.4360),
    "USA":          (37.0902, -95.7129),
    "Germany":      (51.1657,  10.4515),
    "France":       (46.2276,   2.2137),
    "Singapore":    ( 1.3521, 103.8198),
    "Thailand":     (15.8700, 100.9925),
    "Australia":    (-25.2744, 133.7751),
    "China":        (35.8617, 104.1954),
    "Japan":        (36.2048, 138.2529),
    "South Korea":  (35.9078, 127.7669),
}

# ── ISO-3 para choropleth ─────────────────────────────────────────────────────
ISO_MAP = {
    "UAE": "ARE", "India": "IND", "Qatar": "QAT", "Turkey": "TUR",
    "Germany": "DEU", "UK": "GBR", "Pakistan": "PAK", "Iran": "IRN",
    "Saudi Arabia": "SAU", "China": "CHN", "South Korea": "KOR",
    "Singapore": "SGP", "USA": "USA", "Australia": "AUS", "France": "FRA",
    "Thailand": "THA", "Japan": "JPN", "Kuwait": "KWT", "Bahrain": "BHR",
    "Oman": "OMN", "Jordan": "JOR", "Lebanon": "LBN", "Iraq": "IRQ",
}

# ── Severity colors para mapas ────────────────────────────────────────────────
SEVERITY_COLORS = {
    "Critical": COLORS["danger"],
    "High":     "#FF6B35",
    "Medium":   COLORS["warning"],
    "Low":      "#58A6FF",
    "Minimal":  COLORS["success"],
}

AIRSPACE_STATUS_COLORS = {
    "Fechado":     (COLORS["danger"],  28),
    "NOTAM Ativo": (COLORS["warning"], 22),
    "Restrito":    ("#FF6B35",         20),
}
