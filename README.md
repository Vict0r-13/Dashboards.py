# ⛽ Análise de Preços da Gasolina no Brasil (2004–2021)

> Dashboard interativo construído com Python, Dash e Plotly. Explora 18 anos de série histórica de preços de revenda da gasolina em todos os 27 estados brasileiros.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)
![Dash](https://img.shields.io/badge/Dash-2.14+-0066FF?style=flat-square&logo=plotly&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.17+-3F4F75?style=flat-square&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-ETL-150458?style=flat-square&logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/Status-Funcional-22C55E?style=flat-square)

---

## 🎯 O que este projeto entrega

| Seção             | O que você encontra |
|-------------------|---------------------|
| **📈 Visão Geral** | Evolução anual com anotações em eventos críticos (Greve dos Caminhoneiros 2018, Pandemia 2020), ranking de estados e comparativo regional |
| **🗺️ Comparar Estados** | Linha histórica multi-estado com slider de período + desvio em relação à média nacional |
| **🌎 Análise Regional** | Evolução por estado dentro de cada região, box plot de dispersão e variação % ano a ano |

---

## 📊 Insights do dataset

- **+131,5%** de alta acumulada entre 2004 e 2021
- **ACRE** é historicamente o estado mais caro (média R$ 3,57/L)
- **SÃO PAULO** é o estado mais barato (média R$ 2,99/L)
- **NORTE** é a região com maior preço médio histórico
- A **Greve dos Caminhoneiros (2018)** gerou o maior choque pontual de preço da série
- A **Pandemia (2020)** reduziu temporariamente os preços, seguida de alta histórica em 2021

---

## 🗂️ Estrutura do projeto

```
dash-gasolina/
├── app.py               ← Dashboard completo (single-file, modular)
├── data/
│   └── data_clean.csv   ← Dataset limpo (23.570 registros, 6 colunas)
├── assets/              ← CSS customizado (opcional)
├── requirements.txt
├── Procfile             ← Deploy no Render/Heroku
├── .gitignore
└── README.md
```

---

## 🚀 Como executar localmente

```bash
# 1. Clone o repositório
git clone https://github.com/Vict0r-13/dash-gasolina.git
cd dash-gasolina

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute
python app.py
```

Acesse em: **http://localhost:8050**

---

## 🛠️ Stack técnica

| Biblioteca  | Uso                                          |
|-------------|----------------------------------------------|
| `Dash`      | Framework web para dashboards interativos    |
| `Plotly`    | Gráficos interativos (linha, barra, box plot)|
| `Pandas`    | ETL, limpeza e agregação dos dados           |
| `dbc`       | Layout responsivo com Bootstrap              |
| `Gunicorn`  | Servidor WSGI para deploy em produção        |

---

## 📬 Contato

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ivanildo-victor-py/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Vict0r-13)
[![Email](https://img.shields.io/badge/Email-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:ivanildov92@gmail.com)

---

*Fonte: ANP — Agência Nacional do Petróleo, Gás Natural e Biocombustíveis*
