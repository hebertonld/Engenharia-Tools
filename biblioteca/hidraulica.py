"""
Motor Hidráulico

Projeto:
    Engenharia Tools

Objetivo:
    Centralizar cálculos hidráulicos
    utilizados pelas ferramentas.

Referências:
    ABNT NBR 5626
    Azevedo Netto
"""

from math import log10

from biblioteca.constantes import (
    VISCOSIDADE_AGUA_20C,
    GRAVIDADE
)

from biblioteca.normas import (
    RE_LAMINAR,
    RE_TRANSICAO
)

# =====================================================
# VELOCIDADE
# =====================================================

def calcular_velocidade(
    vazao_ls,
    area_m2
):
    """
    Calcula velocidade do escoamento.

    Entradas:
        vazao_ls [L/s]
        area_m2 [m²]

    Saída:
        velocidade [m/s]

    Tratamento de erros:
        Área deve ser maior que zero.
    """

    if area_m2 <= 0:
        raise ValueError(
            "Área deve ser maior que zero."
        )

    vazao_m3s = vazao_ls / 1000

    return vazao_m3s / area_m2


# =====================================================
# REYNOLDS
# =====================================================

def calcular_reynolds(
    velocidade_m_s,
    diametro_interno_mm
):
    """
    Calcula o número de Reynolds.

    Entradas:
        velocidade_m_s [m/s]
        diametro_interno_mm [mm]

    Saída:
        reynolds [-]

    Tratamento de erros:
        Diâmetro deve ser maior que zero.
    """

    if diametro_interno_mm <= 0:
        raise ValueError(
            "Diâmetro deve ser maior que zero."
        )

    diametro_m = diametro_interno_mm / 1000

    return (
        velocidade_m_s
        * diametro_m
        / VISCOSIDADE_AGUA_20C
    )
# =====================================================
# REGIME DE ESCOAMENTO
# =====================================================

def classificar_regime(reynolds):
    """
    Classifica o regime de escoamento.

    Retorno:
        Laminar
        Transição
        Turbulento
    """

    if reynolds < RE_LAMINAR:
        return "Laminar"

    if reynolds <= RE_TRANSICAO:
        return "Transição"

    return "Turbulento"
# =====================================================
# FATOR DE ATRITO
# =====================================================

def calcular_fator_atrito(
    reynolds,
    rugosidade_mm,
    diametro_interno_mm
):
    """
    Calcula fator de atrito Darcy.

    Laminar:
        f = 64/Re

    Turbulento:
        Swamee-Jain

    Transição:
        Swamee-Jain
    """

    if reynolds <= 0:
        raise ValueError(
            "Reynolds inválido."
        )

    if reynolds < RE_LAMINAR:

        return 64 / reynolds

    diametro_m = (
        diametro_interno_mm / 1000
    )

    rugosidade_m = (
        rugosidade_mm / 1000
    )

    return (
        0.25
        /
        (
            log10(
                (
                    rugosidade_m
                    /
                    (
                        3.7
                        * diametro_m
                    )
                )
                +
                (
                    5.74
                    /
                    (
                        reynolds ** 0.9
                    )
                )
            )
        ) ** 2
    )
# =====================================================
# DARCY-WEISBACH
# =====================================================

def calcular_j_darcy(
    fator_atrito,
    velocidade_m_s,
    diametro_interno_mm
):
    """
    Perda de carga unitária.

    Retorno:
        j [mca/m]
    """

    diametro_m = (
        diametro_interno_mm / 1000
    )

    return (
        fator_atrito
        *
        (
            velocidade_m_s ** 2
        )
        /
        (
            2
            *
            GRAVIDADE
            *
            diametro_m
        )
    )
# =====================================================
# HAZEN-WILLIAMS
# =====================================================

def calcular_j_hazen_williams(
    vazao_ls,
    diametro_interno_mm,
    coef_hazen
):
    """
    Calcula a perda de carga unitária
    pelo método de Hazen-Williams.

    Entradas:
        vazao_ls [L/s]
        diametro_interno_mm [mm]
        coef_hazen [-]

    Saída:
        j [mca/m]

    Referência:
        Azevedo Netto
        NBR 5626
    """

    if vazao_ls <= 0:
        raise ValueError(
            "Vazão deve ser maior que zero."
        )

    if diametro_interno_mm <= 0:
        raise ValueError(
            "Diâmetro deve ser maior que zero."
        )

    if coef_hazen <= 0:
        raise ValueError(
            "Coeficiente Hazen deve ser maior que zero."
        )

    q = vazao_ls / 1000

    d = diametro_interno_mm / 1000

    j = (
        10.643
        * (q ** 1.852)
        / (
            (coef_hazen ** 1.852)
            * (d ** 4.871)
        )
    )

    return j


def calcular_perda_linear(
    j,
    comprimento_m
):
    """
    Calcula perda de carga linear.

    Entradas:
        j [mca/m]
        comprimento_m [m]

    Saída:
        hf [mca]
    """

    if comprimento_m < 0:
        raise ValueError(
            "Comprimento inválido."
        )

    return j * comprimento_m

# =====================================================
# PERDAS DE CARGA
# =====================================================

def calcular_perda_linear(
    j,
    comprimento_real_m
):
    """
    Perda de carga linear.

    hf = j × L
    """

    return (
        j
        *
        comprimento_real_m
    )


def calcular_perda_singular(
    j,
    comprimento_equivalente_m
):
    """
    Perda singular por
    comprimento equivalente.
    """

    return (
        j
        *
        comprimento_equivalente_m
    )


def calcular_perda_total(
    perda_linear,
    perda_singular,
    perda_adicional,
    diferenca_cota
):
    """
    Perda total do trecho.

    Convenção:

    Δz positivo:
        favorece o escoamento

    Δz negativo:
        desfavorece o escoamento
    """

    return (

        perda_linear

        +

        perda_singular

        +

        perda_adicional

        -

        diferenca_cota

    )
# =====================================================
# PRESSÕES
# =====================================================

def calcular_pressao_jusante(
    pressao_montante,
    perda_total
):
    """
    Pressão residual.
    """

    return (

        pressao_montante

        -

        perda_total

    )