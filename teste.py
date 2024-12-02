from main import *

########################################## Exemplo: ##########################################

# RegiaoA                      RegiaoB
#    1A ------(100)------- 2A --------(150)-------- 3B
#    |                                               |
#   (120)                                          (200)
#    |                                               |                  RegiãoC
#    5A -------------------(80)-------------------- 4B ----------(80)---------- 6C



import time

def testar_tempo_planejamento():
    import math
    tamanhos = [10, 100, 1000, 10000, 100000, 1000000]
    k = 5
    resultados = []

    for N in tamanhos:
        print(f"\nTestando para N = {N} cruzamentos...")
        # Calcular dimensões x e y para ter aproximadamente N cruzamentos (x * y = N)
        x = int(math.sqrt(N))
        y = N // x
        print(f"Dimensões da grade: x = {x}, y = {y}")
        
        cidade = generate_city(x, y, k)
          
        cru_inicial = cidade.Segmentos[0].cruzamento_inicial
        start_cruzamento = cru_inicial
        
        start_time = time.time()
        try:
            caminho_segmentos = cidade.planejar_linha_onibus(start_cruzamento=start_cruzamento)
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




cidade = generate_city(2, 2, 2)

for seg in cidade.Segmentos.keys():
    print(f"Cruzamento Inicial {cidade.Segmentos[seg].cruzamento_inicial.ID}, Cruzamento Final {cidade.Segmentos[seg].cruzamento_final.ID},")
