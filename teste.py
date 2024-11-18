from main import *

########################################## Exemplo: ##########################################

# RegiaoA                      RegiaoB
#    1A ------(100)------- 2A --------(150)-------- 3B
#    |                                               |
#   (120)                                          (200)
#    |                                               |
#    5A -------------------(80)-------------------- 4B


cruzamento1 = Cruzamento(ID=1, cep='RegiaoA')
cruzamento2 = Cruzamento(ID=2, cep='RegiaoA')
cruzamento3 = Cruzamento(ID=3, cep='RegiaoB')
cruzamento4 = Cruzamento(ID=4, cep='RegiaoB')
cruzamento5 = Cruzamento(ID=5, cep='RegiaoA')

segmento1 = Segmento(
    ID_do_segmento=101,
    distancia=100.0,
    custo_de_escavacao=5000.0,
    cruzamento_inicial=cruzamento1,
    cruzamento_final=cruzamento2
)

segmento2 = Segmento(
    ID_do_segmento=102,
    distancia=150.0,
    custo_de_escavacao=7500.0,
    cruzamento_inicial=cruzamento2,
    cruzamento_final=cruzamento3
)

segmento3 = Segmento(
    ID_do_segmento=103,
    distancia=200.0,
    custo_de_escavacao=10000.0,
    cruzamento_inicial=cruzamento3,
    cruzamento_final=cruzamento4
)

segmento4 = Segmento(
    ID_do_segmento=104,
    distancia=120.0,
    custo_de_escavacao=6000.0,
    cruzamento_inicial=cruzamento1,
    cruzamento_final=cruzamento5
)

segmento5 = Segmento(
    ID_do_segmento=105,
    distancia=80.0,
    custo_de_escavacao=4000.0,
    cruzamento_inicial=cruzamento5,
    cruzamento_final=cruzamento4
)

imovel1 = Imovel(1, 'RegiaoA', 'R', 'Rua 1', 101)
imovel2 = Imovel(2, 'RegiaoA', 'C', 'Rua 2', 102)
imovel3 = Imovel(3, 'RegiaoB', 'I', 'Rua 3', 103)
imovel4 = Imovel(4, 'RegiaoB', 'T', 'Rua 4', 104)

segmento1.adicionar_imovel(imovel1)
segmento2.adicionar_imovel(imovel2)
segmento3.adicionar_imovel(imovel3)
segmento4.adicionar_imovel(imovel4)

print("Segmento 1 - Residenciais:", segmento1.quantidade_residencial)
print("Segmento 2 - Comerciais:", segmento2.quantidade_comercial)
print("Segmento 3 - Industriais:", segmento3.quantidade_industrial)
print("Segmento 4 - Turísticos:", segmento4.quantidade_turistico)

cidade = Cidade()
cidade.adicionar_segmento(segmento1)
cidade.adicionar_segmento(segmento2)
cidade.adicionar_segmento(segmento3)
cidade.adicionar_segmento(segmento4)
cidade.adicionar_segmento(segmento5)

cidade.construir_planta()

cidade.construir_subgrafos_regioes()

print("Planta (Grafo):")
for cruzamento_id, edges in cidade.Planta.items():
    print(f"Cruzamento {cruzamento_id}: {edges}")

# Output:
# Planta (Grafo):
# Cruzamento 1: [(2, 5000.0, 100.0)]
# Cruzamento 2: [(1, 5000.0, 100.0), (3, 7500.0, 150.0)]
# Cruzamento 3: [(2, 7500.0, 150.0), (4, 10000.0, 200.0)]
# Cruzamento 4: [(3, 10000.0, 200.0)]
# Cruzamento 5: [(1, 6000.0, 120.0), (4, 4000.0, 80.0)]
print("\nRegiões:")
for regiao_id, cruzamentos in cidade.Regioes.items():
    print(f"Região {regiao_id}: Cruzamentos {cruzamentos}")

# Output:
# Regiões:
# Região RegiaoA: Cruzamentos {1, 2, 5}
# Região RegiaoB: Cruzamentos {3, 4}


print("\nSubgrafos por Região:")
for regiao_id, subgrafo in cidade.Subgrafos_Regioes.items():
    print(f"\n Sugrafo da {regiao_id}:")
    for cruzamento_id, edges in subgrafo.items():
        print(f"  Cruzamento {cruzamento_id}: {edges}")

### Exemplo com djikstra
for i in cidade.Planta:
    print(f"Distâncias do cruzamento {i} aos outros no grafo principal:")
    distancias = calcular_distancias(cidade.Planta, i)
    for cruzamento, distancia in distancias.items():
        print(f"Cruzamento {cruzamento}: {distancia}")
    print("|-----|"*10)