from arvore_urls import NoPagina , ArvoreURLs
from urls import decompor_url 
from pathlib import Path



dominio , segmentos = decompor_url("https://www.ifpb.edu.br/coordenacao")

CAMINHO_DOMINIO = Path(dominio,segmentos[0])  
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


print("-----------------")
arvore = ArvoreURLs()
print(arvore.adicionar_dominio(dominio))
print(arvore.buscar_filho(raiz,"professores"))

print("-----------")
if dominio in arvore.dominios.keys():
    print(dominio)


pasta_base = Path(__file__).resolve().parent
pasta_conteudo = pasta_base / "dados" / "paginas" / dominio / Path(*segmentos) / "index.txt"

print(pasta_conteudo)

with pasta_conteudo.open("a",encoding="utf-8") as arquivo:
    arquivo.write("Informações : ...")