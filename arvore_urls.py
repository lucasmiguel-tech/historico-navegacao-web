'''
Os segmentos serão divididos por exemplo: www.ifpb.edu.br/tsi/professores
-> se tornará : nó-raiz -> www.ifpb.edu.br , nó raiz esquerdo -> /tsi , nó-folha -> professores 
'''
#BIBLIOTECAS
from pathlib import Path

class NoPagina:
    def __init__(self, segmento : str , conteudo_pag : Path | None = None):
        self.segmento = segmento
        self.conteudo_pag = conteudo_pag # O atributo guarda o caminho onde esta o conteudo.

        self.link_direito : NoPagina | None = None
        self.link_esquerdo : NoPagina | None = None

        self.cadastrada = False

    def __str__(self):
        return f"{self.segmento} | {self.link_direito} | {self.link_esquerdo}"

class ArvoreURLs:
    def __init__(self):
        self.dominios : dict[str , NoPagina] = {}

    # Gerenciamento de domínios
    def adicionar_dominio(self, dominio: str) -> bool:
        if not isinstance(dominio,str):
            return False
        
        dominio = dominio.lower()

        if dominio in self.dominios:
            return False
        
        raiz = NoPagina(dominio)

        self.dominios[dominio] = raiz

        return True
    
    def __str__(self):
        return str(self.dominios)

    # Busca
    def buscar_filho(self, no : NoPagina , segmento : str) -> NoPagina | None: 
        if no.link_direito is None and no.link_esquerdo is None: # Se o No não possui filhos
            return None
        elif no.link_esquerdo is not None and no.link_esquerdo.segmento == segmento: #Se o No filho estiver na esquerda
            return no.link_esquerdo
        elif no.link_direito is not None and no.link_direito.segmento == segmento: #Se o No filho estiver na direita
            return no.link_direito
        
        return None
    
    def buscar_no(self , dominio : str
        ,segmentos : list[str]) -> NoPagina | None:

        dominio = dominio.lower()

        if dominio not in self.dominios.keys():
            return None

        raiz = self.dominios[dominio]

        if (len(segmentos) == 0):
            return raiz

        no_atual = raiz

        for segmento in segmentos:
            filho = self.buscar_filho(no_atual,segmento)

            if filho is None:
                return None
            
            no_atual = filho
        
        return no_atual

    def pagina_cadastrada(self, dominio : str, segmentos : list[str]) -> bool:
        """Indica se a URL (dominio + segmentos) existe e está cadastrada."""
        if not isinstance(dominio,str):
            return False

        no = self.buscar_no(dominio,segmentos)

        return no is not None and no.cadastrada

    def listar_links(self, dominio : str, segmentos : list[str]) -> list[str]:
        """Retorna os links internos (filhos) da página, no formato '/segmento'."""
        if not isinstance(dominio,str):
            return []

        no = self.buscar_no(dominio,segmentos)

        if no is None:
            return []

        return [
            "/" + filho.segmento
            for filho in (no.link_esquerdo, no.link_direito)
            if filho is not None and filho.cadastrada
        ]

    # Inserção
    def verificar_insercao(self,dominio : str , 
        segmentos : list[str]) -> bool:

        if not isinstance(dominio,str):
            return False

        dominio = dominio.lower()

        if dominio not in self.dominios.keys():
            return False

        raiz = self.dominios[dominio]

        no_atual = raiz

        for segmento in segmentos:
            filho = self.buscar_filho(no_atual,segmento)

            if filho is not None:
                no_atual = filho
            elif filho is None:
                if no_atual.link_direito is not None and no_atual.link_esquerdo is not None:
                    return False
                
                return True # O Nó possui pelo menos um dos dois filhos disponivel.
            
        if no_atual.cadastrada:
            return False 
        
        return True # O nó correspondente à URL não está cadastrado.
                

    def inserir_pagina(
        self,
        dominio : str, 
        segmentos : list[str], 
        conteudo_pag : Path | None = None) -> bool:

        if not isinstance(dominio,str):
            return False

        dominio = dominio.lower()

        if not self.verificar_insercao(dominio,segmentos):
            return False
        
        raiz = self.dominios[dominio]

        no_atual = raiz

        for segmento in segmentos:
            filho = self.buscar_filho(no_atual,segmento)

            if filho is not None:
                no_atual = filho
            elif filho is None:
                if no_atual.link_esquerdo is None:
                    novo_no = NoPagina(segmento)
                    no_atual.link_esquerdo = novo_no
                    no_atual = novo_no

                elif no_atual.link_direito is None:
                    novo_no = NoPagina(segmento)
                    no_atual.link_direito = novo_no
                    no_atual = novo_no
                else:
                    return False
            
        no_atual.cadastrada = True

        no_atual.conteudo_pag = conteudo_pag

        return True

    def remover_pagina(self, dominio : str , segmentos : list[str]) -> bool:

        if not isinstance(dominio,str):
            return False

        dominio = dominio.lower()

        if dominio not in self.dominios.keys(): #Dominio inexistente
            return False

        no_encontrado = self.buscar_no(dominio,segmentos) 

        if no_encontrado is None: #Nó não foi encontrado
            return False
        
        if not no_encontrado.cadastrada: #Nó não está cadastrado
            return False
        
        if len(segmentos) == 0:
            self.dominios.pop(dominio)
            return True

        segmentos_pai = segmentos[:-1]
        no_pai = self.buscar_no(dominio,segmentos_pai)

        if no_pai.link_esquerdo is no_encontrado:
            no_pai.link_esquerdo = None
            return True
        elif no_pai.link_direito is no_encontrado:
            no_pai.link_direito = None
            return True
        else:
            return False
        
        return False
            
    def listar_paginas(self, dominio: str = None) -> list[str]:

        paginas = []

        def percorrer(no: NoPagina, dominio : str , caminho: list[str]):
            if no.cadastrada:
                url = "https://" + dominio

                if caminho:
                    url += "/" + "/".join(caminho)

                paginas.append(url)

            if no.link_esquerdo is not None:
                percorrer(no.link_esquerdo, dominio , caminho + [no.link_esquerdo.segmento])

            if no.link_direito is not None:
                percorrer(no.link_direito, dominio , caminho + [no.link_direito.segmento])

        if dominio is None:
            for chave in self.dominios:
                raiz = self.dominios[chave]
                percorrer(raiz, [])

        else:
            dominio = dominio.lower()

            if dominio not in self.dominios:
                return []

            raiz = self.dominios[dominio]
            percorrer(raiz, [])

        return paginas