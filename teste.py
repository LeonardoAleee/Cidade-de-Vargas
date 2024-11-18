from main import *

########################################## Exemplo: ##########################################

# RegiaoA                      RegiaoB
#    1A ------(100)------- 2A --------(150)-------- 3B
#    |                                               |
#   (120)                                          (200)
#    |                                               |                  RegiãoC
#    5A -------------------(80)-------------------- 4B ----------(80)---------- 6C


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

imovel1 = Imovel(1, 'RegiaoA', 'R', 'Rua 1', 101)
imovel2 = Imovel(2, 'RegiaoA', 'C', 'Rua 2', 102)
imovel3 = Imovel(3, 'RegiaoB', 'I', 'Rua 3', 103)
imovel4 = Imovel(4, 'RegiaoB', 'T', 'Rua 4', 104)
imovel5 = Imovel(4, 'RegiaoC', 'T', 'Rua 6', 104)

segmento1.adicionar_imovel(imovel1)
segmento2.adicionar_imovel(imovel2)
segmento3.adicionar_imovel(imovel3)
segmento4.adicionar_imovel(imovel4)
segmento6.adicionar_imovel(imovel5)


cidade = Cidade()
cidade.adicionar_segmento(segmento1)
cidade.adicionar_segmento(segmento2)
cidade.adicionar_segmento(segmento3)
cidade.adicionar_segmento(segmento4)
cidade.adicionar_segmento(segmento5)
cidade.adicionar_segmento(segmento6) 

cidade.construir_planta_tarefa1()
cidade.construir_subgrafos_regioes()

caminho_segmentos = cidade.planejar_linha_onibus(start_cruzamento=1)
print("\nSegmentos da linha de ônibus:")
for segmento in caminho_segmentos:
    print(f"Segmento {segmento.ID_do_segmento}")

centros = encontrar_centro_por_regiao(cidade.Subgrafos_Regioes)

print("Centros por Região:")
for regiao, (cruzamento, distancia_maxima) in centros.items():
    print(f"Região {regiao}: Cruzamento {cruzamento} (Distância Máxima: {distancia_maxima})")