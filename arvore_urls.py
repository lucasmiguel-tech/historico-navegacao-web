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
        self.links : dict[str, NoPagina] = {} #cria um dicionario cujo a chave será o str segmento e o valor será o objeto dessa pagina 

class ArvoreURLs:
    def __init__(self):
        self.dominios : dict[str , NoPagina] = {} #cria um dicionário cujo a função é guardar o str raiz e o objeto filhos(nó-raiz(esquerdo,direito))

    def adicionar_dominio(self, dominio: str) -> bool:
        if dominio in self.dominios:
            return False
        
        raiz = Nopagina(dominio)

        self.dominios[dominio] = raiz

        return True