import numpy as np
from copy import deepcopy

from besouros import (
    besouro,
    inicializar_populacao,
    mostrar_cor,
    mostrar_populacao, 
    mostrar_historico
)



# Inicializar população
populacao = inicializar_populacao(100)

# Mostrar população
# mostrar_populacao(populacao, colunas=5)


# SELEÇÃO POR TORNEIO
def selecao_torneio(populacao, k=3):

    candidatos = np.random.choice(populacao, k, replace=False)

    vencedor = max(candidatos, key=lambda ind: ind.fitness)

    return vencedor


# CRUZAMENTO ARITMÉTICO
def cruzamento(pai1, pai2):

    alpha = np.random.uniform(0, 1)

    filho = besouro(
        R=alpha*pai1.R + (1-alpha)*pai2.R,
        G=alpha*pai1.G + (1-alpha)*pai2.G,
        B=alpha*pai1.B + (1-alpha)*pai2.B
    )

    return filho


# MUTAÇÃO
def mutacao(individuo, taxa=0.1):

    if np.random.random() < taxa:
        individuo.R = np.clip(individuo.R + np.random.uniform(-0.1, 0.1), 0, 1)

    if np.random.random() < taxa:
        individuo.G = np.clip(individuo.G + np.random.uniform(-0.1, 0.1), 0, 1)

    if np.random.random() < taxa:
        individuo.B = np.clip(individuo.B + np.random.uniform(-0.1, 0.1), 0, 1)

    return individuo


# ALGORITMO GENÉTICO
def algoritmo_genetico(N=10, geracoes=100, meta=0.99):

    # 1 - INICIALIZAÇÃO
    populacao = inicializar_populacao(N)

    # Armazenar todas as gerações
    historico = [deepcopy(populacao)]

    for geracao in range(1, geracoes + 1):

        # 2 - AVALIAÇÃO
        melhor = max(populacao, key=lambda ind: ind.fitness)

        # Elitismo
        nova_populacao = sorted(
            populacao,
            key=lambda ind: ind.fitness,
            reverse=True
        )[:1]

        while len(nova_populacao) < N:

            # 3 - SELEÇÃO
            pai1 = selecao_torneio(populacao)

            candidatos = [ind for ind in populacao if ind is not pai1]

            pai2 = selecao_torneio(candidatos)

            # 4 - CRUZAMENTO
            filho = cruzamento(pai1, pai2)

            # 5 - MUTAÇÃO
            filho = mutacao(filho)

            nova_populacao.append(filho)

        # 6 - NOVA GERAÇÃO
        populacao = nova_populacao

        # Guardar a geração
        historico.append(deepcopy(populacao))

        melhor = max(populacao, key=lambda ind: ind.fitness)

        print(f"Geração {geracao}: fitness = {melhor.fitness:.6f}")

        # 7 - CRITÉRIO DE PARADA
        if melhor.fitness >= meta:
            break

    return populacao, melhor, historico

populacao_final, melhor, historico = algoritmo_genetico(
    N=16,
    geracoes=5,
    meta=0.99
)

mostrar_historico(historico)