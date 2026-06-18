"""
Perda de Carga - Água Fria

Primeira versão da ferramenta.
"""

import pandas as pd

from biblioteca.materiais_tubulacao import (
    obter_propriedades
)

from biblioteca.hidraulica import (
    calcular_velocidade,
    calcular_reynolds,
    classificar_regime,
    calcular_fator_atrito,
    calcular_j_darcy,
    calcular_j_hazen_williams,
    calcular_perda_linear,
    calcular_perda_singular,
    calcular_perda_total,
    propagar_pressao_rede_serie
)

from biblioteca.consumo_maximo_provavel import (
    calcular_vazao_maximo_provavel
)


def processar_tabela(
    df,
    metodo
):

    resultados = []

    for indice, linha in df.iterrows():

        try:

            material = linha["Material"]

            dn = linha["DN"]

            props = obter_propriedades(
                material,
                dn
            )

            # -------------------------
            # Trecho
            # -------------------------

            trecho = (
                f"{linha['Nó Montante']}"
                "-"
                f"{linha['Nó Jusante']}"
            )

            # -------------------------
            # Vazão
            # -------------------------

            if (
                linha["Consumo"]
                ==
                "Máximo Provável"
            ):

                vazao = (
                    calcular_vazao_maximo_provavel(
                        linha["Peso"]
                    )
                )

            else:

                vazao = (
                    linha["Vazão Informada"]
                )

            # -------------------------
            # Área
            # -------------------------

            area = props["area_m2"]

            # -------------------------
            # Velocidade
            # -------------------------

            velocidade = (
                calcular_velocidade(
                    vazao,
                    area
                )
            )

            # -------------------------
            # Reynolds
            # -------------------------

            reynolds = (
                calcular_reynolds(
                    velocidade,
                    props[
                        "diametro_interno_mm"
                    ]
                )
            )

            regime = (
                classificar_regime(
                    reynolds
                )
            )

            # -------------------------
            # Perda unitária
            # -------------------------

            if metodo == "Hazen-Williams":

                j = (
                    calcular_j_hazen_williams(
                        vazao,
                        props[
                            "diametro_interno_mm"
                        ],
                        props[
                            "coef_hazen"
                        ]
                    )
                )

            else:

                fator = (
                    calcular_fator_atrito(
                        reynolds,
                        props[
                            "rugosidade_mm"
                        ],
                        props[
                            "diametro_interno_mm"
                        ]
                    )
                )

                j = (
                    calcular_j_darcy(
                        fator,
                        velocidade,
                        props[
                            "diametro_interno_mm"
                        ]
                    )
                )

            # -------------------------
            # Comprimentos
            # -------------------------

            comprimento_real = (
                linha["Comprimento Real"]
            )

            comprimento_equiv = (
                linha["Comprimento Equiv."]
            )

            comprimento_total = (
                comprimento_real
                +
                comprimento_equiv
            )

            # -------------------------
            # Perdas
            # -------------------------

            perda_linear = (
                calcular_perda_linear(
                    j,
                    comprimento_real
                )
            )

            perda_singular = (
                calcular_perda_singular(
                    j,
                    comprimento_equiv
                )
            )

            perda_total = (
                calcular_perda_total(
                    perda_linear,
                    perda_singular,
                    linha[
                        "Perda Adicional"
                    ],
                    linha[
                        "Diferença de Cota"
                    ]
                )
            )

            # -------------------------
            # Resultado
            # -------------------------

            resultados.append({

                **linha,

                "Trecho":
                trecho,

                "DI (mm)":
                props[
                    "diametro_interno_mm"
                ],

                "Área (m²)":
                area,

                "Vazão Utilizada":
                vazao,

                "Velocidade":
                velocidade,

                "Reynolds":
                reynolds,

                "Regime":
                regime,

                "j (mca/m)":
                j,

                "Comprimento Total":
                comprimento_total,

                "Perda Linear":
                perda_linear,

                "Perda Singular":
                perda_singular,

                "Perda Total":
                perda_total
            })

        except Exception as erro:

            resultados.append({

                **linha,

                "Erro":
                str(erro)
            })

    # -------------------------
    # Propagação de pressões
    # -------------------------

    if len(resultados) > 0:

        indices_validos = []

        propagacao_interrompida = False

        for indice, resultado in enumerate(
            resultados
        ):

            if "Erro" in resultado:

                propagacao_interrompida = True
                continue

            if propagacao_interrompida:

                resultado[
                    "Erro Pressão"
                ] = (
                    "Propagação interrompida por "
                    "erro em trecho anterior."
                )

                continue

            indices_validos.append(
                indice
            )

        trechos_validos = [
            resultados[indice]
            for indice in indices_validos
        ]

        if len(trechos_validos) > 0:

            try:

                if "Pressão Disponível" not in df.columns:
                    raise ValueError(
                        "Coluna Pressão Disponível não encontrada."
                    )

                pressao_inicial = (
                    df.iloc[0][
                        "Pressão Disponível"
                    ]
                )

                trechos_propagados = (
                    propagar_pressao_rede_serie(
                        trechos_validos,
                        pressao_inicial
                    )
                )

                for indice, trecho in zip(
                    indices_validos,
                    trechos_propagados
                ):

                    resultados[indice] = trecho

            except Exception as erro:

                for indice in indices_validos:

                    resultados[indice][
                        "Erro Pressão"
                    ] = str(erro)

    return pd.DataFrame(
        resultados
    )
