import streamlit as st

from biblioteca.materiais_tubulacao import (
    obter_materiais,
    obter_diametros,
    obter_propriedades
)

st.title("Base Técnica")

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

st.subheader("Propriedades")

st.json(dados)