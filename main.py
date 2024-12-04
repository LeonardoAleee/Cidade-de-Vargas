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
        self.PlantaCustosEscavacao = {}
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

    def construir_planta_tarefa1(self):
        self.PlantaCustosEscavacao = {}  # Alterado de PlantaPesos para PlantaCustosEscavacao
        custos_escavacao = []
        
        for segmento in self.Segmentos.values():
            ci_id = segmento.cruzamento_inicial.ID
            cf_id = segmento.cruzamento_final.ID

            # Calcular o custo de escavação com base nos tipos de imóveis adjacentes
            custo_escavacao = (
                3.0 * segmento.quantidade_comercial -  # Ajuste de custo para área comercial
                5.0 * segmento.quantidade_turistico +  # Ajuste de custo para área turística
                1.0 * segmento.quantidade_residencial +  # Ajuste de custo para área residencial
                2.0 * segmento.quantidade_industrial  # Ajuste de custo para área industrial
            )
            custos_escavacao.append(custo_escavacao)
            segmento.custo_escavacao = custo_escavacao  # Armazena o custo de escavação no segmento

        min_custo = min(custos_escavacao)
        shift = -min_custo + 1 if min_custo < 0 else 0  # Ajuste para custos não negativos

        for segmento in self.Segmentos.values():
            ci_id = segmento.cruzamento_inicial.ID
            cf_id = segmento.cruzamento_final.ID

            adjusted_custo = segmento.custo_escavacao + shift

            # Armazenar os custos de escavação ajustados no dicionário PlantaCustosEscavacao
            self.PlantaCustosEscavacao.setdefault(ci_id, []).append((cf_id, adjusted_custo, segmento))
            self.PlantaCustosEscavacao.setdefault(cf_id, []).append((ci_id, adjusted_custo, segmento))

    def dijkstra_custo_escavacao(self, start):
        """
        Calcula o menor custo de escavação de um cruzamento de partida para todos os outros cruzamentos
        usando o algoritmo de Dijkstra.
        """
        # Dicionários para armazenar os custos e os caminhos anteriores
        custo_escavacao = {}
        prev = {}
        pq = [(0, start, None)]  # (custo acumulado, nó atual, segmento anterior)
        custo_escavacao[start] = 0

        while pq:
            custo, current, segmento = heapq.heappop(pq)

            # Se o custo encontrado for maior que o mínimo registrado, continue
            if custo > custo_escavacao.get(current, float('inf')):
                continue

            # Percorrer os vizinhos e calcular os custos de escavação
            for neighbor, custo_vizinho, seg in self.PlantaCustosEscavacao.get(current, []):
                novo_custo = custo + custo_vizinho  # Acumula o custo de escavação
                if neighbor not in custo_escavacao or novo_custo < custo_escavacao[neighbor]:
                    custo_escavacao[neighbor] = novo_custo
                    prev[neighbor] = (current, seg)
                    heapq.heappush(pq, (novo_custo, neighbor, seg))

        return custo_escavacao, prev

    def definir_estacoes(self):
        """
        Define as estações de metrô para cada região com base na distância mínima do ponto mais longe.
        """
        self.estacoes = {}  # Dicionário: região -> ID do cruzamento da estação

        for regiao_id, cruzamentos in self.Regioes.items():
            menor_max_distancia = float('inf')
            melhor_cruzamento = None

            for cruzamento_id in cruzamentos:
                # Dijkstra para calcular as distâncias de cruzamento_id a todos os outros cruzamentos da região
                distancias, _ = self.dijkstra(cruzamento_id)

                # Considera apenas os cruzamentos dentro da região atual
                max_distancia = max(
                    distancias[c] for c in cruzamentos if c in distancias
                )

                # Atualiza o cruzamento se encontrar uma melhor opção
                if max_distancia < menor_max_distancia:
                    menor_max_distancia = max_distancia
                    melhor_cruzamento = cruzamento_id

            self.estacoes[regiao_id] = melhor_cruzamento
    
    def is_station(self, cruzamento_id):
        return cruzamento_id in self.estacoes
    
    def conectar_estacoes_com_kruskal(self):
        """
        Conecta as estações de metrô utilizando o algoritmo de Kruskal para encontrar a árvore geradora mínima.
        Considera o menor custo entre estações, mesmo que exija múltiplos segmentos.
        """
        # Lista de estações
        estacoes_ids = list(self.estacoes.values())

        # Calcula as menores distâncias entre todas as estações usando Dijkstra
        menores_distancias = {}
        for estacao in estacoes_ids:
            distancias, _ = self.dijkstra_custo_escavacao(estacao)
            menores_distancias[estacao] = distancias

        # Lista de arestas no formato (custo, estação_a, estação_b)
        arestas = []
        for i, est_a in enumerate(estacoes_ids):
            for est_b in estacoes_ids[i+1:]:
                if est_b in menores_distancias[est_a]:
                    custo = menores_distancias[est_a][est_b]
                    arestas.append((custo, est_a, est_b))

        # Ordena as arestas pelo custo
        arestas.sort()

        # Estruturas auxiliares para o algoritmo de Kruskal
        parent = {}
        rank = {}

        def find(node):
            if parent[node] != node:
                parent[node] = find(parent[node])
            return parent[node]

        def union(node1, node2):
            root1 = find(node1)
            root2 = find(node2)

            if root1 != root2:
                if rank[root1] > rank[root2]:
                    parent[root2] = root1
                elif rank[root1] < rank[root2]:
                    parent[root1] = root2
                else:
                    parent[root2] = root1
                    rank[root1] += 1

        # Inicializa os conjuntos disjuntos
        for cruz in estacoes_ids:
            parent[cruz] = cruz
            rank[cruz] = 0

        # Árvore geradora mínima resultante
        mst = []

        for custo, cruz_a, cruz_b in arestas:
            if find(cruz_a) != find(cruz_b):
                union(cruz_a, cruz_b)
                mst.append((custo, cruz_a, cruz_b))

        return mst

    def planejar_metro(self):
        """
        Planeja as linhas de metrô da cidade.
        """
        # Passo 1: Definir as estações para cada região
        self.definir_estacoes()

        # Passo 2: Conectar as estações usando Kruskal
        mst = self.conectar_estacoes_com_kruskal()

        return mst
    
    def encontrar_segmento_por_imovel(self, imovel):
        # Obter cruzamentos da região pelo CEP do imóvel
        cruzamentos_da_regiao = self.Regioes.get(imovel.cep, set())

        # Iterar apenas pelos segmentos que conectam cruzamentos da região
        for segmento in self.Segmentos.values():
            if (segmento.cruzamento_inicial.ID in cruzamentos_da_regiao or 
                segmento.cruzamento_final.ID in cruzamentos_da_regiao):
                if imovel.ID in segmento.conjunto_de_imoveis:
                    return segmento

        return None

    def mapear_imoveis_para_segmentos(self):
        imovel_para_segmento = {}

        for segmento in self.Segmentos.values(): # for segmento in lista_de_segmentos
            for imovel_id, imovel in segmento.conjunto_de_imoveis.items(): 
                imovel_para_segmento[imovel] = segmento

        return imovel_para_segmento

    def cruzamento_mais_proximo(self, imovel):
        segmento = self.encontrar_segmento_por_imovel(imovel)
        if not segmento:
            return None  # Retorna None se o imóvel não estiver associado a um segmento

        distancia_inicial = self.calcular_distancia(imovel, segmento.cruzamento_inicial)
        distancia_final = self.calcular_distancia(imovel, segmento.cruzamento_final)

        if distancia_inicial <= distancia_final:
            return segmento.cruzamento_inicial
        else:
            return segmento.cruzamento_final

    def calcular_distancia(self, imovel, cruzamento):
        return abs(imovel.ID - cruzamento.ID)

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

