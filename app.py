import streamlit as st

from core.config import AppConfig
from components.header import render_header
from components.footer import render_footer


st.set_page_config(
    page_title=AppConfig.APP_NAME,
    page_icon=AppConfig.PAGE_ICON,
    layout=AppConfig.LAYOUT
)

with st.sidebar:

    st.title("🛠️ Engenharia Tools")

    st.caption("Portal de Engenharia")

    st.divider()

    st.success("Sistema operacional")

render_header()

st.info(
    "Selecione um módulo no menu lateral."
)

render_footer()