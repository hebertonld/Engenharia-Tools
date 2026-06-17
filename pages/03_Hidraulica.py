import streamlit as st
import pandas as pd

from apps.perda_carga_agua_fria import (
    processar_tabela
)

from biblioteca.materiais_tubulacao import (
    obter_materiais
)

st.title(
    "Perda de Carga - Água Fria"
)

# =====================================================
# CONFIGURAÇÕES
# =====================================================

metodo = st.selectbox(

    "Método Hidráulico",

    [
        "Universal",
        "Hazen-Williams",
        "Fair-Whipple-Hsiao"
    ]
)

# =====================================================
# TABELA INICIAL
# =====================================================

if "rede" not in st.session_state:

    st.session_state.rede = pd.DataFrame({

        "Consumo":
        ["Máximo Possível"],

        "Nó Montante":
        ["A"],

        "Nó Jusante":
        ["B"],

        "Peso":
        [0.0],

        "Vazão Informada":
        [1.0],

        "Material":
        ["PVC SOLDAVEL"],

        "DN":
        [25],

        "Comprimento Real":
        [10.0],

        "Comprimento Equiv.":
        [0.0],

        "Diferença de Cota":
        [0.0],

        "Perda Adicional":
        [0.0],

        "Pressão Disponível":
        [25.0]
    })

# =====================================================
# EDIÇÃO
# =====================================================

df = st.data_editor(

    st.session_state.rede,

    num_rows="dynamic",

    use_container_width=True,

    column_config={

        "Consumo":
        st.column_config.SelectboxColumn(

            "Consumo",

            options=[

                "Máximo Possível",
                "Máximo Provável"
            ]
        ),

        "Material":
        st.column_config.SelectboxColumn(

            "Material",

            options=obter_materiais()
        ),

        "Peso":
        st.column_config.NumberColumn(

            "Peso",

            min_value=0.0
        ),

        "Vazão Informada":
        st.column_config.NumberColumn(

            "Vazão Informada",

            min_value=0.0
        ),

        "Comprimento Real":
        st.column_config.NumberColumn(

            "Comprimento Real",

            min_value=0.0
        ),

        "Comprimento Equiv.":
        st.column_config.NumberColumn(

            "Comprimento Equiv.",

            min_value=0.0
        ),

        "Diferença de Cota":
        st.column_config.NumberColumn(

            "Diferença de Cota"
        ),

        "Perda Adicional":
        st.column_config.NumberColumn(

            "Perda Adicional",

            min_value=0.0
        ),

        "Pressão Disponível":
        st.column_config.NumberColumn(

            "Pressão Disponível",

            min_value=0.0,

            help=(
                "Pressão disponível no nó de montante "
                "do primeiro trecho da rede."
            )
        )
    }
)

st.session_state.rede = df

# =====================================================
# PROCESSAMENTO
# =====================================================

resultado = processar_tabela(
    df,
    metodo
)

# =====================================================
# RESULTADOS
# =====================================================

st.subheader(
    "Resultados"
)

st.dataframe(

    resultado,

    use_container_width=True
)