def a_star_com_restricao_custo(self, origem, destino, custo_maximo):
    """
    Implementa o algoritmo A* com restrição de custo para encontrar o caminho mais rápido
    entre dois cruzamentos, respeitando o limite de custo.
    
    :param origem: ID do cruzamento de origem.
    :param destino: ID do cruzamento de destino.
    :param custo_maximo: Custo máximo permitido.
    :param horario_embarque: Horário de embarque do usuário em minutos (ex: 505 para 8:05 AM).
    :param tempo_transferencia: Tempo necessário para troca de transporte, em minutos.
    :return: Rota como lista de arestas e meios de transporte, ou None se não houver rota viável.
    """
    # Fila de prioridade com (custo total, cruzamento atual, caminho percorrido)
    pq = [(0, origem, [])]  # (custo acumulado, cruzamento atual, caminho)
    visitados = {}  # dicionário para armazenar o custo mínimo encontrado para cada cruzamento

    while pq:
        custo_atual, cruzamento_atual, caminho = heapq.heappop(pq)

        # Se o custo atual exceder o limite de custo, ignore essa rota
        if custo_atual > custo_maximo:
            continue

        # Se já visitamos o cruzamento com custo menor, ignoramos
        if cruzamento_atual in visitados and visitados[cruzamento_atual] <= custo_atual:
            continue

        # Marcar o cruzamento como visitado
        visitados[cruzamento_atual] = custo_atual

        # Se chegamos ao destino, retorna o caminho
        if cruzamento_atual == destino:
            return caminho

        # Expande os vizinhos
        for aresta in self.PlantaPesos.get(cruzamento_atual, []):
            for meio, dados in aresta.meios_transporte.items():
                # Calcula o tempo de espera para o transporte (método ou ônibus)
                tempo_espera = 0
                if meio in aresta.horarios:
                    tempo_espera, proximo_horario = self.calcular_espera(horario_embarque, aresta.horarios[meio])
                    if tempo_espera is None:
                        continue  # Se não há horários disponíveis, ignora essa aresta

                # Calcula o custo e tempo da viagem para esse meio de transporte
                novo_custo = custo_atual + dados["custo"]
                novo_tempo = dados["tempo"] + tempo_espera

                # Adiciona tempo de transferência se houver mudança de transporte
                if caminho and caminho[-1][1] != meio:
                    tempo_transferencia, _ = self.calcular_espera(horario_embarque, aresta.horarios[meio])
                    novo_tempo += tempo_transferencia  # Adiciona o tempo de transferência calculado

                # Se o custo acumulado é menor que o custo máximo, adiciona a fila
                if novo_custo <= custo_maximo:
                    novo_caminho = caminho + [(aresta, meio, tempo_espera)]
                    heapq.heappush(pq, (novo_tempo, aresta.destino, novo_caminho))

    return None  # Caso não haja caminho viável

