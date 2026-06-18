import streamlit as st
import pandas as pd

from core.theme import Theme

from apps.perda_carga_agua_fria import (
    processar_tabela
)

from biblioteca.materiais_tubulacao import (
    obter_materiais
)


COLUNAS_ENTRADA = [
    "Consumo",
    "Nó Montante",
    "Nó Jusante",
    "Peso",
    "Vazão Informada",
    "Material",
    "DN",
    "Comprimento Real",
    "Comprimento Equiv.",
    "Diferença de Cota",
    "Perda Adicional"
]


COLUNAS_PLANILHA = [
    "Trecho",
    "Vazão (L/s)",
    "Pesos",
    "Q (L/s)",
    "DN",
    "Material",
    "Vel.",
    "Vel. max",
    "J",
    "Real",
    "Equiv.",
    "Total",
    "Dif. Cota",
    "P mon",
    "Linear",
    "Singular",
    "Total Perda",
    "P jus"
]


def aplicar_design_system():
    st.markdown(
        f"""
        <style>
            :root {{
                --et-primary: {Theme.PRIMARY};
                --et-primary-light: {Theme.PRIMARY_LIGHT};
                --et-surface: {Theme.SURFACE};
                --et-bg: {Theme.BACKGROUND};
                --et-border: {Theme.BORDER};
                --et-text: {Theme.TEXT};
                --et-muted: {Theme.TEXT_LIGHT};
                --et-warning: {Theme.WARNING};
                --et-success: {Theme.SUCCESS};
                --et-error: {Theme.ERROR};
            }}

            .main .block-container {{
                padding-top: 1.5rem;
                padding-bottom: 2rem;
                max-width: 1480px;
            }}

            h1, h2, h3 {{
                color: var(--et-text);
                letter-spacing: 0;
            }}

            h1 {{
                font-size: 2rem;
                font-weight: 750;
                margin-bottom: 0.25rem;
            }}

            div[data-testid="stForm"] {{
                border: 1px solid var(--et-border);
                border-radius: 8px;
                background: var(--et-surface);
                padding: 0.75rem 0.75rem 1rem;
            }}

            div[data-testid="stDataFrame"],
            div[data-testid="stDataEditor"] {{
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                overflow: hidden;
            }}

            div[data-testid="stDataFrame"] [role="columnheader"],
            div[data-testid="stDataEditor"] [role="columnheader"] {{
                background: #e5e7eb;
                color: #111827;
                font-weight: 700;
                border-right: 1px solid #94a3b8;
            }}

            div[data-testid="stDataFrame"] [role="gridcell"],
            div[data-testid="stDataEditor"] [role="gridcell"] {{
                border-right: 1px solid #d1d5db;
                border-bottom: 1px solid #d1d5db;
            }}

            .et-toolbar {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 0.75rem;
                margin: 0.25rem 0 0.75rem;
                padding: 0.75rem 0.9rem;
                border: 1px solid var(--et-border);
                border-radius: 8px;
                background: #f8fafc;
            }}

            .et-toolbar-title {{
                font-size: 0.92rem;
                font-weight: 700;
                color: var(--et-text);
            }}

            .et-toolbar-subtitle {{
                font-size: 0.78rem;
                color: var(--et-muted);
                margin-top: 0.15rem;
            }}

            .et-section-title {{
                font-size: 0.98rem;
                font-weight: 750;
                margin: 1rem 0 0.45rem;
                color: #111827;
            }}

            .et-sheet-hint {{
                font-size: 0.78rem;
                color: var(--et-muted);
                margin: -0.2rem 0 0.5rem;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )


def criar_linha(
    no_montante="A",
    no_jusante="B"
):
    return {
        "Consumo": "Máximo Possível",
        "Nó Montante": no_montante,
        "Nó Jusante": no_jusante,
        "Peso": 0.0,
        "Vazão Informada": 1.0,
        "Material": "PVC SOLDAVEL",
        "DN": 25,
        "Comprimento Real": 10.0,
        "Comprimento Equiv.": 0.0,
        "Diferença de Cota": 0.0,
        "Perda Adicional": 0.0
    }


def proximo_no(no):
    if (
        isinstance(no, str)
        and
        len(no) == 1
        and
        no.isalpha()
    ):
        return chr(
            ord(no.upper()) + 1
        )

    return ""


def criar_rede_padrao():
    return pd.DataFrame(
        [
            criar_linha()
        ],
        columns=COLUNAS_ENTRADA
    )


def criar_rede_exemplo():
    return pd.DataFrame(
        [
            criar_linha("A", "B"),
            criar_linha("B", "C"),
            criar_linha("C", "D"),
            criar_linha("D", "E")
        ],
        columns=COLUNAS_ENTRADA
    )


def atualizar_editor():
    st.session_state.editor_rede_versao += 1
    st.session_state.resultado_hidraulica = None


def adicionar_trecho():
    rede = st.session_state.rede.copy()

    ultimo_no_jusante = (
        rede.iloc[-1]["Nó Jusante"]
        if len(rede) > 0
        else "A"
    )

    novo_no_jusante = proximo_no(
        ultimo_no_jusante
    )

    nova_linha = criar_linha(
        ultimo_no_jusante,
        novo_no_jusante
    )

    st.session_state.rede = pd.concat(
        [
            rede,
            pd.DataFrame(
                [nova_linha],
                columns=COLUNAS_ENTRADA
            )
        ],
        ignore_index=True
    )

    atualizar_editor()


def remover_ultimo_trecho():
    if len(st.session_state.rede) > 1:
        st.session_state.rede = (
            st.session_state.rede
            .iloc[:-1]
            .reset_index(drop=True)
        )

    atualizar_editor()


def carregar_exemplo():
    st.session_state.rede = criar_rede_exemplo()
    atualizar_editor()


def limpar_rede():
    st.session_state.rede = criar_rede_padrao()
    atualizar_editor()


def valor_linha(
    linha,
    coluna,
    padrao=0.0
):
    if coluna not in linha:
        return padrao

    valor = linha[coluna]

    if pd.isna(valor):
        return padrao

    return valor


def montar_planilha_calculo(resultado):
    linhas = []

    for _, linha in resultado.iterrows():

        trecho = valor_linha(
            linha,
            "Trecho",
            ""
        )

        vazao = valor_linha(
            linha,
            "Vazão Informada"
        )

        q_calculado = valor_linha(
            linha,
            "Vazão Utilizada"
        )

        perda_total = valor_linha(
            linha,
            "Perda Total"
        )

        linhas.append({
            "Trecho": trecho,
            "Vazão (L/s)": vazao,
            "Pesos": valor_linha(linha, "Peso"),
            "Q (L/s)": q_calculado,
            "DN": valor_linha(linha, "DN", ""),
            "Material": valor_linha(linha, "Material", ""),
            "Vel.": valor_linha(linha, "Velocidade"),
            "Vel. max": 3.0,
            "J": valor_linha(linha, "j (mca/m)"),
            "Real": valor_linha(linha, "Comprimento Real"),
            "Equiv.": valor_linha(linha, "Comprimento Equiv."),
            "Total": valor_linha(linha, "Comprimento Total"),
            "Dif. Cota": valor_linha(linha, "Diferença de Cota"),
            "P mon": valor_linha(linha, "Pressão Montante"),
            "Linear": valor_linha(linha, "Perda Linear"),
            "Singular": valor_linha(linha, "Perda Singular"),
            "Total Perda": perda_total,
            "P jus": valor_linha(linha, "Pressão Jusante")
        })

    planilha = pd.DataFrame(
        linhas,
        columns=COLUNAS_PLANILHA
    )

    planilha.columns = pd.MultiIndex.from_tuples([
        ("Trecho", ""),
        ("Vazão Máx. Possível", "Vazão"),
        ("Vazão Máx. Provável", "Pesos"),
        ("Vazão Estimada", "Q=0,3P¹ᐟ²"),
        ("DN", "mm"),
        ("Material", ""),
        ("Vel.", "m/s"),
        ("Vel. máx", "m/s"),
        ("Perda de Carga Unit.", "J"),
        ("Comprimento da Tubulação", "Real"),
        ("Comprimento da Tubulação", "Equiv."),
        ("Comprimento da Tubulação", "Total"),
        ("Diferença de Cota", "Cmon-Cjus"),
        ("Pmon", "disp."),
        ("Perda de Carga", "Linear"),
        ("Perda de Carga", "Singular"),
        ("Perda de Carga", "Total"),
        ("Pjus", "residual")
    ])

    return planilha


def destacar_planilha(planilha):
    def estilo_coluna(coluna):
        estilos = []

        for valor in coluna:
            estilo = (
                "border: 1px solid #9ca3af; "
                "font-size: 12px;"
            )

            grupo = coluna.name[0]

            if grupo in [
                "Vazão Máx. Provável",
                "Vazão Estimada",
                "Perda de Carga Unit.",
                "Diferença de Cota",
                "Pmon",
                "Perda de Carga"
            ]:
                estilo += "background-color: #e5e7eb;"

            if grupo == "Vel.":
                estilo += "background-color: #fde68a;"

            if grupo == "Pjus":
                estilo += "background-color: #bbf7d0;"

            estilos.append(
                estilo
            )

        return estilos

    formatos = {
        coluna: "{:.2f}"
        for coluna in planilha.columns
        if coluna[0] not in [
            "Trecho",
            "Material",
            "DN"
        ]
    }

    formatos.update({
        ("DN", "mm"): "{}",
        ("Vel.", "m/s"): "{:.2f}",
        ("Vel. máx", "m/s"): "{:.2f}",
        ("Perda de Carga Unit.", "J"): "{:.3f}",
        ("Pjus", "residual"): "{:.2f}"
    })

    return (
        planilha
        .style
        .apply(estilo_coluna, axis=0)
        .format(formatos)
        .set_table_styles([
            {
                "selector": "th",
                "props": [
                    ("background-color", "#d9d9d9"),
                    ("color", "#111827"),
                    ("font-weight", "700"),
                    ("border", "1px solid #111827"),
                    ("font-size", "12px"),
                    ("text-align", "center")
                ]
            },
            {
                "selector": "td",
                "props": [
                    ("text-align", "center"),
                    ("padding", "3px 6px")
                ]
            }
        ])
    )


aplicar_design_system()

st.title(
    "Perda de Carga - Água Fria"
)

st.markdown(
    """
    <div class="et-toolbar">
        <div>
            <div class="et-toolbar-title">Planilha técnica de dimensionamento</div>
            <div class="et-toolbar-subtitle">
                Rede em série, com propagação de pressão trecho a trecho.
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

if "rede" not in st.session_state:
    st.session_state.rede = criar_rede_padrao()

if "resultado_hidraulica" not in st.session_state:
    st.session_state.resultado_hidraulica = None

if "editor_rede_versao" not in st.session_state:
    st.session_state.editor_rede_versao = 0


# =====================================================
# CONFIGURAÇÕES
# =====================================================

col_metodo, col_pressao = st.columns(
    [2, 1]
)

with col_metodo:
    metodo = st.selectbox(
        "Método Hidráulico",
        [
            "Universal",
            "Hazen-Williams",
            "Fair-Whipple-Hsiao"
        ]
    )

with col_pressao:
    pressao_disponivel = st.number_input(
        "Pressão Disponível",
        min_value=0.0,
        value=25.0,
        step=0.5
    )


# =====================================================
# AÇÕES
# =====================================================

st.markdown(
    '<div class="et-section-title">Entrada de dados</div>',
    unsafe_allow_html=True
)

col_adicionar, col_remover, col_exemplo, col_limpar = st.columns(
    4
)

with col_adicionar:
    st.button(
        "Adicionar trecho",
        width="stretch",
        on_click=adicionar_trecho
    )

with col_remover:
    st.button(
        "Remover último",
        width="stretch",
        on_click=remover_ultimo_trecho
    )

with col_exemplo:
    st.button(
        "Exemplo A-E",
        width="stretch",
        on_click=carregar_exemplo
    )

with col_limpar:
    st.button(
        "Limpar",
        width="stretch",
        on_click=limpar_rede
    )


# =====================================================
# ENTRADA
# =====================================================

with st.form("form_rede_hidraulica"):

    st.markdown(
        """
        <div class="et-sheet-hint">
            Edite os trechos e salve ou calcule. As linhas são adicionadas pelos botões acima para evitar registros vazios.
        </div>
        """,
        unsafe_allow_html=True
    )

    df_editado = st.data_editor(
        st.session_state.rede,
        key=f"editor_rede_{st.session_state.editor_rede_versao}",
        hide_index=True,
        num_rows="fixed",
        width="stretch",
        height=260,
        column_order=COLUNAS_ENTRADA,
        column_config={
            "Consumo":
            st.column_config.SelectboxColumn(
                "Consumo",
                options=[
                    "Máximo Possível",
                    "Máximo Provável"
                ],
                width="medium"
            ),

            "Nó Montante":
            st.column_config.TextColumn(
                "Trecho de",
                width="small"
            ),

            "Nó Jusante":
            st.column_config.TextColumn(
                "Trecho até",
                width="small"
            ),

            "Peso":
            st.column_config.NumberColumn(
                "Peso",
                min_value=0.0,
                width="small"
            ),

            "Vazão Informada":
            st.column_config.NumberColumn(
                "Vazão (L/s)",
                min_value=0.0,
                width="small"
            ),

            "Material":
            st.column_config.SelectboxColumn(
                "Material",
                options=obter_materiais(),
                width="medium"
            ),

            "DN":
            st.column_config.NumberColumn(
                "DN",
                min_value=0,
                width="small"
            ),

            "Comprimento Real":
            st.column_config.NumberColumn(
                "Real (m)",
                min_value=0.0,
                width="small"
            ),

            "Comprimento Equiv.":
            st.column_config.NumberColumn(
                "Equiv. (m)",
                min_value=0.0,
                width="small"
            ),

            "Diferença de Cota":
            st.column_config.NumberColumn(
                "Cota (m)",
                width="small"
            ),

            "Perda Adicional":
            st.column_config.NumberColumn(
                "Adic. (mca)",
                min_value=0.0,
                width="small"
            )
        }
    )

    col_salvar, col_calcular = st.columns(
        [1, 1]
    )

    with col_salvar:
        salvar = st.form_submit_button(
            "Salvar tabela",
            width="stretch"
        )

    with col_calcular:
        calcular = st.form_submit_button(
            "Calcular",
            width="stretch",
            type="primary"
        )


if salvar or calcular:
    st.session_state.rede = (
        df_editado[COLUNAS_ENTRADA]
        .reset_index(drop=True)
    )

if calcular:
    df_processamento = st.session_state.rede.copy()

    df_processamento[
        "Pressão Disponível"
    ] = pressao_disponivel

    st.session_state.resultado_hidraulica = (
        processar_tabela(
            df_processamento,
            metodo
        )
    )


# =====================================================
# RESULTADOS
# =====================================================

resultado = st.session_state.resultado_hidraulica

if resultado is not None:

    st.markdown(
        '<div class="et-section-title">Memória de cálculo</div>',
        unsafe_allow_html=True
    )

    planilha = montar_planilha_calculo(
        resultado
    )

    st.dataframe(
        destacar_planilha(
            planilha
        ),
        hide_index=True,
        width="stretch",
        height=260
    )

    colunas_resumo = [
        "Trecho",
        "Pressão Montante",
        "Perda Total",
        "Pressão Jusante",
        "Velocidade",
        "Regime",
        "Erro",
        "Erro Pressão"
    ]

    colunas_visiveis = [
        coluna
        for coluna in colunas_resumo
        if coluna in resultado.columns
    ]

    st.markdown(
        '<div class="et-section-title">Resumo hidráulico</div>',
        unsafe_allow_html=True
    )

    if len(colunas_visiveis) > 0:
        st.dataframe(
            resultado[colunas_visiveis],
            hide_index=True,
            width="stretch"
        )

    with st.expander(
        "Resultado completo"
    ):
        st.dataframe(
            resultado,
            hide_index=True,
            width="stretch"
        )
