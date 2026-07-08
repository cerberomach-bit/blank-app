import streamlit as st

st.set_page_config(page_title="Solar Técnico", layout="centered")

st.title("⚡ Dimensionamento Técnico Solar")
st.write("Determine a potência exata dos equipamentos fotovoltaicos necessários.")

# 1. Base de dados de irradiação corrigida (HSP)
banco_hsp = {
    "MG - Zona da Mata (Juiz de Fora)": 4.4,
    "MG - Belo Horizonte e Metropolitana": 4.8,
    "MG - Norte de Minas (Montes Claros)": 5.4,
    "MG - Triângulo Mineiro": 5.1,
    "MG - Sul de Minas (Pouso Alegre)": 4.5,
    "SP - São Paulo Capital e Região": 4.2,
    "SP - Campinas e Sorocaba": 4.6,
    "SP - Ribeirão Preto e Norte": 5.1,
    "SP - Vale do Paraíba": 4.4,
    "RJ - Rio Capital e Baixada": 4.5,
    "RJ - Região Serrana (Petrópolis)": 4.1,
    "RJ - Região dos Lagos (Cabo Frio)": 4.8,
    "RJ - Médio Paraíba / Costa Verde": 4.3
}

# 2. Formulário direto de entrada
st.subheader("📋 Entrada de Dados")
consumo = st.number_input("Necessidade mensal do cliente (kWh/mês):", min_value=30, value=300, step=50)
localidade = st.selectbox("📍 Selecione a Região:", list(banco_hsp.keys()))

# 3. Processamento matemático exato e direto
hsp = banco_hsp[localidade]
eficiencia = 0.80  # 20% de perdas globais padrão

# Fórmula correta de Engenharia: kWp = kWh / (30 dias * HSP * Eficiência)
potencia_sistema_kwp = consumo / (30 * hsp * eficiencia)

# Cálculo exato de painéis (Módulos de 550W = 0.55kW) com arredondamento correto
num_paineis = int((potencia_sistema_kwp / 0.55) + 0.99)
area_estimada = num_paineis * 2.6

# 4. Exibição limpa (Sem blocos complexos que travam a tela)
st.markdown("---")
st.subheader("📊 Especificações Recomendadas")

st.write(f"🍏 **Potência do Sistema / Inversor:** {potencia_sistema_kwp:.2f} kWp")
st.write(f"🧩 **Quantidade de Painéis (550W):** {num_paineis} unidades")
st.write(f"📐 **Área Mínima de Telhado:** {area_estimada:.1f} m²")

st.markdown("---")
st.caption(f"Configuração calculada com {hsp} HSP para {localidade}.")
