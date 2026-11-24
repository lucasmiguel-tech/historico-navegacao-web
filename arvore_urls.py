'''
Os segmentos serão divididos por exemplo: www.ifpb.edu.br/tsi/professores
-> se tornará : nó-raiz -> www.ifpb.edu.br , nó raiz esquerdo -> /tsi , nó-folha -> professores 
'''
class NoPagina:
    def __init__(self, segmento : str , conteudo_pag : Path | None = None):
        self.segmento = segmento
        self.conteudo_pag = conteudo_pag # O atributo guarda o caminho onde esta o conteudo.

        self.link_direito : NoPagina | None = None
        self.link_esquerdo : NoPagina | None = None

    def __str__(self):
        return f"{self.segmento} | {self.link_direito} | {self.link_esquerdo}"

class ArvoreURLs:
    def __init__(self):
        self.dominios : dict[str , NoPagina] = {} # Cria um dicionário cujo a função é guardar o str raiz e o objeto filhos(nó-raiz(esquerdo,direito))

    def adicionar_dominio(self, dominio: str) -> bool:
        if dominio in self.dominios:
            return False
        
        raiz = NoPagina(dominio)

        self.dominios[dominio] = raiz

        return True
    
    def __str__(self):
        return self.dominios