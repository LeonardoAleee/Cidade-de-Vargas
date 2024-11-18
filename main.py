import heapq
from math import inf

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
        for segmento in self.Segmentos.values():
            ci_id = segmento.cruzamento_inicial.ID
            cf_id = segmento.cruzamento_final.ID

            # Calcular o peso com base nos tipos de imóveis (podemos alterar isso)
            peso = (
                -2 * segmento.quantidade_comercial -
                2 * segmento.quantidade_turistico +
                1 * segmento.quantidade_residencial +
                1 * segmento.quantidade_industrial
            )

            # Criar aresta dupla (grafo não direcionado) com pesos customizados
            self.PlantaPesos.setdefault(ci_id, []).append((cf_id, peso, segmento))
            self.PlantaPesos.setdefault(cf_id, []).append((ci_id, peso, segmento))

    def planejar_linha_onibus(self):
        self.construir_planta_tarefa2()

        pontos_por_regiao = {regiao: list(cruzamentos)[0] for regiao, cruzamentos in self.Regioes.items()}
        pontos_iniciais = list(pontos_por_regiao.values())
        rota_final = self.encontrar_rota_otimizada(pontos_iniciais)

        if not rota_final:
            print("Não foi possível encontrar um ciclo ideal.")
            return [], []

        segmentos_onibus = []

        for segmento in rota_final:
            segmentos_onibus.append(segmento.ID_do_segmento)

        return pontos_iniciais, segmentos_onibus

    def encontrar_rota_otimizada(self, pontos_iniciais):
        visitados = set()
        heap = [(0, pontos_iniciais[0], [], None)]
        melhor_rota = None
        menor_custo = float('inf')

        while heap:
            custo, atual, caminho, segmento_anterior = heapq.heappop(heap)

            # Verifica se cobrimos todas as regiões e formamos um ciclo
            if len(set(caminho)) >= len(self.Regioes) and caminho and caminho[0].cruzamento_inicial.ID == atual:
                if custo < menor_custo:
                    menor_custo = custo
                    melhor_rota = caminho
                continue

            if atual in visitados and segmento_anterior:
                continue
            visitados.add(atual)

            for adjacente, peso, segmento in self.PlantaPesos.get(atual, []):
                if segmento != segmento_anterior:
                    novo_caminho = caminho + [segmento]
                    heapq.heappush(heap, (custo + peso, adjacente, novo_caminho, segmento))

        return melhor_rota


#### Implementando algoritmo de calcular distâncias ####


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

