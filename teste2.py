from main import *
cidade = Cidade()
cruzamento1 = Cruzamento(ID=1, cep='RegiaoA')
cruzamento2 = Cruzamento(ID=2, cep='RegiaoA')
cruzamento3 = Cruzamento(ID=3, cep='RegiaoB')
cruzamento4 = Cruzamento(ID=4, cep='RegiaoB')
cruzamento5 = Cruzamento(ID=5, cep='RegiaoA')
cruzamento6 = Cruzamento(ID=6, cep='RegiaoC')
segmento1 = Segmento(101, 100.0, 5000.0, cruzamento1, cruzamento2)
segmento2 = Segmento(102, 150.0, 7500.0, cruzamento2, cruzamento3)
segmento3 = Segmento(103, 200.0, 10000.0, cruzamento3, cruzamento4)
segmento4 = Segmento(104, 120.0, 6000.0, cruzamento1, cruzamento5)
segmento5 = Segmento(105, 80.0, 4000.0, cruzamento5, cruzamento4)
segmento6 = Segmento(106, 80.0, 4000.0, cruzamento4, cruzamento6)
cidade.adicionar_segmento(segmento1)
cidade.adicionar_segmento(segmento2)
cidade.adicionar_segmento(segmento3)
cidade.adicionar_segmento(segmento4)
cidade.adicionar_segmento(segmento5)
cidade.adicionar_segmento(segmento6) 
cidade.construir_planta_tarefa1()
cidade.construir_subgrafos_regioes()

segmentos_metro = cidade.planejar_metro()
custo_total = sum(seg.custo_de_escavacao for seg in segmentos_metro)
distancia_total = sum(seg.distancia for seg in segmentos_metro)

print(f"Linha de metrô planejada:")
print(f"Número de segmentos: {len(segmentos_metro)}")
print(f"Custo total de escavação: {custo_total}")
print(f"Distância total: {distancia_total} km")

