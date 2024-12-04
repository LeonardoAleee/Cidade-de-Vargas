from main import *
# Parâmetros: grid 5x5, 4 regiões
cidade = generate_city(5, 5, 4)

# Construir a planta inicial da cidade para análise
cidade.construir_planta_tarefa1()
cidade.construir_planta_tarefa2()

# Exibir algumas informações sobre a cidade
print(f"Cidade criada com {len(cidade.Cruzamentos)} cruzamentos.")
print(f"Total de segmentos na cidade: {len(cidade.Segmentos)}")

# Pegando o primeiro cruzamento da cidade como ponto de partida
start_cruzamento = list(cidade.Cruzamentos.values())[0]

# Planejar linha de ônibus
linha_onibus = cidade.planejar_linha_onibus(start_cruzamento)

# Exibir a rota planejada
print("Linha de ônibus planejada:")
for segmento in linha_onibus:
    print(f"Segmento {segmento.ID_do_segmento}: de {segmento.cruzamento_inicial.ID} para {segmento.cruzamento_final.ID}")

# Planejar linhas de metrô
metro_mst = cidade.planejar_metro()

# Exibir as conexões das estações de metrô
print("Conexões de metrô planejadas:")
for custo, estacao_a, estacao_b in metro_mst:
    print(f"Conexão entre {estacao_a} e {estacao_b} com custo {custo}")

# Criar o mapa multimodal baseado na cidade
mapa = Mapa(cidade)
mapa.construir_grafo()

# Configurar origem, destino e custo máximo
origem = 0  # ID do cruzamento de origem
destino = 24  # ID do cruzamento de destino
custo_maximo = 10  # Exemplo de custo máximo

# Buscar rota
rota = buscar_rota(mapa, origem, destino, custo_maximo)

# Atualizar condições de trânsito
fator_taxi = 0.5  # Reduz velocidade dos táxis pela metade
fator_onibus = 0.8  # Reduz velocidade dos ônibus para 80%

mapa.atualizar_condicoes_transito(fator_taxi, fator_onibus)

# Buscar rota novamente com as condições atualizadas
rota = buscar_rota(mapa, origem, destino, custo_maximo)

import random

def simular_transito():
    # Gera fatores de trânsito aleatórios para táxi e ônibus
    fator_taxi = random.uniform(0.5, 1.0)  # Velocidade varia entre 50% e 100%
    fator_onibus = random.uniform(0.3, 0.8)  # Velocidade varia entre 30% e 80%
    return fator_taxi, fator_onibus

# Atualizar condições com base em simulação
fator_taxi, fator_onibus = simular_transito()
mapa.atualizar_condicoes_transito(fator_taxi, fator_onibus)

# Criar a cidade
cidade = generate_city(5, 5, 4)

# Construir a planta inicial da cidade para análise
cidade.construir_planta_tarefa1()
cidade.construir_planta_tarefa2()

# Exibir informações sobre a cidade
print(f"Cidade criada com {len(cidade.Cruzamentos)} cruzamentos.")
print(f"Total de segmentos na cidade: {len(cidade.Segmentos)}")

# Definir as estações e planejar as linhas de metrô e ônibus
cidade.definir_estacoes()
cidade.planejar_linha_onibus(list(cidade.Cruzamentos.values())[0])

# Criar o mapa multimodal
mapa = Mapa(cidade)
mapa.construir_grafo()

# Configurar origem, destino e custo máximo
origem = 0  # ID do cruzamento de origem
destino = 24  # ID do cruzamento de destino
custo_maximo = 15  # Exemplo de custo máximo

# Buscar rota
print("\nBuscando rota:")
rota = buscar_rota(mapa, origem, destino, custo_maximo)

# Calcular o tempo total de percurso e exibir detalhes da rota
def exibir_detalhes_rota(rota):
    if not rota:
        print("Nenhuma rota encontrada.")
        return
    
    tempo_total = 0
    print("\nDetalhes da Rota:")
    for aresta, meio in rota:
        tempo = aresta.meios_de_transporte[meio]["tempo"]
        tempo_total += tempo
        print(f"{meio.capitalize()}: {aresta.origem} -> {aresta.destino}, Tempo: {tempo:.2f} min")
    
    print(f"\nTempo total de percurso: {tempo_total:.2f} min")

# Exibir detalhes da rota encontrada
exibir_detalhes_rota(rota)

# Atualizar condições de trânsito
fator_taxi = 0.7  # Reduz velocidade dos táxis para 70%
fator_onibus = 0.6  # Reduz velocidade dos ônibus para 60%
mapa.atualizar_condicoes_transito(fator_taxi, fator_onibus)

# Buscar rota novamente com as condições de trânsito atualizadas
print("\nBuscando rota com condições de trânsito atualizadas:")
rota_atualizada = buscar_rota(mapa, origem, destino, custo_maximo)

# Exibir detalhes da rota atualizada
exibir_detalhes_rota(rota_atualizada)

mapa.atualizar_condicoes_transito_randomico()
# Buscar rota novamente com as condições de trânsito atualizadas
print("\nBuscando rota com condições de trânsito atualizadas:")
rota_atualizada = buscar_rota(mapa, origem, destino, custo_maximo)

# Exibir detalhes da rota atualizada
exibir_detalhes_rota(rota_atualizada)
