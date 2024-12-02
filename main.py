import heapq
from math import inf
from collections import defaultdict

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
        

    def adicionar_segmento(self, segmento):
        self.Segmentos[segmento.ID_do_segmento] = segmento
        for cruzamento in [segmento.cruzamento_inicial, segmento.cruzamento_final]:
            regiao_id = cruzamento.cep
            if regiao_id not in self.Regioes:
                self.Regioes[regiao_id] = set()
            self.Regioes[regiao_id].add(cruzamento.ID)

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

    def calcular_menor_caminho_entre_regioes(self, start_cruzamento):
        regioes = list(self.Regioes.keys())
        caminhos_regioes = {}

        for regiao_i in regioes:
            for regiao_j in regioes:
                if regiao_i == regiao_j:
                    continue

                menor_custo = float('inf')
                caminho_segmentos = []

                if regiao_i == self.regiao_inicial:
                    cruz_i_list = [start_cruzamento.ID]
                else:
                    cruz_i_list = self.Regioes[regiao_i]

                if regiao_j == self.regiao_inicial:
                    cruz_j_list = [start_cruzamento.ID]
                else:
                    cruz_j_list = self.Regioes[regiao_j]

                for cruz_i in cruz_i_list:
                    dist, prev = self.dijkstra(cruz_i)
                    for cruz_j in cruz_j_list:
                        if cruz_j in dist and dist[cruz_j] < menor_custo:
                            menor_custo = dist[cruz_j]
                            caminho_segmentos = self.reconstruir_caminho(prev, cruz_j)

                caminhos_regioes[(regiao_i, regiao_j)] = (menor_custo, caminho_segmentos)

        return caminhos_regioes


    def tsp(self, regioes, caminhos_regioes):
        n = len(regioes)
        memo = {}

        def tsp_rec(mask, pos):
            if mask == (1 << n) - 1:  # Todos visitados
                if (regioes[pos], regioes[0]) in caminhos_regioes:
                    return_custo, return_caminho = caminhos_regioes[(regioes[pos], regioes[0])]
                    return return_caminho, return_custo
                else:
                    return [], float('inf')

            if (mask, pos) in memo:
                return memo[(mask, pos)]

            min_caminho = []
            min_custo = float('inf')
            for next_region in range(n):
                if mask & (1 << next_region) == 0:
                    if (regioes[pos], regioes[next_region]) in caminhos_regioes:
                        edge_custo, edge_caminho = caminhos_regioes[(regioes[pos], regioes[next_region])]
                        caminho, custo = tsp_rec(mask | (1 << next_region), next_region)
                        total_custo = edge_custo + custo
                        total_caminho = edge_caminho + caminho

                        if total_custo < min_custo:
                            min_custo = total_custo
                            min_caminho = total_caminho

            memo[(mask, pos)] = (min_caminho, min_custo)
            return memo[(mask, pos)]

        caminho_final, _ = tsp_rec(1, 0)
        return caminho_final

    def planejar_linha_onibus(self, start_cruzamento):
        self.construir_planta_tarefa2()

        '''
        regiao_inicial = None
        for regiao, cruzamentos in self.Regioes.items():
            if start_cruzamento in cruzamentos:
                regiao_inicial = regiao
                break
        '''
        regiao_inicial = start_cruzamento.cep 
        self.regiao_inicial = regiao_inicial

        regioes = list(self.Regioes.keys())

        if regiao_inicial is not None:
            regioes.remove(regiao_inicial)
            regioes = [regiao_inicial] + regioes

        caminhos_regioes = self.calcular_menor_caminho_entre_regioes(start_cruzamento)

        linha_onibus = self.tsp(regioes, caminhos_regioes)
        return linha_onibus
    
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