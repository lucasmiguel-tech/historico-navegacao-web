
"""
Gerencia a árvore binária de URLs do navegador.

A estrutura utiliza a representação filho-esquerdo/irmão-direito
para representar os domínios e os caminhos das páginas.

Organização dos nós:
- O nó raiz representa o domínio.
- O filho esquerdo representa o primeiro filho.
- O filho direito representa o próximo irmão.

Cada página pode possuir, no máximo, dois filhos diretos.

Exemplo:
    https://www.ifpb.edu.br/tsi/professores

    www.ifpb.edu.br (raiz)
             |
           /tsi
             |
        /professores

Cada nó armazena:
- O segmento correspondente à URL.
- O caminho do arquivo que contém o conteúdo da página.
- As referências aos nós filhos.
- Um indicador que informa se a página está cadastrada.
"""

# BIBLIOTECAS

from pathlib import Path


class NoPagina:
    def __init__(
        self,
        segmento: str,
        conteudo_pag: Path | None = None
    ):
        self.segmento = segmento
        self.conteudo_pag = conteudo_pag

        # Filho esquerdo: primeiro filho.
        # Filho direito: próximo irmão.
        self.link_direito: NoPagina | None = None
        self.link_esquerdo: NoPagina | None = None

        self.cadastrada = False

    def __str__(self) -> str:
        return (
            f"Segmento: {self.segmento} | "
            f"Cadastrada: {self.cadastrada}"
        )


