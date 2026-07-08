"""
Aplicativo de Dimensionamento Solar Fotovoltaico
Desenvolvido com Streamlit - Focado em uso Mobile (Responsivo)

Como executar:
    streamlit run dimensionamento_solar.py
"""

import streamlit as st

# =========================================================
# CONFIGURAÇÃO DA PÁGINA (mobile-first)
# =========================================================
st.set_page_config(
    page_title="Dimensionamento Solar FV",
    page_icon="☀️",
    layout="centered",  # 'centered' funciona melhor em telas de celular
    initial_sidebar_state="collapsed",
)

# =========================================================
# CSS CUSTOMIZADO - Melhora a experiência em dispositivos móveis
# =========================================================
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        div[data-testid="stMetric"] {
            background-color: #fff8e1;
            border: 1px solid #ffe082;
            border-radius: 12px;
            padding: 12px 8px;
            text-align: center;
        }
        div[data-testid="stMetricLabel"] {
            justify-content: center;
        }
        div[data-testid="stMetricValue"] {
            justify-content: center;
            color: #e65100;
        }
        .stButton > button {
            width: 100%;
            background-color: #f9a825;
            color: white;
            font-weight: 700;
            border-radius: 10px;
            padding: 0.6rem 0;
            border: none;
        }
        .stButton > button:hover {
            background-color: #f57f17;
            color: white;
        }
        h1 {
            font-size: 1.6rem !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# BASE DE DADOS DE HSP (Horas de Sol Pleno)
# Valores aproximados médios anuais, baseados no
# Atlas Brasileiro de Energia Solar (referência de mercado)
# Estrutura: { "Estado": { "Região/Cidade": HSP } }
# =========================================================
HSP_DATA = {
    "Acre": {
        "Rio Branco": 4.7,
        "Cruzeiro do Sul": 4.6,
    },
    "Alagoas": {
        "Maceió": 5.4,
        "Sertão Alagoano": 5.7,
    },
    "Amapá": {
        "Macapá": 4.8,
        "Oiapoque": 4.7,
    },
    "Amazonas": {
        "Manaus": 4.5,
        "Interior do Amazonas": 4.4,
    },
    "Bahia": {
        "Salvador": 5.3,
        "Chapada Diamantina": 5.8,
        "Vale do São Francisco": 6.0,
        "Sul da Bahia": 5.2,
    },
    "Ceará": {
        "Fortaleza": 5.6,
        "Sertão Central": 5.9,
        "Cariri": 5.7,
    },
    "Distrito Federal": {
        "Brasília": 5.6,
    },
    "Espírito Santo": {
        "Vitória": 5.1,
        "Norte do ES": 5.3,
        "Sul do ES": 4.9,
    },
    "Goiás": {
        "Goiânia": 5.5,
        "Sudoeste Goiano": 5.6,
        "Norte Goiano": 5.4,
    },
    "Maranhão": {
        "São Luís": 5.2,
        "Sul do Maranhão": 5.5,
    },
    "Mato Grosso": {
        "Cuiabá": 5.3,
        "Norte de Mato Grosso": 5.1,
        "Sudeste de Mato Grosso": 5.5,
    },
    "Mato Grosso do Sul": {
        "Campo Grande": 5.4,
        "Dourados": 5.5,
    },
    "Minas Gerais": {
        "Belo Horizonte": 5.4,
        "Norte de Minas": 5.9,
        "Triângulo Mineiro": 5.6,
        "Zona da Mata": 5.0,
        "Sul de Minas": 5.2,
    },
    "Pará": {
        "Belém": 4.6,
        "Sudeste do Pará": 4.9,
    },
    "Paraíba": {
        "João Pessoa": 5.5,
        "Sertão Paraibano": 5.9,
    },
    "Paraná": {
        "Curitiba": 4.4,
        "Norte do Paraná": 4.9,
        "Oeste do Paraná": 4.8,
    },
    "Pernambuco": {
        "Recife": 5.4,
        "Sertão Pernambucano": 6.0,
        "Agreste": 5.7,
    },
    "Piauí": {
        "Teresina": 5.6,
        "Sul do Piauí": 5.9,
    },
    "Rio de Janeiro": {
        "Rio de Janeiro (Capital)": 4.9,
        "Norte Fluminense": 5.1,
        "Sul Fluminense": 4.8,
    },
    "Rio Grande do Norte": {
        "Natal": 5.7,
        "Seridó": 6.1,
    },
    "Rio Grande do Sul": {
        "Porto Alegre": 4.6,
        "Fronteira Oeste": 4.9,
        "Norte do RS": 4.5,
    },
    "Rondônia": {
        "Porto Velho": 4.7,
        "Ji-Paraná": 4.8,
    },
    "Roraima": {
        "Boa Vista": 5.0,
    },
    "Santa Catarina": {
        "Florianópolis": 4.4,
        "Oeste Catarinense": 4.7,
        "Norte Catarinense": 4.5,
    },
    "São Paulo": {
        "São Paulo (Capital)": 4.6,
        "Campinas": 4.9,
        "Ribeirão Preto": 5.3,
        "Vale do Paraíba": 4.7,
        "São José do Rio Preto": 5.4,
    },
    "Sergipe": {
        "Aracaju": 5.4,
        "Sertão Sergipano": 5.7,
    },
    "Tocantins": {
        "Palmas": 5.4,
        "Bico do Papagaio": 5.2,
    },
}

# =========================================================
# CONSTANTES DE ENGENHARIA
# =========================================================
PERFORMANCE_RATIO = 0.80      # Perda padrão do sistema (Taxa de Desempenho)
POTENCIA_PAINEL_W = 550       # Potência do módulo padrão de mercado (W)
AREA_PAINEL_M2 = 2.6          # Área ocupada por painel (m²)
DIAS_MES = 30                 # Dias considerados no mês

# =========================================================
# CABEÇALHO
# =========================================================
st.title("☀️ Dimensionamento Solar FV")
st.caption("Calcule o sistema fotovoltaico ideal para sua residência ou comércio")

st.divider()

# =========================================================
# ETAPA 1 — ENTRADAS DO USUÁRIO
# =========================================================
st.subheader("1️⃣ Dados de Consumo e Localização")

consumo_mensal = st.number_input(
    "Consumo Médio Mensal (kWh)",
    min_value=0.0,
    value=350.0,
    step=10.0,
    help="Verifique o valor de 'kWh consumidos' na sua conta de energia elétrica",
)

col_estado, col_regiao = st.columns(2)

with col_estado:
    estado_selecionado = st.selectbox(
        "Estado",
        options=sorted(HSP_DATA.keys()),
        index=sorted(HSP_DATA.keys()).index("Minas Gerais")
        if "Minas Gerais" in HSP_DATA
        else 0,
    )

# A segunda selectbox é dinâmica: depende do estado escolhido acima
with col_regiao:
    regioes_disponiveis = list(HSP_DATA[estado_selecionado].keys())
    regiao_selecionada = st.selectbox(
        "Cidade / Região",
        options=regioes_disponiveis,
    )

# HSP automático puxado da base de dados
hsp_automatico = HSP_DATA[estado_selecionado][regiao_selecionada]

st.divider()

# =========================================================
# ETAPA 2 — AJUSTE FINO DO HSP
# =========================================================
st.subheader("2️⃣ Irradiação Solar (HSP)")

st.write(
    f"HSP médio de referência para **{regiao_selecionada} ({estado_selecionado})**: "
    f"**{hsp_automatico} horas/dia**"
)

hsp_ajustado = st.slider(
    "Ajuste fino do HSP (opcional)",
    min_value=3.5,
    max_value=6.5,
    value=float(hsp_automatico),
    step=0.05,
    help=(
        "O valor inicial é preenchido automaticamente com base na região escolhida. "
        "Ajuste manualmente caso possua um dado mais preciso (ex: irradiância medida "
        "no telhado, orientação, sombreamento, etc.)."
    ),
)

st.divider()

# =========================================================
# ETAPA 3 — CÁLCULO
# =========================================================
st.subheader("3️⃣ Dimensionamento do Sistema")

calcular = st.button("🔆 Calcular Dimensionamento", type="primary")

if calcular:
    if consumo_mensal <= 0:
        st.error("Por favor, informe um consumo mensal maior que zero.")
    else:
        # --- Cálculos de engenharia solar ---

        # Potência do sistema necessária (kWp)
        potencia_kwp = consumo_mensal / (DIAS_MES * hsp_ajustado * PERFORMANCE_RATIO)

        # Quantidade de painéis (arredondado para cima, pois não existe painel fracionado)
        potencia_kwp_w = potencia_kwp * 1000
        qtd_paineis = -(-potencia_kwp_w // POTENCIA_PAINEL_W)  # ceil sem usar math
        qtd_paineis = int(qtd_paineis)

        # Potência real instalada, já considerando o arredondamento de painéis
        potencia_real_kwp = (qtd_paineis * POTENCIA_PAINEL_W) / 1000

        # Área mínima necessária
        area_necessaria = qtd_paineis * AREA_PAINEL_M2

        # Geração média mensal estimada com o sistema dimensionado
        geracao_estimada = potencia_real_kwp * DIAS_MES * hsp_ajustado * PERFORMANCE_RATIO

        st.success("✅ Dimensionamento calculado com sucesso!")

        # --- Exibição em métricas (2 colunas x 2 linhas, ideal para celular) ---
        col1, col2 = st.columns(2)
        with col1:
            st.metric("⚡ Potência do Sistema", f"{potencia_kwp:.2f} kWp")
        with col2:
            st.metric("🔲 Nº de Painéis (550W)", f"{qtd_paineis} un.")

        col3, col4 = st.columns(2)
        with col3:
            st.metric("📐 Área Necessária", f"{area_necessaria:.1f} m²")
        with col4:
            st.metric("☀️ HSP Utilizado", f"{hsp_ajustado:.2f} h/dia")

        st.divider()

        with st.expander("📋 Detalhes técnicos do dimensionamento"):
            st.markdown(
                f"""
- **Consumo mensal informado:** {consumo_mensal:.0f} kWh
- **Localização:** {regiao_selecionada} — {estado_selecionado}
- **Performance Ratio (perdas do sistema):** {PERFORMANCE_RATIO*100:.0f}%
- **Potência real instalada (após arredondamento de painéis):** {potencia_real_kwp:.2f} kWp
- **Geração média mensal estimada:** {geracao_estimada:.0f} kWh/mês
- **Módulo considerado:** {POTENCIA_PAINEL_W} W por painel
- **Área por painel:** {AREA_PAINEL_M2} m²
                """
            )

        st.caption(
            "⚠️ Este é um dimensionamento estimado para fins de pré-projeto. "
            "Um projeto executivo deve considerar orientação, inclinação, "
            "sombreamento, estrutura do telhado e normas técnicas da concessionária local."
        )
else:
    st.info("Preencha os dados acima e toque em **Calcular Dimensionamento**.")

st.divider()
st.caption("Desenvolvido para dimensionamento preliminar de sistemas fotovoltaicos residenciais e comerciais.")
