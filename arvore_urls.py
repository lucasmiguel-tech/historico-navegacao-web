''' 
Os segmentos serão divididos por exemplo: www.ifpb.edu.br/tsi/professores
-> se tornará : nó-raiz -> www.ifpb.edu.br , nó raiz esquerdo -> /tsi , nó-folha -> professores 
'''

from urls import carregar_urls
from pathlib import Path


class NoPagina:
    def __init__(self, segmento : str , index_txt : Path | None = None):
        self.segmento = segmento
        self.index_txt = index_txt #o arquivo que contém o conteúdo da página
        self.links : dict[str, Nopagina] = {} #cria um dicionario cujo a chave será o str segmento e o valor será o objeto dessa pagina 

class ArvoreUrls:
    pass