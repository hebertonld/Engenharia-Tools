"""
Base Técnica de Tubulações

Projeto:
    Engenharia Tools

Objetivo:
    Centralizar propriedades hidráulicas dos materiais
    utilizados pelas ferramentas da plataforma.

Referências:
    ABNT NBR 5626
    ABNT NBR 5648
    ABNT NBR 12218
    ABNT NBR 12266
    Catálogos Tigre
    Catálogos Amanco
    Saint-Gobain PAM
"""

from math import pi


# =====================================================
# FUNÇÕES AUXILIARES
# =====================================================

def calcular_area(diametro_interno_mm):
    """
    Calcula área interna do tubo.

    Entrada:
        diametro_interno_mm [mm]

    Saída:
        área [m²]
    """

    diametro_m = diametro_interno_mm / 1000

    return (pi * diametro_m**2) / 4


def criar_diametro(
    dn,
    diametro_interno_mm
):
    """
    Cria registro padronizado de diâmetro.
    """

    return {
        "dn": dn,
        "diametro_interno_mm": diametro_interno_mm,
        "area_m2": calcular_area(
            diametro_interno_mm
        )
    }
MATERIAIS = {

    "PVC SOLDAVEL": {

        "norma": "ABNT NBR 5648",

        "coef_hazen": 150,

        "coef_fwh": 150,

        "rugosidade_mm": 0.0015,

        "diametros": [

            criar_diametro(20, 17.0),
            criar_diametro(25, 21.6),
            criar_diametro(32, 27.8),
            criar_diametro(40, 35.2),
            criar_diametro(50, 44.0),
            criar_diametro(60, 53.4),
            criar_diametro(75, 66.6),
            criar_diametro(85, 75.6),
            criar_diametro(110, 97.8)

        ]
    },

    "CPVC": {

        "norma": "ASTM D2846",

        "coef_hazen": 150,

        "coef_fwh": 150,

        "rugosidade_mm": 0.0015,

        "diametros": [

            criar_diametro(15, 11.9),
            criar_diametro(22, 18.1),
            criar_diametro(28, 23.1),
            criar_diametro(35, 37.4),
            criar_diametro(42, 33.6),
            criar_diametro(54, 44.1),
            criar_diametro(73, 59.9),
            criar_diametro(89, 72.8),
            criar_diametro(114, 93.6)

        ]
    },
     "PPR PN12": {

        "norma": "ABNT NBR 15813",

        "coef_hazen": 150,

        "coef_fwh": 150,

        "rugosidade_mm": 0.007,

        "diametros": [

            criar_diametro(32, 26.2),
            criar_diametro(40, 32.6),
            criar_diametro(50, 40.8),
            criar_diametro(63, 51.4),
            criar_diametro(75, 61.4),
            criar_diametro(90, 73.6),
            criar_diametro(110, 90.0)

        ]
    },

    "PPR PN20": {

        "norma": "ABNT NBR 15813",

        "coef_hazen": 150,

        "coef_fwh": 150,

        "rugosidade_mm": 0.007,

        "diametros": [

            criar_diametro(20, 14.4),
            criar_diametro(25, 18.0),
            criar_diametro(32, 23.2),
            criar_diametro(40, 29.0),
            criar_diametro(50, 36.2),
            criar_diametro(63, 45.8),
            criar_diametro(75, 54.4),
            criar_diametro(90, 65.4),
            criar_diametro(110, 79.8)

        ]
    },

    "PPR PN25": {

        "norma": "ABNT NBR 15813",

        "coef_hazen": 150,

        "coef_fwh": 150,

        "rugosidade_mm": 0.007,

        "diametros": [

            criar_diametro(20, 13.2),
            criar_diametro(25, 16.6),
            criar_diametro(32, 21.2),
            criar_diametro(40, 26.6),
            criar_diametro(50, 33.4),
            criar_diametro(63, 42.0),
            criar_diametro(75, 50.0),
            criar_diametro(90, 60.0),
            criar_diametro(110, 75.4)

        ]
    },
        "ACO NBR 5580": {

        "norma": "ABNT NBR 5580",

        "coef_hazen": 120,

        "coef_fwh": 100,

        "rugosidade_mm": 0.045,

        "diametros": [

            criar_diametro("1/2", 16.8),
            criar_diametro("3/4", 22.4),
            criar_diametro("1", 28.4),
            criar_diametro("1 1/4", 37.1),
            criar_diametro("1 1/2", 42.3),
            criar_diametro("2", 54.3),
            criar_diametro("2 1/2", 69.4),
            criar_diametro("3", 82.2),
            criar_diametro("3 1/2", 94.1),
            criar_diametro("4", 106.8),
            criar_diametro("5", 139.7),
            criar_diametro("6", 165.1)

        ]
    },
}
# =====================================================
# CONSULTAS
# =====================================================

def obter_materiais():
    """
    Retorna lista de materiais.
    """

    return sorted(
        list(MATERIAIS.keys())
    )


def obter_diametros(material):
    """
    Retorna DNs disponíveis.
    """

    return [

        item["dn"]

        for item in
        MATERIAIS[material]["diametros"]

    ]


def obter_propriedades(
    material,
    dn
):
    """
    Retorna propriedades hidráulicas.
    """

    for item in MATERIAIS[
        material
    ]["diametros"]:

        if item["dn"] == dn:

            return {

                "material": material,

                "coef_hazen":
                MATERIAIS[material][
                    "coef_hazen"
                ],

                "rugosidade_mm":
                MATERIAIS[material][
                    "rugosidade_mm"
                ],

                **item

            }

    raise ValueError(
        f"DN {dn} não encontrado."
    )