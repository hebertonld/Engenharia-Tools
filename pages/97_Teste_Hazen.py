import streamlit as st

from biblioteca.materiais_tubulacao import (
    obter_materiais,
    obter_diametros,
    obter_propriedades
)

from biblioteca.hidraulica import (
    calcular_j_hazen_williams,
    calcular_perda_linear
)

st.title(
    "Teste Hazen-Williams"
)

material = st.selectbox(
    "Material",
    obter_materiais()
)

dn = st.selectbox(
    "DN",
    obter_diametros(material)
)

dados = obter_propriedades(
    material,
    dn
)

vazao = st.number_input(
    "Vazão [L/s]",
    min_value=0.01,
    value=1.0
)

comprimento = st.number_input(
    "Comprimento [m]",
    min_value=0.0,
    value=10.0
)

j = calcular_j_hazen_williams(
    vazao,
    dados["diametro_interno_mm"],
    dados["coef_hazen"]
)

hf = calcular_perda_linear(
    j,
    comprimento
)

st.subheader("Resultados")

st.metric(
    "Diâmetro Interno [mm]",
    round(
        dados["diametro_interno_mm"],
        2
    )
)

st.metric(
    "J [mca/m]",
    round(j, 6)
)

st.metric(
    "hf [mca]",
    round(hf, 4)
)