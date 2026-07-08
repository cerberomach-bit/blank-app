
import streamlit as st

# Configuração da página para celular
st.set_page_config(page_title="Dimensionamento Solar SE", page_icon="⚡", layout="centered")

st.title("⚡ Dimensionamento Técnico Solar")
st.write("Cálculo de potência fotovoltaica para os estados de MG, SP e RJ baseado na demanda do cliente.")

st.markdown("---")
st.subheader("📋 Dados de Entrada")

# 1. Entrada de Consumo em kWh
consumo = st.number_input("Necessidade mensal de consumo do cliente (kWh/mês):", min_value=30, max_value=100000, value=300, step=50)

# 2. Base de dados expandida de Irradiação (HSP) para MG, SP e RJ
banco_dados_hsp = {
    "Minas Gerais": {
        "Zona da Mata (Juiz de Fora e região)": 4.4,
        "Belo Horizonte e Região Metropolitana": 4.8,
        "Norte de Minas (Montes Claros, Januária)": 5.4,
        "Triângulo Mineiro / Alto Paranaíba": 5.1,
        "Sul de Minas (Pouso Alegre, Varginha)": 4.5,
        "Vale do Rio Doce / Mucuri": 4.6,
        "Noroeste de Minas (Paracatu, Unaí)": 5.3
    },
    "São Paulo": {
        "São Paulo (Capital e Região Metropolitana)": 4.2,
        "Campinas e Sorocaba": 4.6,
        "Ribeirão Preto / São José do Rio Preto (Norte/Oeste)": 5.1,
        "Vale do Paraíba (S. J. dos Campos, Taubaté)": 4.4,
        "Baixada Santista / Litoral Sul": 3.9,
        "Bauru / Marília / Presidente Prudente (Centro-Oeste)": 4.9
    },
    "Rio de Janeiro": {
        "Rio de Janeiro (Capital e Baixada Fluminense)": 4.5,
        "Região Serrana (Petrópolis, Nova Friburgo)": 4.1,
        "Norte / Noroeste Fluminense (Campos, Itaperuna)": 4.9,
        "Região dos Lagos (Cabo Frio, Macaé)": 4.8,
        "Médio Paraíba / Costa Verde (Volta Redonda, Angra)": 4.3
    }
}

# Caixas de seleção dinâmicas para o celular
estado = st.selectbox("🗺️ Selecione o Estado:", list(banco_dados_hsp.keys()))
regiao = st.selectbox("📍 Selecione a Região/Localidade:", list(banco_dados_hsp[estado].keys()))

hsp_padrao = banco_dados_hsp[estado][regiao]

# Slider para ajuste fino do HSP se você tiver o dado do CRESESB em mãos
hsp = st.slider("Horas de Sol Pleno (HSP) selecionado:", min_value=3.0, max_value=6.5, value=hsp_padrao, step=0.1)

# 3. Cálculos de Engenharia (Foco 100% Técnico)
# Perda padrão do sistema (Performance Ratio) = 80% (inversor, cabos, sujeira)
eficiencia = 0.80 

# Cálculo da Potência do Inversor / Sistema (kWp)
potencia_sistema_kwp = consumo / (30 * hsp * eficiencia)

# Sugestão de Painéis de Mercado (Padrão atual de 550W = 0.55kW)
potencia_painel_kw = 0.55
num_paineis = int(-(-potencia_sistema_kwp // potencia_painel_kw)) # Arredonda para cima

# Área física mínima estimada em metros quadrados (2,6 m² por painel de 550W)
area_estimada = num_paineis * 2.6

# 4. Exibição Técnica dos Resultados
st.markdown("---")
st.subheader("📊 Especificações dos Equipamentos")

st.metric(label="💡 Potência Recomendada do Sistema / Inversor", value=f"{potencia_sistema_kwp:.2f} kWp")

col1, col2 = st.columns(2)
with col1:
    st.metric(label="🧩 Painéis Necessários (550W)", value=f"{num_paineis} un")
with col2:
    st.metric(label="📐 Área Mínima de Telhado", value=f"{area_estimada:.1f} m²")

st.markdown("---")
st.caption(f"⚙️ Parâmetros utilizados: Eficiência global do sistema fixa em 80% e irradiação solar de {hsp} kWh/m²/dia para a região selecionada.")
