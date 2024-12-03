import heapq
from math import inf
from collections import defaultdict
import math
import random

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
        self.Segmentos = {}
        self.PlantaPesos = {}
        self.Regioes = {}
        self.Cruzamentos = {}

        

    def adicionar_segmento(self, segmento):
        self.Segmentos[segmento.ID_do_segmento] = segmento
        for cruzamento in [segmento.cruzamento_inicial, segmento.cruzamento_final]:
            regiao_id = cruzamento.cep
            if regiao_id not in self.Regioes:
                self.Regioes[regiao_id] = set()
            self.Regioes[regiao_id].add(cruzamento.ID)
            self.Cruzamentos[cruzamento.ID] = cruzamento

    def get_cruzamento_region(self, cruz_id):
        return self.Cruzamentos[cruz_id].cep

    def construir_planta_tarefa1(self):
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

    def construir_planta_tarefa2(self):
        self.PlantaPesos = {}
        pesos = []
        for segmento in self.Segmentos.values():
            ci_id = segmento.cruzamento_inicial.ID
            cf_id = segmento.cruzamento_final.ID

            # Calcular o peso com base nos tipos de imóveis adjacentes
            peso = (
                -2 * segmento.quantidade_comercial -
                2 * segmento.quantidade_turistico +
                1 * segmento.quantidade_residencial +
                1 * segmento.quantidade_industrial
            )
            pesos.append(peso)
            segmento.peso = peso  # Armazena o peso no segmento

        min_peso = min(pesos)
        shift = -min_peso + 1 if min_peso < 0 else 0  # Ajuste para pesos não negativos

        for segmento in self.Segmentos.values():
            ci_id = segmento.cruzamento_inicial.ID
            cf_id = segmento.cruzamento_final.ID

            adjusted_peso = segmento.peso + shift

            self.PlantaPesos.setdefault(ci_id, []).append((cf_id, adjusted_peso, segmento))
            self.PlantaPesos.setdefault(cf_id, []).append((ci_id, adjusted_peso, segmento))

    def dijkstra(self, start):
        dist = {}
        prev = {}
        pq = [(0, start, None)]  # (distância acumulada, nó atual, segmento anterior)
        dist[start] = 0

        while pq:
            d, current, segment = heapq.heappop(pq)

            if d > dist.get(current, float('inf')):
                continue

            for neighbor, weight, seg in self.PlantaPesos.get(current, []):
                new_dist = d + weight
                if neighbor not in dist or new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    prev[neighbor] = (current, seg)
                    heapq.heappush(pq, (new_dist, neighbor, seg))

        return dist, prev


    def reconstruir_caminho(self, prev, end):
        caminho = []
        current = end
        while current in prev:
            previous, segment = prev[current]
            if segment:
                caminho.append(segment)
            current = previous
        return list(reversed(caminho))


    def calcular_menor_caminho_entre_regioes(self):
        regioes = list(self.Regioes.keys())
        caminhos_regioes = {}

        for i, regiao_i in enumerate(regioes):
            for regiao_j in regioes[i+1:]:
                menor_custo = float('inf')
                caminho_segmentos = []

                cruz_i_list = self.Regioes[regiao_i]
                cruz_j_list = self.Regioes[regiao_j]

                for cruz_i in cruz_i_list:
                    dist, prev = self.dijkstra(cruz_i)
                    for cruz_j in cruz_j_list:
                        if cruz_j in dist and dist[cruz_j] < menor_custo:
                            menor_custo = dist[cruz_j]
                            caminho_segmentos = self.reconstruir_caminho(prev, cruz_j)

                caminhos_regioes[(regiao_i, regiao_j)] = (menor_custo, caminho_segmentos)

        return caminhos_regioes


    def planejar_linha_onibus(self, start_cruzamento):
        self.construir_planta_tarefa2()
        unvisited_regions = set(self.Regioes.keys())
        current_cruzamento_id = start_cruzamento.ID
        current_region = start_cruzamento.cep
        unvisited_regions.remove(current_region)

        segments_in_route = set()
        path_segments = []

        while unvisited_regions:
            dist, prev = self.dijkstra(current_cruzamento_id) #O((V+E)logV)
            sorted_intersections = sorted(dist.items(), key=lambda x: x[1]) #O(vlogv)
            found = False
            for cruz_id, distance in sorted_intersections: #O(V)
                cruz_region = self.get_cruzamento_region(cruz_id)
                if cruz_region in unvisited_regions:
                    path = self.reconstruir_caminho(prev, cruz_id)
                    for segment in path:
                        if segment.ID_do_segmento not in segments_in_route:
                            segments_in_route.add(segment.ID_do_segmento)
                            path_segments.append(segment)
                    current_cruzamento_id = cruz_id
                    current_region = cruz_region
                    unvisited_regions.remove(current_region)
                    found = True
                    break
            if not found:
                break
        
        #Retornar pro ponto inicial
        dist, prev = self.dijkstra(current_cruzamento_id)
        path = self.reconstruir_caminho(prev, start_cruzamento.ID)
        for segment in path:
            if segment.ID_do_segmento not in segments_in_route:
                segments_in_route.add(segment.ID_do_segmento)
                path_segments.append(segment)

        return path_segments


    
    def planejar_metro(self):
        """
        algritmo de planejamento do metrô usando Prim MST.
        Retorna lista de segmentos que formam a árvore geradora minima.
        """
        if not self.Segmentos:
            print("Segmentos vazios!")
            return []
        primeiro_segmento = next(iter(self.Segmentos.values()))
        inicial = primeiro_segmento.cruzamento_inicial.ID
        
        visitados = set()
        mst = [] 
        heap = []  
        
        for segmento in self.Segmentos.values():
            if segmento.cruzamento_inicial.ID == inicial:
                heapq.heappush(heap, (segmento.custo_de_escavacao, segmento))
            elif segmento.cruzamento_final.ID == inicial:
                heapq.heappush(heap, (segmento.custo_de_escavacao, segmento))
        
        visitados.add(inicial)
        
        while heap:
            custo, segmento = heapq.heappop(heap)
            
            if segmento.cruzamento_inicial.ID not in visitados:
                proximo_cruzamento = segmento.cruzamento_inicial.ID
            elif segmento.cruzamento_final.ID not in visitados:
                proximo_cruzamento = segmento.cruzamento_final.ID
            else:
                continue  
            
            mst.append(segmento)
            visitados.add(proximo_cruzamento)
            
            for seg in self.Segmentos.values():
                if (seg.cruzamento_inicial.ID == proximo_cruzamento and 
                    seg.cruzamento_final.ID not in visitados):
                    heapq.heappush(heap, (seg.custo_de_escavacao, seg))
                elif (seg.cruzamento_final.ID == proximo_cruzamento and 
                    seg.cruzamento_inicial.ID not in visitados):
                    heapq.heappush(heap, (seg.custo_de_escavacao, seg))
        
        return mst


