import streamlit as st

from biblioteca.consumo_maximo_provavel import (
    calcular_vazao_maximo_provavel
)

st.title(
    "Teste Consumo Máximo Provável"
)

peso = st.number_input(
    "Soma dos Pesos",
    min_value=0.0,
    value=1.0
)

vazao = calcular_vazao_maximo_provavel(
    peso
)

st.metric(
    "Vazão (L/s)",
    f"{vazao:.3f}"
)