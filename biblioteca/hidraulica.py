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

calcular_reynolds()

# =====================================================
# DARCY-WEISBACH
# =====================================================

calcular_fator_atrito()

calcular_perda_darcy()

# =====================================================
# HAZEN-WILLIAMS
# =====================================================

calcular_perda_hazen()

# =====================================================
# FAIR-WHIPPLE-HSIAO
# =====================================================

calcular_perda_fwh()

# =====================================================
# PRESSÕES
# =====================================================

calcular_pressao_jusante()

# =====================================================
# VALIDAÇÕES
# =====================================================

validar_velocidade()

validar_pressao()