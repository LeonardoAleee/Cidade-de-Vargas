from main import *
import time
import math

def testar_tempo_planejamento_metro():
    """
    Testa o desempenho da função planejar_metro para diferentes tamanhos de cidades.
    """
    tamanhos = [10, 100, 1000, 10000, 100000]  # Números de cruzamentos
    k = 5  # Número de conexões por cruzamento
    resultados = []

    for N in tamanhos:
        print(f"\nTestando para N = {N} cruzamentos...")
        # Calcular dimensões x e y para ter aproximadamente N cruzamentos (x * y = N)
        x = int(math.sqrt(N))
        y = N // x
        print(f"Dimensões da grade: x = {x}, y = {y}")
        
        # Gerar a cidade com x por y cruzamentos e k conexões
        cidade = generate_city(x, y, k)

        start_time = time.time()
        try:
            # Testar a função de planejamento da linha de metrô
            mst = cidade.planejar_metro()
            end_time = time.time()
            tempo_execucao = end_time - start_time
            resultados.append((N, tempo_execucao))
            print(f"Tempo de execução para N = {N}: {tempo_execucao:.4f} segundos")
        except Exception as e:
            print(f"Erro ao processar N = {N}: {e}")
            resultados.append((N, None))
            continue

    print("\nResultados:")
    for N, tempo in resultados:
        if tempo is not None:
            print(f"N = {N} cruzamentos: {tempo:.4f} segundos")
        else:
            print(f"N = {N} cruzamentos: Não foi possível calcular")


# Executa o teste para planejar a linha de metrô
testar_tempo_planejamento_metro()