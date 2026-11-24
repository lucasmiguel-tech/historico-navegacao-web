from arvore_urls import NoPagina
from urls import decompor_url 
from pathlib import Path



dominio , segmentos = decompor_url("https://www.ifpb.edu.br/coordenacao")

primeiro_segmento = segmentos[0]

CAMINHO_DOMINIO = Path(dominio,primeiro_segmento)  
CAMINHO_INDEX = Path(dominio,"index.txt")

raiz : NoPagina = NoPagina(dominio)
no_coordenacao : NoPagina = NoPagina(segmentos[0])

raiz.link_esquerdo = no_coordenacao

print(raiz)
print(raiz.link_esquerdo)
print(CAMINHO_DOMINIO)
print(CAMINHO_INDEX)

print("--------")
print(dominio,segmentos)