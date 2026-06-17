import streamlit as st

from biblioteca.aparelhos_nbr5626 import (
    obter_aparelhos,
    obter_peso,
    obter_pressao_minima
)

st.title(
    "Teste Aparelhos NBR 5626"
)

aparelho = st.selectbox(
    "Aparelho",
    obter_aparelhos()
)

st.metric(
    "Peso",
    obter_peso(aparelho)
)

st.metric(
    "Pressão mínima (kPa)",
    obter_pressao_minima(aparelho)
)