def calcular_espera(self, horario_embarque, horarios_transporte):
    """
    Calcula o tempo de espera até o próximo horário de transporte disponível.
    
    :param horario_embarque: Horário de embarque do usuário em minutos desde meia-noite.
    :param horarios_transporte: Lista de horários de chegada do transporte (ex: metrô ou ônibus).
    
    :return: Tempo de espera até o próximo transporte, em minutos, ou None se não houver horários disponíveis.
    """
    # Encontra o próximo horário de chegada disponível para o transporte
    proximo_horario = min(
        (h for h in horarios_transporte if h >= horario_embarque),
        default=float('inf')  # Se não houver horários futuros, retorna infinito
    )
    
    if proximo_horario == float('inf'):
        return None  # Se não há horários disponíveis, retorna None

    # Calcula o tempo de espera até o próximo horário disponível
    tempo_espera = proximo_horario - horario_embarque
    return tempo_espera, proximo_horario


class Aresta:
    def __init__(self, Origem_ID, Destino_ID):
        self.origem = Origem_ID
        self.destino = Destino_ID
        self.meios_de_transporte = {
            "metro": None,
            "onibus": None,
            "taxi": None,
            "Andar": None
        }
        self.tempos_transferencia = {}  # Novo: tempos de transferência entre modos

    def adicionar_transporte(self, meio, tempo, custo):
        if meio in self.meios_de_transporte and meio != "metro":
            self.meios_de_transporte[meio] = {"tempo": tempo, "custo": custo, "acessivel": True}
        
        if meio == "metro":
            self.meios_de_transporte[meio] = {"tempo": tempo, "custo": custo, 
                                              "acessivel": Cidade.is_station(self.origem)}

    def adicionar_tempo_transferencia(self, de_meio, para_meio, tempo):
        if de_meio not in self.tempos_transferencia:
            self.tempos_transferencia[de_meio] = {}
        self.tempos_transferencia[de_meio][para_meio] = tempo
           
