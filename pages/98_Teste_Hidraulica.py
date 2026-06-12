import streamlit as st

from biblioteca.hidraulica import (
    calcular_velocidade
)

st.title("Teste Hidráulica")

vazao = st.number_input(
    "Vazão [L/s]",
    value=1.0
)

area = st.number_input(
    "Área [m²]",
    value=0.001
)

velocidade = calcular_velocidade(
    vazao,
    area
)

st.metric(
    "Velocidade [m/s]",
    round(velocidade, 3)
)