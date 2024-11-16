class Cruzamento:
    def __init__(self, ID, cep):
        self.ID = ID
        self.cep = cep #como se fosse o ID da região
        

class Segmento:
    def __init__(self, ID_do_segmento, distancia, custo_de_escavacao, cruzamento_inicial, cruzamento_final):
        self.ID_do_segmento = ID_do_segmento
        self.distancia = distancia
        self.custo_de_escavacao = custo_de_escavacao
        self.cruzamento_inicial = cruzamento_inicial  # objeto Cruzamento
        self.cruzamento_final = cruzamento_final      # objeto Cruzamento
        self.conjunto_de_imoveis = None  # Futuramente um conjunto com objetos do tipo Imóvel


class Cidade:
    def __init__(self):
        self.Segmentos = []  # Lista de objetos do tipo Segmento
        self.Planta = {}     # Grafo - {cruzamento_ID: [(cruzamento_adjacente_ID, custo_de_escavacao, distancia), ...]}
        self.Regioes = {}    # Regioes - {regiao_ID: set of cruzamento IDs}
        self.Subgrafos_Regioes = {}  # Guarda os subgrafos das regiões


    def adicionar_segmento(self, segmento):
        self.Segmentos.append(segmento)
        
        # Já adiciona os cruzamentos do segmento, às suas respectivas regiões
        for cruzamento in [segmento.cruzamento_inicial, segmento.cruzamento_final]:
            regiao_id = cruzamento.cep 
            if regiao_id not in self.Regioes:
                self.Regioes[regiao_id] = set()
            self.Regioes[regiao_id].add(cruzamento.ID)

    def construir_planta(self):
        self.Planta = {}
        for segmento in self.Segmentos:
            ci_id = segmento.cruzamento_inicial.ID
            cf_id = segmento.cruzamento_final.ID
            
            # Como o grafo é não dirigido criamos 2 arestas uma de i para j e outra de j para i
            edge_data = (cf_id, segmento.custo_de_escavacao, segmento.distancia)
            self.Planta.setdefault(ci_id, []).append(edge_data)
            
            edge_data_reverse = (ci_id, segmento.custo_de_escavacao, segmento.distancia)
            self.Planta.setdefault(cf_id, []).append(edge_data_reverse)

    def construir_subgrafos_regioes(self):
        self.Subgrafos_Regioes = {}

        for regiao_id, cruzamentos in self.Regioes.items():
            
            subgrafo = {}
            for cruzamento_id in cruzamentos:
                subgrafo[cruzamento_id] = []
                for edge in self.Planta.get(cruzamento_id, []):
                    adj_cruzamento_id, custo, distancia = edge # edge é uma tupla
                    if adj_cruzamento_id in cruzamentos:
                        subgrafo[cruzamento_id].append(edge)

            self.Subgrafos_Regioes[regiao_id] = subgrafo

########################################## Exemplo: ##########################################

# RegiaoA                      RegiaoB
#    1A ------(100)------- 2A --------(150)-------- 3B
#    |                                               |
#   (120)                                          (200)
#    |                                               |
#    5A -------------------(80)-------------------- 4B

cruzamento1 = Cruzamento(ID=1, cep='RegiaoA')
cruzamento2 = Cruzamento(ID=2, cep='RegiaoA')
cruzamento3 = Cruzamento(ID=3, cep='RegiaoB')
cruzamento4 = Cruzamento(ID=4, cep='RegiaoB')
cruzamento5 = Cruzamento(ID=5, cep='RegiaoA')

segmento1 = Segmento(
    ID_do_segmento=101,
    distancia=100.0,
    custo_de_escavacao=5000.0,
    cruzamento_inicial=cruzamento1,
    cruzamento_final=cruzamento2
)

segmento2 = Segmento(
    ID_do_segmento=102,
    distancia=150.0,
    custo_de_escavacao=7500.0,
    cruzamento_inicial=cruzamento2,
    cruzamento_final=cruzamento3
)

segmento3 = Segmento(
    ID_do_segmento=103,
    distancia=200.0,
    custo_de_escavacao=10000.0,
    cruzamento_inicial=cruzamento3,
    cruzamento_final=cruzamento4
)

segmento4 = Segmento(
    ID_do_segmento=104,
    distancia=120.0,
    custo_de_escavacao=6000.0,
    cruzamento_inicial=cruzamento1,
    cruzamento_final=cruzamento5
)

segmento5 = Segmento(
    ID_do_segmento=105,
    distancia=80.0,
    custo_de_escavacao=4000.0,
    cruzamento_inicial=cruzamento5,
    cruzamento_final=cruzamento4
)

cidade = Cidade()
cidade.adicionar_segmento(segmento1)
cidade.adicionar_segmento(segmento2)
cidade.adicionar_segmento(segmento3)
cidade.adicionar_segmento(segmento4)
cidade.adicionar_segmento(segmento5)

cidade.construir_planta()

cidade.construir_subgrafos_regioes()

print("Planta (Grafo):")
for cruzamento_id, edges in cidade.Planta.items():
    print(f"Cruzamento {cruzamento_id}: {edges}")

# Output:
# Planta (Grafo):
# Cruzamento 1: [(2, 5000.0, 100.0)]
# Cruzamento 2: [(1, 5000.0, 100.0), (3, 7500.0, 150.0)]
# Cruzamento 3: [(2, 7500.0, 150.0), (4, 10000.0, 200.0)]
# Cruzamento 4: [(3, 10000.0, 200.0)]
# Cruzamento 5: [(1, 6000.0, 120.0), (4, 4000.0, 80.0)]
print("\nRegiões:")
for regiao_id, cruzamentos in cidade.Regioes.items():
    print(f"Região {regiao_id}: Cruzamentos {cruzamentos}")

# Output:
# Regiões:
# Região RegiaoA: Cruzamentos {1, 2, 5}
# Região RegiaoB: Cruzamentos {3, 4}


print("\nSubgrafos por Região:")
for regiao_id, subgrafo in cidade.Subgrafos_Regioes.items():
    print(f"\n Sugrafo da {regiao_id}:")
    for cruzamento_id, edges in subgrafo.items():
        print(f"  Cruzamento {cruzamento_id}: {edges}")

#### Implementando algoritmo de calcular distâncias ####

import heapq
from math import inf


def calcular_distancias(subgrafo, origem):
    # Dicionário armazenando as distâncias:
    distancias = {v : inf for v in subgrafo}

    distancias[origem] = 0
    # Criar uma heap de prioridades
    heap = [(0, origem)]

    while heap:
        dist_atual , cruzamento_atual = heapq.heappop(heap)
        # se a distância for maior, vá ao próximo vértice
        if dist_atual > distancias[cruzamento_atual]:
            continue
        for adj, _, distancia in subgrafo[cruzamento_atual]:
            nova_distancia = dist_atual + distancia
            if nova_distancia < distancias[adj]:
                distancias[adj] = nova_distancia
                heapq.heappush(heap, (nova_distancia, adj))

    return distancias

### Exemplo com djikstra
for i in cidade.Planta:
    print(f"Distâncias do cruzamento {i} aos outros no grafo principal:")
    distancias = calcular_distancias(cidade.Planta, i)
    for cruzamento, distancia in distancias.items():
        print(f"Cruzamento {cruzamento}: {distancia}")
    print("|-----|"*10)
