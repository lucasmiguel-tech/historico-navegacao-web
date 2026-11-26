
"""
Organiza as URLs em árvores binárias, separadas por domínio.

Exemplo:
    www.ifpb.edu.br/tsi/professores

    Raiz: www.ifpb.edu.br
        └── tsi
              └── professores
"""

# BIBLIOTECAS
from pathlib import Path


class NoPagina:
    """Representa um nó da árvore binária de URLs."""

    def __init__(self, segmento: str, conteudo_pag: Path | None = None):
        self.segmento = segmento
        self.conteudo_pag = conteudo_pag

        self.link_direito: NoPagina | None = None
        self.link_esquerdo: NoPagina | None = None

        self.cadastrada = False

    def __str__(self):
        """Retorna uma representação textual do nó."""

        return f"{self.segmento} | {self.link_direito} | {self.link_esquerdo}"


class ArvoreURLs:
    """Gerencia as árvores binárias de páginas por domínio."""

    def __init__(self):
        self.dominios: dict[str, NoPagina] = {}

    # GERENCIAMENTO DE DOMÍNIOS
    def adicionar_dominio(self, dominio: str) -> bool:
        """Adiciona um novo domínio à árvore."""

        if not isinstance(dominio, str):
            return False

        dominio = dominio.lower()

        if dominio in self.dominios:
            return False

        # O domínio representa a raiz da árvore.
        raiz = NoPagina(dominio)

        self.dominios[dominio] = raiz

        return True

    def __str__(self):
        """Retorna os domínios armazenados na árvore."""

        return str(self.dominios)

    # BUSCA
    def buscar_filho(self, no: NoPagina, segmento: str) -> NoPagina | None:
        """Busca um segmento entre os filhos de determinado nó."""

        if no.link_direito is None and no.link_esquerdo is None:
            return None

        elif no.link_esquerdo is not None and no.link_esquerdo.segmento == segmento:
            return no.link_esquerdo

        elif no.link_direito is not None and no.link_direito.segmento == segmento:
            return no.link_direito

        return None

    def buscar_no(self, dominio: str, segmentos: list[str]) -> NoPagina | None:
        """Localiza um nó a partir do domínio e dos segmentos da URL."""

        dominio = dominio.lower()

        if dominio not in self.dominios.keys():
            return None

        raiz = self.dominios[dominio]

        if len(segmentos) == 0:
            return raiz

        no_atual = raiz

        for segmento in segmentos:
            filho = self.buscar_filho(no_atual, segmento)

            if filho is None:
                return None

            no_atual = filho

        return no_atual

    def pagina_cadastrada(self, dominio: str, segmentos: list[str]) -> bool:
        """Verifica se a URL corresponde a uma página cadastrada."""

        if not isinstance(dominio, str):
            return False

        no = self.buscar_no(dominio, segmentos)

        return no is not None and no.cadastrada

    def listar_links(self, dominio: str, segmentos: list[str]) -> list[str]:
        """Retorna os links internos cadastrados de uma página."""

        if not isinstance(dominio, str):
            return []

        no = self.buscar_no(dominio, segmentos)

        if no is None:
            return []

        return [
            "/" + filho.segmento
            for filho in (no.link_esquerdo, no.link_direito)
            if filho is not None and filho.cadastrada
        ]

    # INSERÇÃO
    def verificar_insercao(self, dominio: str, segmentos: list[str]) -> bool:
        """Verifica se existe espaço para inserir uma página na árvore."""

        if not isinstance(dominio, str):
            return False

        dominio = dominio.lower()

        if dominio not in self.dominios.keys():
            return False

        raiz = self.dominios[dominio]

        no_atual = raiz

        for segmento in segmentos:
            filho = self.buscar_filho(no_atual, segmento)

            if filho is not None:
                no_atual = filho

            elif filho is None:
                # Cada nó pode possuir no máximo dois filhos.
                if no_atual.link_direito is not None and no_atual.link_esquerdo is not None:
                    return False

                return True

        if no_atual.cadastrada:
            return False

        return True

    def inserir_pagina(
        self,
        dominio: str,
        segmentos: list[str],
        conteudo_pag: Path | None = None
    ) -> bool:
        """Insere uma página na árvore e associa seu arquivo de conteúdo."""

        if not isinstance(dominio, str):
            return False

        dominio = dominio.lower()

        if not self.verificar_insercao(dominio, segmentos):
            return False

        raiz = self.dominios[dominio]

        no_atual = raiz

        for segmento in segmentos:
            filho = self.buscar_filho(no_atual, segmento)

            if filho is not None:
                no_atual = filho

            elif filho is None:
                # Insere o novo nó na primeira posição disponível.
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

        # Marca o último nó como página cadastrada.
        no_atual.cadastrada = True
        no_atual.conteudo_pag = conteudo_pag

        return True

    # REMOÇÃO
    def remover_pagina(self, dominio: str, segmentos: list[str]) -> bool:
        """Remove uma página cadastrada da árvore."""

        if not isinstance(dominio, str):
            return False

        dominio = dominio.lower()

        if dominio not in self.dominios.keys():
            return False

        no_encontrado = self.buscar_no(dominio, segmentos)

        if no_encontrado is None:
            return False

        if not no_encontrado.cadastrada:
            return False

        if len(segmentos) == 0:
            self.dominios.pop(dominio)
            return True

        segmentos_pai = segmentos[:-1]
        no_pai = self.buscar_no(dominio, segmentos_pai)

        # Desconecta o nó da referência de seu pai.
        if no_pai.link_esquerdo is no_encontrado:
            no_pai.link_esquerdo = None
            return True

        elif no_pai.link_direito is no_encontrado:
            no_pai.link_direito = None
            return True

        else:
            return False

        return False

    # LISTAGEM DE PÁGINAS
    def listar_paginas(self, dominio: str = None) -> list[str]:
        """Retorna as URLs cadastradas de um ou todos os domínios."""

        paginas = []

        def percorrer(no: NoPagina, dominio: str, caminho: list[str]):
            """Percorre recursivamente os nós da árvore."""

            if no.cadastrada:
                url = "https://" + dominio

                if caminho:
                    url += "/" + "/".join(caminho)

                paginas.append(url)

            # Continua percorrendo os filhos, inclusive nós intermediários.
            if no.link_esquerdo is not None:
                percorrer(
                    no.link_esquerdo,
                    dominio,
                    caminho + [no.link_esquerdo.segmento]
                )

            if no.link_direito is not None:
                percorrer(
                    no.link_direito,
                    dominio,
                    caminho + [no.link_direito.segmento]
                )

        if dominio is None:
            for chave in self.dominios:
                raiz = self.dominios[chave]
                percorrer(raiz, chave, [])

        else:
            dominio = dominio.lower()

            if dominio not in self.dominios:
                return []

            raiz = self.dominios[dominio]
            percorrer(raiz, dominio, [])

        return paginas