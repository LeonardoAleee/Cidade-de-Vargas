class Imovel:
    def __init__(self, ID, cep, tipo, rua, numero):
        self.ID = ID
        self.cep = cep  # Como se fosse o ID da região
        self.tipo = tipo  # Tipos: 'R', 'C', 'I', 'T'
        self.rua = rua
        self.numero = numero

class Cruzamento:
    def __init__(self, ID, cep):
        self.ID = ID
        self.cep = cep  # ID da região

class Segmento:
    def __init__(self, ID_do_segmento, distancia, custo_de_escavacao, cruzamento_inicial, cruzamento_final, limite_de_velocidade=60):
        self.ID_do_segmento = ID_do_segmento
        self.distancia = distancia
        self.custo_de_escavacao = custo_de_escavacao
        self.cruzamento_inicial = cruzamento_inicial
        self.cruzamento_final = cruzamento_final
        self.limite_de_velocidade = limite_de_velocidade

        self.conjunto_de_imoveis = {}

        self.quantidade_residencial = 0
        self.quantidade_comercial = 0
        self.quantidade_industrial = 0
        self.quantidade_turistico = 0

    def adicionar_imovel(self, imovel):
        if imovel.ID not in self.conjunto_de_imoveis:
            self.conjunto_de_imoveis[imovel.ID] = imovel
            
            # Atualiza a contagem com base no tipo do imóvel
            if imovel.tipo == "R":
                self.quantidade_residencial += 1
            elif imovel.tipo == "C":
                self.quantidade_comercial += 1
            elif imovel.tipo == "I":
                self.quantidade_industrial += 1
            elif imovel.tipo == "T":
                self.quantidade_turistico += 1


class Cidade:
    def __init__(self):
        self.Segmentos = {}  # Dicionário {ID_do_segmento: objeto Segmento}
        self.Planta = {}     # Grafo - {cruzamento_ID: [(cruzamento_adjacente_ID, custo_de_escavacao, distancia), ...]}
        self.Regioes = {}    # Regiões - {regiao_ID: set of cruzamento IDs}
        self.Subgrafos_Regioes = {}  # Guarda os subgrafos das regiões

    def adicionar_segmento(self, segmento):
        # Adiciona o segmento ao dicionário usando seu ID como chave
        self.Segmentos[segmento.ID_do_segmento] = segmento
        
        # Já adiciona os cruzamentos do segmento às suas respectivas regiões
        for cruzamento in [segmento.cruzamento_inicial, segmento.cruzamento_final]:
            regiao_id = cruzamento.cep
            if regiao_id not in self.Regioes:
                self.Regioes[regiao_id] = set()
            self.Regioes[regiao_id].add(cruzamento.ID)

    #Usada apenas para Tarefa 1 e 2
    def construir_planta(self):
        self.Planta = {}
        # Itera pelos segmentos no dicionário
        for segmento in self.Segmentos.values():
            ci_id = segmento.cruzamento_inicial.ID
            cf_id = segmento.cruzamento_final.ID
            
            # Como o grafo é não dirigido, criamos 2 arestas: uma de i para j e outra de j para i
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
                    adj_cruzamento_id, custo, distancia = edge
                    if adj_cruzamento_id in cruzamentos:
                        subgrafo[cruzamento_id].append(edge)

            self.Subgrafos_Regioes[regiao_id] = subgrafo





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