class Mapa:
    def __init__(self, cidade):
        """
        Inicializa o Mapa com base na cidade fornecida.
        
        :param cidade: Instância da classe Cidade, que contém os segmentos e cruzamentos.
        """
        self.cidade = cidade
        self.grafo = defaultdict(list)  # Representação do grafo multimodal como lista de adjacência

    def construir_grafo(self):
        """
        Constrói o grafo multimodal da cidade.
        """
        for segmento in self.cidade.Segmentos.values():
            cruz_inicial = segmento.cruzamento_inicial.ID
            cruz_final = segmento.cruzamento_final.ID

            meios_de_transporte = self.inicializar_meios_transporte(segmento)

            for meio, dados in meios_de_transporte.items():
                tempo = dados['tempo']
                custo = dados['custo']

                aresta_ida = Aresta(cruz_inicial, cruz_final)
                aresta_ida.adicionar_transporte(meio, tempo, custo)

                aresta_volta = Aresta(cruz_final, cruz_inicial)
                aresta_volta.adicionar_transporte(meio, tempo, custo)

                self.grafo[cruz_inicial].append(aresta_ida)
                self.grafo[cruz_final].append(aresta_volta)


    def obter_rota(self, endereco_origem, endereco_destino, custo_maximo):
        """
        Encontra a rota mais rápida entre dois endereços, respeitando um custo máximo.
        
        :param endereco_origem: Endereço de origem (ou ID do cruzamento).
        :param endereco_destino: Endereço de destino (ou ID do cruzamento).
        :param custo_maximo: Custo máximo permitido para a rota.
        :return: Detalhes da rota ou uma mensagem de erro.
        """
        # Identificar os cruzamentos correspondentes aos endereços
        cruzamento_origem = self._encontrar_cruzamento_por_endereco(endereco_origem)
        cruzamento_destino = self._encontrar_cruzamento_por_endereco(endereco_destino)

        if not cruzamento_origem or not cruzamento_destino:
            return f"Endereço inválido: {'origem' if not cruzamento_origem else 'destino'} não encontrado."

        # Buscar a rota mais curta com restrição de custo
        rota = self.caminho_mais_curto_com_restricao(cruzamento_origem, cruzamento_destino, custo_maximo)
        
        if not rota:
            return f"Nenhuma rota viável encontrada dentro do custo máximo de {custo_maximo}."

        # Formatar os detalhes da rota
        detalhes_rota = []
        for aresta, meio in rota:
            detalhes_rota.append(f"Cruzamento {aresta.origem} -> {aresta.destino} via {meio}")

        return "\n".join(detalhes_rota)

    def _encontrar_cruzamento_por_endereco(self, endereco):
        """
        Encontra o ID do cruzamento associado a um endereço.
        :param endereco: Endereço fornecido pelo usuário (CEP ou outro identificador).
        :return: ID do cruzamento correspondente.
        """
        # Caso o endereço já seja um ID de cruzamento
        if isinstance(endereco, int) and endereco in self.cidade.Cruzamentos:
            return endereco

        # Procurar pelo endereço no conjunto de imóveis
        for segmento in self.cidade.Segmentos.values():
            for imovel in segmento.conjunto_de_imoveis.values():
                if imovel.rua == endereco or imovel.cep == endereco:
                    return self.cidade.cruzamento_mais_proximo(imovel).ID

        return None
    
    def inicializar_meios_transporte(self, segmento):
        """
        Inicializa os meios de transporte disponíveis para um segmento.
        
        :param segmento: Instância do objeto Segmento.
        :return: Um dicionário contendo os meios de transporte e seus dados (tempo e custo).
        """
        meios_de_transporte = {}

        # Definições de transporte: ajustar conforme necessário
        velocidade_andar = 5  # km/h
        velocidade_onibus = 40  # km/h
        velocidade_taxi = 60  # km/h
        custo_onibus = 2.50  # custo fixo
        custo_taxi_por_km = 3.50  # custo por km

        # Cálculo para "andar"
        tempo_andar = segmento.distancia / (velocidade_andar / 60)  # em minutos
        meios_de_transporte["Andar"] = {"tempo": tempo_andar, "custo": 0}

        # Cálculo para "ônibus"
        tempo_onibus = segmento.distancia / (velocidade_onibus / 60)  # em minutos
        meios_de_transporte["onibus"] = {"tempo": tempo_onibus, "custo": custo_onibus}

        # Cálculo para "táxi"
        tempo_taxi = segmento.distancia / (velocidade_taxi / 60)  # em minutos
        custo_taxi = segmento.distancia * custo_taxi_por_km
        meios_de_transporte["taxi"] = {"tempo": tempo_taxi, "custo": custo_taxi}

        # Opcional: adicionar "metrô" se o segmento conecta estações
        if segmento.cruzamento_inicial.ID in self.cidade.estacoes and segmento.cruzamento_final.ID in self.cidade.estacoes:
            meios_de_transporte["metro"] = {"tempo": tempo_onibus, "custo": 1.50}  # Exemplo de custo fixo

        return meios_de_transporte

    def caminho_mais_curto_com_restricao(self, origem_id, destino_id, custo_maximo):
        pq = []
        counter = 0
        heapq.heappush(pq, (0, 0, counter, origem_id, None, []))  # Adiciona `None` para o meio anterior
        visitados = {}

        while pq:
            tempo_atual, custo_atual, _, cruzamento_atual, meio_anterior, caminho = heapq.heappop(pq)

            if custo_atual > custo_maximo:
                continue

            if cruzamento_atual in visitados and visitados[cruzamento_atual] <= custo_atual:
                continue

            visitados[cruzamento_atual] = custo_atual

            if cruzamento_atual == destino_id:
                return caminho

            for aresta in self.grafo.get(cruzamento_atual, []):
                for meio, dados in aresta.meios_de_transporte.items():
                    if dados is None:
                        continue

                    novo_tempo = tempo_atual + dados["tempo"]
                    novo_custo = custo_atual + dados["custo"]

                    # Adicionar tempo de transferência se necessário
                    if meio_anterior and meio_anterior != meio:
                        transferencia = aresta.tempos_transferencia.get(meio_anterior, {}).get(meio, 0)
                        novo_tempo += transferencia

                    if novo_custo <= custo_maximo:
                        novo_caminho = caminho + [(aresta, meio)]
                        counter += 1
                        heapq.heappush(pq, (novo_tempo, novo_custo, counter, aresta.destino, meio, novo_caminho))

        return None

    
    #def heuristica(self, cruzamento_atual, cruzamento_destino):
    #    pos_atual = self.cidade.Cruzamentos[cruzamento_atual].posicao  # Posição (x, y)
    #    pos_destino = self.cidade.Cruzamentos[cruzamento_destino].posicao
    #    return math.sqrt((pos_atual[0] - pos_destino[0])**2 + (pos_atual[1] - pos_destino[1])**2)


    def atualizar_condicoes_transito(self, fator_taxi, fator_onibus):
        """
        Atualiza as velocidades dos meios de transporte afetados pelo trânsito.
        
        :param fator_taxi: Fator de ajuste para a velocidade do táxi (ex.: 0.5 para reduzir pela metade).
        :param fator_onibus: Fator de ajuste para a velocidade do ônibus.
        """
        for cruzamento_id, arestas in self.grafo.items():
            for aresta in arestas:
                for meio, dados in aresta.meios_de_transporte.items():
                    if dados is None:
                        continue
                    
                    # Ajustar velocidade para táxi e ônibus
                    if meio == "taxi":
                        dados["tempo"] /= fator_taxi  # Reduzir ou aumentar tempo de viagem
                    elif meio == "onibus":
                        dados["tempo"] /= fator_onibus    

    def atualizar_condicoes_transito_randomico(self):
        """
        Atualiza as velocidades dos meios de transporte afetados pelo trânsito.
        
        :param fator_taxi: Fator de ajuste para a velocidade do táxi (ex.: 0.5 para reduzir pela metade).
        :param fator_onibus: Fator de ajuste para a velocidade do ônibus.
        """
        for cruzamento_id, arestas in self.grafo.items():
            for aresta in arestas:
                for meio, dados in aresta.meios_de_transporte.items():
                    if dados is None:
                        continue
                    
                    # Ajustar velocidade para táxi e ônibus
                    if meio == "taxi":
                        dados["tempo"] /= random.random()  # Reduzir ou aumentar tempo de viagem
                    elif meio == "onibus":
                        dados["tempo"] /= random.random()
    


def buscar_rota(map, origem_id, destino_id, custo_maximo):
    """
    Envolve o algoritmo A* com restrição para facilitar o uso.
    
    :param map: Instância da classe Mapa.
    :param origem_id: ID do cruzamento de origem.
    :param destino_id: ID do cruzamento de destino.
    :param custo_maximo: Custo máximo permitido.
    :return: Rota como lista de arestas e meios de transporte, ou mensagem de erro.
    """
    rota = map.caminho_mais_curto_com_restricao(origem_id, destino_id, custo_maximo)
    if rota:
        print("Rota encontrada:")
        for aresta, meio in rota:
            print(f"Cruzamento {aresta.origem} -> {aresta.destino} via {meio}")
        return rota
    else:
        print("Nenhum caminho viável encontrado dentro do custo máximo.")
        return None
