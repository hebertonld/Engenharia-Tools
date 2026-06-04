import streamlit as st


def render_module_card(
    titulo: str,
    descricao: str
):
    """
    DESCRIÇÃO:
        Exibe card padronizado.

    ENTRADAS:
        titulo : str
        descricao : str

    SAÍDA:
        Card visual.

    TRATAMENTO DE ERROS:
        Não aplicável.
    """

    with st.container(border=True):

        st.subheader(titulo)

        st.caption(descricao)