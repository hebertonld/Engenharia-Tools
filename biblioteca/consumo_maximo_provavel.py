"""
Consumo Máximo Provável

Referências:

ABNT NBR 5626
Azevedo Netto
"""

from math import sqrt


# =====================================================
# CONSUMO MÁXIMO PROVÁVEL
# =====================================================

def calcular_vazao_maximo_provavel(
    soma_pesos
):
    """
    Calcula vazão máxima provável.

    Equação adotada:

    Q = 0,3 × √P

    Onde:

    Q = vazão [L/s]

    P = soma dos pesos

    Referência:
        Azevedo Netto
    """

    if soma_pesos < 0:

        raise ValueError(
            "Soma dos pesos não pode ser negativa."
        )

    return (
        0.3
        *
        sqrt(soma_pesos)
    )