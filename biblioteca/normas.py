"""
Parâmetros Normativos

Hierarquia:

1. ABNT
2. Azevedo Netto
3. Usuário
"""

VELOCIDADE_MAXIMA = {

    "PVC SOLDAVEL": 3.0,
    "CPVC": 3.0,
    "PPR PN12": 3.0,
    "PPR PN20": 3.0,
    "PPR PN25": 3.0,
    "ACO NBR 5580": 3.5,
    "SCH40": 3.5,
    "SCH80": 3.5

}

# mca
PRESSAO_DINAMICA_MINIMA = 10.0

# mca (400 kPa)
PRESSAO_ESTATICA_MAXIMA = 40.0

# =====================================================
# REYNOLDS
# =====================================================

RE_LAMINAR = 2000

RE_TRANSICAO = 4000