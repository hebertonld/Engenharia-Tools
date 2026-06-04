import streamlit as st

from components.cards import render_module_card


st.title("🏠 Engenharia Tools")

st.markdown(
    """
    Plataforma de aplicações para engenharia.

    ---
    """
)

st.subheader("Módulos")

col1, col2 = st.columns(2)

with col1:

    render_module_card(
        "🌧️ Drenagem",
        "Galerias, bueiros, método racional, reservação."
    )

    render_module_card(
        "💧 Hidráulica",
        "Perda de carga, redes pressurizadas e bombeamento."
    )

with col2:

    render_module_card(
        "🚰 Saneamento",
        "Abastecimento de água e esgotamento sanitário."
    )

    render_module_card(
        "🏗️ BIM",
        "Ferramentas para Revit, Dynamo e automações."
    )

st.divider()

st.subheader("Roadmap")

roadmap = [
    "Método Racional",
    "Perda de Carga",
    "Dimensionamento de Galerias",
    "Método de Rippl",
    "Bueiros",
    "Ferramentas BIM"
]

for item in roadmap:

    st.checkbox(item, value=False, disabled=True)