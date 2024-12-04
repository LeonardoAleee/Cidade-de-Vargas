# Criar o mapa
from main import *

# Importar o código anterior
# Assumindo que o código foi salvo em um arquivo chamado `cidade.py`

# Gerar uma cidade com 5x5 cruzamentos divididos em 4 regiões
cidade = generate_city(x=5, y=5, k=4)

# Construir a planta da cidade e as estações de metrô
cidade.construir_planta_tarefa2()
cidade.definir_estacoes()

# Criar um mapa multimodal para a cidade
mapa = Mapa(cidade)
mapa.construir_grafo()

# Escolher cruzamentos de origem e destino
origem_id = 0  # ID do cruzamento inicial
destino_id = 24  # ID do cruzamento final (canto oposto da grade)

# Definir um custo máximo para a rota
custo_maximo = 50.0  # Limite de custo permitido

# Buscar a rota
rota = buscar_rota(mapa, origem_id, destino_id, custo_maximo)