class ArvoreURLs:

    def __init__(self):
        self.dominios: dict[str, NoPagina] = {}

    def __str__(self) -> str:
        return str(self.dominios)

    # ==================================================
    # NORMALIZAÇÃO
    # ==================================================

    def _normalizar_dominio(self, dominio: str) -> str | None:
        """
        Normaliza o domínio recebido.

        O domínio deve ser informado sem protocolo
        e sem caminho.
        """

        if not isinstance(dominio, str):
            return None

        dominio = dominio.strip().lower()

        if not dominio:
            return None

        if "://" in dominio or "/" in dominio:
            return None

        if any(caractere.isspace() for caractere in dominio):
            return None

        return dominio

    def _normalizar_segmentos(
        self,
        segmentos: list[str]
    ) -> list[str] | None:
        """
        Normaliza os segmentos da URL.

        Exemplos aceitos:
            ["tsi", "professores"]
            ["/tsi/professores"]

        Retorna None se algum segmento for inválido.
        """

        if not isinstance(segmentos, list):
            return None

        resultado = []

        for segmento in segmentos:

            if not isinstance(segmento, str):
                return None

            segmento = segmento.strip()

            if not segmento:
                return None

            partes = segmento.strip("/").split("/")

            for parte in partes:

                if not parte:
                    continue

                if any(caractere.isspace() for caractere in parte):
                    return None

                if "?" in parte or "#" in parte:
                    return None

                resultado.append(parte)

        return resultado

    # ==================================================
    # GERENCIAMENTO DE DOMÍNIOS
    # ==================================================

    def adicionar_dominio(self, dominio: str) -> bool:
        """
        Adiciona um domínio à árvore.

        O domínio é criado como nó raiz.
        """

        dominio = self._normalizar_dominio(dominio)

        if dominio is None:
            return False

        if dominio in self.dominios:
            return False

        self.dominios[dominio] = NoPagina(dominio)

        return True

    # ==================================================
    # BUSCA
    # ==================================================

    def buscar_filho(
        self,
        no: NoPagina,
        segmento: str
    ) -> NoPagina | None:
        """
        Procura um filho direto de determinado nó.

        Na representação filho-esquerdo/irmão-direito:

        1. O primeiro filho está em link_esquerdo.
        2. O segundo filho está em link_direito do primeiro.

        A busca considera, portanto, no máximo dois filhos.
        """

        if no is None or not isinstance(segmento, str):
            return None

        filho = no.link_esquerdo

        quantidade = 0

        while filho is not None and quantidade < 2:

            if filho.segmento == segmento:
                return filho

            filho = filho.link_direito
            quantidade += 1

        return None

    def buscar_no(
        self,
        dominio: str,
        segmentos: list[str]
    ) -> NoPagina | None:
        """
        Localiza um nó percorrendo os segmentos da URL.

        Retorna None caso o domínio ou algum segmento
        não seja encontrado.

        Também pode retornar nós intermediários
        que ainda não estejam cadastrados como páginas.
        """

        dominio = self._normalizar_dominio(dominio)

        if dominio is None:
            return None

        segmentos = self._normalizar_segmentos(segmentos)

        if segmentos is None:
            return None

        no_atual = self.dominios.get(dominio)

        if no_atual is None:
            return None

        for segmento in segmentos:

            no_atual = self.buscar_filho(
                no_atual,
                segmento
            )

            if no_atual is None:
                return None

        return no_atual

    def pagina_cadastrada(
        self,
        dominio: str,
        segmentos: list[str]
    ) -> bool:
        """
        Indica se a URL existe e está cadastrada.
        """

        no = self.buscar_no(dominio, segmentos)

        return no is not None and no.cadastrada

    # ==================================================
    # VERIFICAÇÃO DE INSERÇÃO
    # ==================================================

    def verificar_insercao(
        self,
        dominio: str,
        segmentos: list[str]
    ) -> bool:
        """
        Verifica se uma página pode ser inserida.

        Regras:
        - O domínio precisa existir.
        - A página não pode já estar cadastrada.
        - Cada nó pode possuir no máximo dois filhos.
        - Nós intermediários podem ser criados.
        """

        dominio = self._normalizar_dominio(dominio)

        if dominio is None:
            return False

        segmentos = self._normalizar_segmentos(segmentos)

        if segmentos is None:
            return False

        if dominio not in self.dominios:
            return False

        no_atual = self.dominios[dominio]

        # Cadastro do próprio domínio.
        if not segmentos:
            return not no_atual.cadastrada

        for segmento in segmentos:

            filho = self.buscar_filho(
                no_atual,
                segmento
            )

            # O segmento já existe.
            if filho is not None:
                no_atual = filho
                continue

            # O segmento ainda não existe.
            # Verifica quantos filhos o nó atual possui.
            primeiro_filho = no_atual.link_esquerdo

            if primeiro_filho is None:
                return True

            segundo_filho = primeiro_filho.link_direito

            if segundo_filho is None:
                return True

            # O nó já possui dois filhos.
            return False

        # Todos os segmentos já existem.
        # Verifica se o último nó ainda não está cadastrado.
        return not no_atual.cadastrada

    # ==================================================
    # INSERÇÃO
    # ==================================================

    def inserir_pagina(
        self,
        dominio: str,
        segmentos: list[str],
        conteudo_pag: Path | None = None
    ) -> bool:
        """
        Insere uma página na árvore.

        Os nós intermediários são criados automaticamente.

        O primeiro filho é conectado à esquerda.
        O segundo filho é conectado à direita do primeiro.

        Somente o último nó é marcado como cadastrado.
        """

        dominio = self._normalizar_dominio(dominio)

        if dominio is None:
            return False

        segmentos = self._normalizar_segmentos(segmentos)

        if segmentos is None:
            return False

        if conteudo_pag is not None:
            if not isinstance(conteudo_pag, Path):
                return False

        if not self.verificar_insercao(dominio, segmentos):
            return False

        no_atual = self.dominios[dominio]

        # Cadastro do próprio domínio.
        if not segmentos:

            no_atual.cadastrada = True
            no_atual.conteudo_pag = conteudo_pag

            return True

        for segmento in segmentos:

            filho = self.buscar_filho(
                no_atual,
                segmento
            )

            # Se o segmento já existe, continua a descida.
            if filho is not None:
                no_atual = filho
                continue

            # Cria um novo nó.
            novo_no = NoPagina(segmento)

            primeiro_filho = no_atual.link_esquerdo

            # Se não existe primeiro filho, ocupa a esquerda.
            if primeiro_filho is None:

                no_atual.link_esquerdo = novo_no

            else:
                # Caso contrário, ocupa a posição do segundo filho.
                primeiro_filho.link_direito = novo_no

            no_atual = novo_no

        # Marca o último nó como página cadastrada.
        no_atual.cadastrada = True
        no_atual.conteudo_pag = conteudo_pag

        return True

    # ==================================================
    # REMOÇÃO DE SUBÁRVORE
    # ==================================================

    def _remover_subarvore(self, no: NoPagina | None) -> None:
        """
        Remove logicamente os descendentes de um nó.

        Importante:
        O link_direito do próprio nó aponta para seu irmão.
        Por isso, não podemos remover esse irmão ao excluir
        somente a subárvore do nó recebido.

        A função percorre os filhos e seus irmãos,
        removendo as respectivas subárvores.
        """

        if no is None:
            return

        filho = no.link_esquerdo

        # Desconecta os filhos do nó atual.
        no.link_esquerdo = None

        while filho is not None:

            proximo_irmao = filho.link_direito

            # Separa o irmão para que ele não seja
            # confundido com um descendente do filho atual.
            filho.link_direito = None

            # Remove os descendentes do filho atual.
            self._remover_subarvore(filho)

            # Continua com o próximo irmão.
            filho = proximo_irmao

        no.conteudo_pag = None
        no.cadastrada = False

    # ==================================================
    # REMOÇÃO DE PÁGINAS
    # ==================================================

    def remover_pagina(
        self,
        dominio: str,
        segmentos: list[str]
    ) -> bool:
        """
        Remove uma página cadastrada e toda sua subárvore.

        Se o nó removido for o primeiro filho e possuir
        um irmão, esse irmão será promovido à primeira posição.

        A remoção não apaga arquivos físicos de conteúdo.
        """

        dominio = self._normalizar_dominio(dominio)

        if dominio is None:
            return False

        segmentos = self._normalizar_segmentos(segmentos)

        if segmentos is None:
            return False

        if dominio not in self.dominios:
            return False

        # Remoção do próprio domínio.
        if not segmentos:

            raiz = self.dominios[dominio]

            if not raiz.cadastrada:
                return False

            self._remover_subarvore(raiz)

            del self.dominios[dominio]

            return True

        # Localiza o nó que será removido.
        no_encontrado = self.buscar_no(
            dominio,
            segmentos
        )

        if no_encontrado is None:
            return False

        if not no_encontrado.cadastrada:
            return False

        # Localiza o pai do nó.
        no_pai = self.buscar_no(
            dominio,
            segmentos[:-1]
        )

        if no_pai is None:
            return False

        primeiro_filho = no_pai.link_esquerdo

        if primeiro_filho is no_encontrado:

            # O nó removido é o primeiro filho.
            # Seu irmão passa a ocupar a primeira posição.
            no_pai.link_esquerdo = no_encontrado.link_direito

        elif (
            primeiro_filho is not None
            and primeiro_filho.link_direito is no_encontrado
        ):

            # O nó removido é o segundo filho.
            # O primeiro filho deixa de apontar para ele.
            primeiro_filho.link_direito = no_encontrado.link_direito

        else:
            return False

        # Separa o nó removido de seu irmão.
        no_encontrado.link_direito = None

        # Remove todos os descendentes do nó.
        self._remover_subarvore(no_encontrado)

        return True

    # ==================================================
    # LISTAGEM DE LINKS DISPONÍVEIS
    # ==================================================

    def listar_links(
        self,
        dominio: str,
        segmentos: list[str]
    ) -> list[str]:
        """
        Retorna os links internos diretos de uma página.

        Retorna somente filhos cadastrados.

        Os links são apresentados como URLs completas,
        utilizando HTTPS.
        """

        dominio = self._normalizar_dominio(dominio)

        if dominio is None:
            return []

        segmentos = self._normalizar_segmentos(segmentos)

        if segmentos is None:
            return []

        no_atual = self.buscar_no(
            dominio,
            segmentos
        )

        if no_atual is None or not no_atual.cadastrada:
            return []

        # Monta o endereço completo da página atual.
        prefixo = f"https://{dominio}"

        for segmento in segmentos:
            prefixo += f"/{segmento}"

        links = []

        filho = no_atual.link_esquerdo

        quantidade = 0

        while filho is not None and quantidade < 2:

            if filho.cadastrada:

                url = f"{prefixo}/{filho.segmento}"

                links.append(url)

            filho = filho.link_direito
            quantidade += 1

        return links

    # ==================================================
    # PERCORRIMENTO DA ÁRVORE
    # ==================================================

    def _percorrer_no(
        self,
        no: NoPagina | None,
        prefixo: str,
        paginas: list[str]
    ) -> None:
        """
        Percorre os nós utilizando pré-ordem.

        1. Visita o nó atual.
        2. Percorre o filho esquerdo usando a URL atual.
        3. Percorre o irmão direito usando o prefixo do pai.

        Assim, o irmão permanece no mesmo nível hierárquico.
        """

        if no is None:
            return

        url_atual = f"{prefixo}/{no.segmento}"

        if no.cadastrada:
            paginas.append(url_atual)

        # Desce para os filhos do nó atual.
        self._percorrer_no(
            no.link_esquerdo,
            url_atual,
            paginas
        )

        # Percorre o irmão do nó atual.
        # O prefixo original é preservado.
        self._percorrer_no(
            no.link_direito,
            prefixo,
            paginas
        )

    def percorrer_arvore(self) -> list[str]:
        """
        Percorre todos os domínios e retorna
        somente as páginas cadastradas.
        """

        paginas = []

        for dominio, raiz in self.dominios.items():

            prefixo = f"https://{dominio}"

            if raiz.cadastrada:
                paginas.append(prefixo)

            self._percorrer_no(
                raiz.link_esquerdo,
                prefixo,
                paginas
            )

        return paginas

    # ==================================================
    # CONSULTA E LISTAGEM DE PÁGINAS
    # ==================================================

    def listar_paginas(
        self,
        dominio: str | None = None
    ) -> list[str]:
        """
        Lista as páginas cadastradas.

        Se dominio for None:
            Retorna as páginas de todos os domínios.

        Se um domínio for informado:
            Retorna somente as páginas daquele domínio.
        """

        if dominio is None:
            return self.percorrer_arvore()

        dominio = self._normalizar_dominio(dominio)

        if dominio is None:
            return []

        raiz = self.dominios.get(dominio)

        if raiz is None:
            return []

        paginas = []

        prefixo = f"https://{dominio}"

        if raiz.cadastrada:
            paginas.append(prefixo)

        self._percorrer_no(
            raiz.link_esquerdo,
            prefixo,
            paginas
        )

        return paginas