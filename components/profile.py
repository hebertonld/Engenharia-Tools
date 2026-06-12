import streamlit as st


def render_profile_image(
    image_path: str,
    size: int = 260
):
    """
    Exibe foto de perfil.

    Entradas:
        image_path : caminho da imagem
        size : largura em pixels

    Saídas:
        Componente visual

    Unidade:
        size -> px

    Tratamento de erros:
        Exibe mensagem caso o arquivo não exista.
    """

    try:

        st.image(
            image_path,
            width=size
        )

    except Exception as erro:

        st.error(
            f"Erro ao carregar imagem: {erro}"
        )