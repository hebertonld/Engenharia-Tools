import streamlit as st

from core.config import AppConfig
from core.version import APP_VERSION


def render_header():
    """
    DESCRIÇÃO:
        Renderiza cabeçalho principal.

    ENTRADAS:
        Nenhuma.

    SAÍDA:
        Cabeçalho da página.

    TRATAMENTO DE ERROS:
        Não aplicável.
    """

    st.title(f"{AppConfig.PAGE_ICON} {AppConfig.APP_NAME}")

    st.caption(
        f"Versão {APP_VERSION}"
    )