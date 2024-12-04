from main import *
import random
import time
import matplotlib.pyplot as plt

class TesteRotas:
    def __init__(self, mapa):
        self.mapa = mapa

    def realizar_teste(self, num_testes=100, max_custo=1000):
        """
        Realiza múltiplos testes de busca de rotas entre cruzamentos aleatórios.

        :param num_testes: Número de testes a serem realizados.
        :param max_custo: Custo máximo para as rotas.
        :return: Estatísticas sobre os testes realizados.
        """
        cruzamentos = list(self.mapa.cidade.Cruzamentos.keys())
        resultados = {
            "sucesso": 0,
            "fracasso": 0,
            "tempos": [],
            "custos": []
        }

        for _ in range(num_testes):
            # Selecionar cruzamentos de origem e destino aleatórios
            origem = random.choice(cruzamentos)
            destino = random.choice(cruzamentos)

            # Garantir que origem e destino sejam diferentes
            while destino == origem:
                destino = random.choice(cruzamentos)

            custo_maximo = random.randint(max_custo // 2, max_custo)

            inicio_tempo = time.time()
            rota = self.mapa.caminho_mais_curto_com_restricao(origem, destino, custo_maximo)
            fim_tempo = time.time()

            if rota:
                resultados["sucesso"] += 1
                # Calcular o custo da rota
                custo_total = sum(
                    aresta.meios_de_transporte[meio]["custo"]
                    for aresta, meio in rota
                )
                resultados["custos"].append(custo_total)
            else:
                resultados["fracasso"] += 1

            resultados["tempos"].append(fim_tempo - inicio_tempo)

        return self.gerar_estatisticas(resultados)

    def gerar_estatisticas(self, resultados):
        """
        Gera estatísticas com base nos resultados dos testes.

        :param resultados: Dicionário com os resultados dos testes.
        :return: Estatísticas formatadas.
        """
        total_testes = resultados["sucesso"] + resultados["fracasso"]
        percentual_sucesso = (resultados["sucesso"] / total_testes) * 100

        estatisticas = {
            "Total de Testes": total_testes,
            "Sucessos": resultados["sucesso"],
            "Fracassos": resultados["fracasso"],
            "Percentual de Sucesso": percentual_sucesso,
            "Tempo Médio (s)": sum(resultados["tempos"]) / total_testes,
            "Custo Médio (Rotas bem-sucedidas)": sum(resultados["custos"]) / len(resultados["custos"]) if resultados["custos"] else None
        }

        return estatisticas

def testar_tempo_busca_rota():
    """
    Testa o tempo necessário para buscar rotas em cidades de tamanhos variados.
    """
    import math
    tamanhos = [10, 20, 30, 50, 75, 100, 200, 300, 500, 750, 1000,2000, 5000, 7500, 10000]
    k = 5  # Número de regiões
    custo_maximo = 1000
    resultados = []
    tempos = []

    for N in tamanhos:
        print(f"\nTestando para N = {N} cruzamentos...")
        # Calcular dimensões x e y para ter aproximadamente N cruzamentos (x * y = N)
        x = int(math.sqrt(N))
        y = N // x
        print(f"Dimensões da grade: x = {x}, y = {y}")

        # Gera a cidade
        cidade = generate_city(x, y, k)

        # Configurações iniciais
        cidade.definir_estacoes()
        cidade.planejar_metro()

        mapa = Mapa(cidade)
        mapa.construir_grafo()

        cruzamentos = list(cidade.Cruzamentos.keys())
        origem = cruzamentos[0]  # Primeiro cruzamento
        destino = cruzamentos[-1]  # Último cruzamento

        start_time = time.time()
        try:
            rota = mapa.caminho_mais_curto_com_restricao(origem, destino, custo_maximo)
            end_time = time.time()
            tempo_execucao = end_time - start_time

            if rota:
                print(f"Rota encontrada com sucesso para N = {N}.")
                resultados.append(N)
                tempos.append(tempo_execucao)
                print(f"Tempo de execução para N = {N}: {tempo_execucao:.4f} segundos")
            else:
                print(f"Nenhuma rota encontrada para N = {N}.")
                resultados.append(N)
                tempos.append(None)

        except Exception as e:
            print(f"Erro ao processar N = {N}: {e}")
            resultados.append(N)
            tempos.append(None)
            continue

    print("\nResultados:")
    for N, tempo in zip(resultados, tempos):
        if tempo is not None:
            print(f"N = {N} cruzamentos: {tempo:.4f} segundos")
        else:
            print(f"N = {N} cruzamentos: Não foi possível calcular")

    # Plotar os resultados
    tamanhos_validos = [N for N, tempo in zip(resultados, tempos) if tempo is not None]
    tempos_validos = [tempo for tempo in tempos if tempo is not None]

    plt.figure(figsize=(10, 6))
    plt.plot(tamanhos_validos, tempos_validos, marker='o')
    plt.xlabel('Número de Cruzamentos (N)')
    plt.ylabel('Tempo de Execução (s)')
    plt.title('Tempo de Execução da Busca de Rotas em Função do Tamanho da Cidade')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # Gera uma cidade de exemplo
    cidade = generate_city(10, 10, 4)  # Grid 10x10 com 4 regiões

    # Configura as rotas de ônibus e metrô
    cidade.definir_estacoes()
    cidade.planejar_metro()

    mapa = Mapa(cidade)
    mapa.construir_grafo()

    # Realiza os testes
    tester = TesteRotas(mapa)
    estatisticas = tester.realizar_teste(num_testes=100, max_custo=500)

    # Exibe as estatísticas
    print("Estatísticas dos Testes de Rotas:")
    for chave, valor in estatisticas.items():
        print(f"{chave}: {valor}")

    # Testa o tempo de busca de rotas
    testar_tempo_busca_rota()
