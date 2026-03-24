# ✈ AviWatch — Global Civil Aviation Disruption Dashboard 2026

> Dashboard interativo que analisa o impacto do conflito Iran–EUA na aviação civil mundial,
> construído com Python, Dash e Plotly sobre dados reais do Kaggle.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)
![Dash](https://img.shields.io/badge/Dash-2.14%2B-008DE4?style=flat&logo=plotly&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3F4F75?style=flat&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?style=flat&logo=pandas&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

---

## 📸 Preview

> *Dashboard rodando em modo dark com sidebar de navegação,
> mapas interativos Mapbox e KPIs em tempo real.*

---

## 📊 O que o dashboard cobre

| Métrica | Valor |
|---|---|
| 💸 Perda financeira diária total | US$ 48,8 milhões |
| 🚫 Voos cancelados no período | 680 |
| 🔀 Voos desviados | 420 |
| 🏢 Aeroportos afetados | 113 (únicos) |
| ✈ Companhias impactadas | 35 |
| 🚁 Espaços aéreos fechados | 39 FIRs/UIRs |

---

## 🗂 Estrutura do projeto

```
aviation-war-dashboard/
│
├── app.py                  # Ponto de entrada — inicializa e conecta tudo
│
├── src/
│   ├── __init__.py
│   ├── config.py           # Constantes, paleta de cores, coordenadas
│   ├── data_loader.py      # Download Kaggle, leitura CSVs, KPIs
│   ├── figures.py          # Todas as figuras Plotly (gráficos + mapas)
│   └── layout.py           # Componentes Dash, sidebar, cards, layout
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/aviation-war-dashboard.git
cd aviation-war-dashboard
```

### 2. Crie e ative o ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o Kaggle

O projeto usa a biblioteca `kagglehub` para baixar os dados automaticamente.
Você precisará de uma conta no [Kaggle](https://www.kaggle.com) e de um token de API:

1. Acesse **Account → API → Create New Token**
2. Salve o arquivo `kaggle.json` em:
   - **Windows:** `C:\Users\<seu-usuario>\.kaggle\kaggle.json`
   - **Linux/macOS:** `~/.kaggle/kaggle.json`

### 5. Execute o dashboard

```bash
python app.py
```

Acesse **http://127.0.0.1:8050** no navegador.

---

## 🛠 Stack utilizada

| Tecnologia | Uso |
|---|---|
| **Python 3.10+** | Linguagem base |
| **Dash 2.14+** | Framework web para dashboards |
| **Plotly 5.18+** | Visualizações interativas |
| **Pandas 2.0+** | Manipulação e análise de dados |
| **kagglehub** | Download automático do dataset |
| **Carto Dark Matter** | Tile de mapa escuro (via Mapbox) |

---

## 📦 Dataset

**[Global Civil Aviation Disruption 2026 – Iran-US War](https://www.kaggle.com/datasets/zkskhurram/global-civil-aviation-disruption2026-iranus-war)**
por `zkskhurram` no Kaggle.

Arquivos utilizados:

| Arquivo | Descrição |
|---|---|
| `airline_losses_estimate.csv` | Perdas financeiras por companhia |
| `airport_disruptions.csv` | Aeroportos afetados e severidade |
| `airspace_closures.csv` | Fechamentos de FIRs/UIRs |
| `flight_cancellations.csv` | Voos cancelados (por voo) |
| `flight_reroutes.csv` | Voos desviados (por voo) |
| `conflict_events.csv` | Timeline de eventos do conflito |

---

## 🎨 Design

- **Tema:** Dark Premium inspirado no GitHub Dark
- **Fontes:** DM Sans · IBM Plex Sans · JetBrains Mono
- **Mapas:** Scattermapbox com tile `carto-darkmatter`
- **Paleta:** Vermelho `#F85149` · Azul `#2F81F7` · Fundo `#0D1117`

---

## 📁 Módulos

### `src/config.py`
Centraliza todas as constantes do projeto: dataset ID, nomes de arquivos CSV,
paleta de cores, fontes, coordenadas de aeroportos e países, mapeamentos ISO-3.

### `src/data_loader.py`
Responsável por baixar e carregar os dados, enriquecer DataFrames com coordenadas
geográficas e calcular os 6 KPIs exibidos no topo do dashboard.

### `src/figures.py`
Contém todas as funções de geração de figuras Plotly:
gráficos de tendência, mapas Mapbox interativos e timeline de eventos.
Cada função recebe um DataFrame e retorna um `go.Figure` pronto para uso.

### `src/layout.py`
Define os componentes visuais reutilizáveis (cards, KPI cards, sidebar, topbar)
e a função `build_layout()` que monta o HTML final do Dash.

### `app.py`
Ponto de entrada limpo: carrega dados → gera figuras → monta layout → inicia servidor.

---

## 📄 Licença

MIT © 2026 — Sinta-se livre para usar, modificar e distribuir.
