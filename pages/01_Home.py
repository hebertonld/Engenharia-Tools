import streamlit as st
from components.profile import render_profile_image

st.set_page_config(layout="wide")

# =====================================================
# HERO
# =====================================================

col_logo, col_texto = st.columns([1, 2])

with col_logo:
    st.image(
        "assets/logo/logo-transparente.png",
        width=250
    )

with col_texto:

    st.title("Heberton Damaceno")

    st.subheader("Engenheiro Civil")

    st.markdown(
        """
        **Especialidades**

        - Drenagem Urbana e Pluvial
        - Saneamento
        - Hidráulica
        - Infraestrutura
        - BIM e Automação
        """
    )

st.divider()

st.subheader("Portal de Ferramentas para Engenharia")

st.markdown(
    """
    Plataforma desenvolvida para concentrar aplicações
    de engenharia voltadas para drenagem, hidráulica,
    saneamento, infraestrutura urbana e automação.

    As ferramentas são desenvolvidas com foco em
    produtividade, rastreabilidade de cálculos e
    aplicação prática em projetos reais.
    """
)

col1, col2 = st.columns(2)

with col1:

    st.page_link(
        "pages/10_Ferramentas.py",
        label="Acessar Ferramentas",
        icon="🛠️"
    )

with col2:

    st.page_link(
        "pages/03_Portfolio.py",
        label="Portfólio",
        icon="📁"
    )

st.divider()

st.divider()

# =====================================================
# ÁREAS DE ATUAÇÃO
# =====================================================

st.subheader("Áreas de Atuação")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.info("🌧️ Drenagem")

with c2:
    st.info("💧 Hidráulica")

with c3:
    st.info("🚰 Saneamento")

with c4:
    st.info("🏗️ BIM")

st.divider()

# =====================================================
# FERRAMENTAS
# =====================================================

st.subheader("Ferramentas em Desenvolvimento")

st.markdown(
    """
    - Método Racional
    - Método de Rippl
    - Galerias Pluviais
    - Bueiros
    - Perda de Carga
    - Redes Pressurizadas
    """
)

st.caption("Versão 0.2.0")