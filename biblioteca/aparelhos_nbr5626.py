"""
Aparelhos Sanitários

Referências:

ABNT NBR 5626
Azevedo Netto
"""

APARELHOS = {

    "Bacia Sanitária c/ Caixa Acoplada": {

        "peso": 0.3,
        "pressao_minima_kpa": 10

    },

    "Bacia Sanitária c/ Válvula de Descarga": {

        "peso": 32.0,
        "pressao_minima_kpa": 150

    },

    "Lavatório": {

        "peso": 0.3,
        "pressao_minima_kpa": 10

    },

    "Chuveiro": {

        "peso": 0.4,
        "pressao_minima_kpa": 10

    },

    "Ducha Higiênica": {

        "peso": 0.1,
        "pressao_minima_kpa": 10

    },

    "Bidê": {

        "peso": 0.1,
        "pressao_minima_kpa": 10

    },

    "Pia de Cozinha": {

        "peso": 0.7,
        "pressao_minima_kpa": 10

    },

    "Tanque": {

        "peso": 0.7,
        "pressao_minima_kpa": 10

    },

    "Máquina de Lavar Roupas": {

        "peso": 1.0,
        "pressao_minima_kpa": 10

    },

    "Torneira de Jardim": {

        "peso": 0.4,
        "pressao_minima_kpa": 10

    }

}
# =====================================================
# CONSULTAS
# =====================================================

def obter_aparelhos():

    return sorted(
        list(APARELHOS.keys())
    )


def obter_peso(aparelho):

    return APARELHOS[
        aparelho
    ]["peso"]


def obter_pressao_minima(aparelho):

    return APARELHOS[
        aparelho
    ]["pressao_minima_kpa"]