def factor_k(k):
    for i in range(int(math.sqrt(k)), 0, -1):
        if k % i == 0:
            return i, k // i
    return 1, k

def generate_city(x, y, k):
    # Criar cruzamentos
    crossings = {}  # key: (i, j), value: Cruzamento object
    cruzamento_id = 0
    crossings_positions = {}  # key: cruzamento_id, value: (i, j)

    # Determinar nx e ny para dividir o grid em regiões
    nx, ny = factor_k(k)

    regions = {}  # key: region_id, value: set of cruzamento IDs

    for i in range(x):
        for j in range(y):
            # Determinar o ID da região
            region_x = i * nx // x
            region_y = j * ny // y
            region_id = region_x + region_y * nx

            # Atribuir o CEP como 'Regiao' + str(region_id)
            cep = f'Regiao{region_id}'

            cruzamento = Cruzamento(ID=cruzamento_id, cep=cep)
            crossings[(i, j)] = cruzamento
            crossings_positions[cruzamento_id] = (i, j)

            # Adicionar o ID do cruzamento à região correspondente
            if region_id not in regions:
                regions[region_id] = set()
            regions[region_id].add(cruzamento_id)

            cruzamento_id += 1

    # Criar segmentos conectando cruzamentos adjacentes
    segmentos = []
    segmento_id = 0
    for i in range(x):
        for j in range(y):
            cruzamento = crossings[(i, j)]
            # Conectar ao vizinho da direita
            if i < x - 1:
                neighbor_cruzamento = crossings[(i + 1, j)]
                distancia = 1.0  # Pode ser ajustada conforme necessário
                custo_de_escavacao = random.uniform(1000, 5000)
                segmento = Segmento(segmento_id, distancia, custo_de_escavacao, cruzamento, neighbor_cruzamento)
                segmentos.append(segmento)
                segmento_id += 1
            # Conectar ao vizinho de baixo
            if j < y - 1:
                neighbor_cruzamento = crossings[(i, j + 1)]
                distancia = 1.0  # Pode ser ajustada conforme necessário
                custo_de_escavacao = random.uniform(1000, 5000)
                segmento = Segmento(segmento_id, distancia, custo_de_escavacao, cruzamento, neighbor_cruzamento)
                segmentos.append(segmento)
                segmento_id += 1

    # Criar imóveis e atribuí-los aos segmentos
    tipos_imovel = ['R', 'C', 'I', 'T']
    imovel_id = 0
    for segmento in segmentos:
        num_imoveis = random.randint(0, 3)  # Número aleatório de imóveis neste segmento
        numero = 1
        for _ in range(num_imoveis):
            tipo = random.choice(tipos_imovel)
            cep = segmento.cruzamento_inicial.cep  # Usar o CEP do cruzamento inicial
            rua = f"Rua {segmento.ID_do_segmento}"  # associar a rua ao ID do segmento
            imovel = Imovel(imovel_id, cep, tipo, rua, numero)
            segmento.adicionar_imovel(imovel)
            imovel_id += 1
            numero += 1 

    # Criar a cidade e adicionar os segmentos
    cidade = Cidade()
    for segmento in segmentos:
        cidade.adicionar_segmento(segmento)

    return cidade



#### Implementando algoritmo de calcular distâncias ####

'''
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

def encontrar_centro_por_regiao(subgrafos_regioes):
    centros = {}
    for regiao, subgrafo in subgrafos_regioes.items():
        melhor_cruzamento = None
        menor_distancia_maxima = inf
        
        for cruzamento in subgrafo:
            distancias = calcular_distancias(subgrafo, cruzamento)
            distancia_maxima = max(distancias.values())  # Pior caso para esse cruzamento
            
            if distancia_maxima < menor_distancia_maxima:
                menor_distancia_maxima = distancia_maxima
                melhor_cruzamento = cruzamento
        
        centros[regiao] = (melhor_cruzamento, menor_distancia_maxima)
    
    return centros

'''