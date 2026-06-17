import streamlit as st

from biblioteca.hidraulica import (
    calcular_velocidade,
    calcular_reynolds,
    classificar_regime,
    calcular_fator_atrito,
    calcular_j_darcy
)

st.title("Teste Darcy-Weisbach")

vazao = st.number_input(
    "Vazão (L/s)",
    value=1.0
)

diametro = st.number_input(
    "Diâmetro interno (mm)",
    value=21.6
)

area = 0.000366

vel = calcular_velocidade(
    vazao,
    area
)

re = calcular_reynolds(
    vel,
    diametro
)

regime = classificar_regime(
    re
)

f = calcular_fator_atrito(
    re,
    0.0015,
    diametro
)

j = calcular_j_darcy(
    f,
    vel,
    diametro
)

st.write(f"Velocidade: {vel:.3f} m/s")
st.write(f"Reynolds: {re:,.0f}")
st.write(f"Regime: {regime}")
st.write(f"Fator de atrito: {f:.5f}")
st.write(f"j Darcy: {j:.5f} mca/m")