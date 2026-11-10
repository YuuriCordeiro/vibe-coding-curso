import streamlit as st
import pandas as pd
from datetime import date
from pathlib import Path

st.title("Meus gastos")

arquivo_gastos = Path(__file__).parent / "gastos.csv"
colunas = ["Categoria", "Valor (R$)", "Data"]

if not arquivo_gastos.exists():
    pd.DataFrame(columns=colunas).to_csv(arquivo_gastos, index=False)

gastos = pd.read_csv(arquivo_gastos).to_dict("records")

if st.button("Limpar tudo"):
    pd.DataFrame(columns=colunas).to_csv(arquivo_gastos, index=False)
    st.rerun()

with st.form("formulario_gasto"):
    categoria = st.text_input("Categoria", placeholder="Ex.: Alimentação")
    valor = st.number_input("Valor (R$)", min_value=0.01, value=0.01, step=1.0)
    data = st.date_input("Data", value=date.today())

    adicionar = st.form_submit_button("Adicionar gasto")

if adicionar:
    if categoria.strip():
        gastos.append({
            "Categoria": categoria.strip(),
            "Valor (R$)": valor,
            "Data": data,
        })
        pd.DataFrame(gastos, columns=colunas).to_csv(arquivo_gastos, index=False)
    else:
        st.error("Digite uma categoria antes de adicionar.")

if gastos:
    gastos = pd.DataFrame(gastos, columns=colunas)

    st.subheader("Gastos adicionados")
    st.dataframe(gastos, use_container_width=True, hide_index=True)

    total = gastos["Valor (R$)"].sum()
    st.metric("Total gasto", f"R$ {total:.2f}")

    st.subheader("Gastos por categoria")
    totais_por_categoria = gastos.groupby("Categoria", as_index=False)["Valor (R$)"].sum()
    st.bar_chart(
        totais_por_categoria,
        x="Categoria",
        y="Valor (R$)",
        color="Categoria",
    )
else:
    st.info("Seus gastos aparecerão aqui depois que você adicionar o primeiro.")
