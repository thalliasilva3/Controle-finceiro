import streamlit as st
import pandas as pd

#Configuração da página
st.set_page_config(
    page_title="Controle Financeiro",
    page_icon="💰",
    layout="wide"
)
#Título
st.title("💰 Controle Financeiro")
st.write("Bem-vindo ao seu sistema de controle financeiro!")

st.divider()

#Valores iniciais
receitas = 0.00
despesas = 0.00
saldo = receitas - despesas
metas = 0.00

#Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Receitas", f"R$ {receitas:,.2f}")

with col2:
    st.metric("💸 Despesas", f"R$ {despesas:,.2f}")

with col3:
    st.metric("🟢 Saldo", f"R$ {saldo:,.2f}")

with col4:
    st.metric("🎯 Metas", f"R$ {metas:,.2f}")
st.divider()

#Área de lançamentos
st.subheader("📊 Movimentações financeiras")

dados = pd.DataFrame ({
    "Tipo": ["Receita", "Despesa"],
    "Valor": [0.00, 0.00]
})

st.bar_chart(dados.set_index("Tipo"))

st.info("💡 Sistema em desenvolvimento. Em breve você poderá cadastrar suas receitas, despesas e metas.")