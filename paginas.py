"""
Armazenamento físico das páginas do projeto.

Responsabilidade única: criar, ler, atualizar, verificar e remover os
diretórios e arquivos "index.txt" que guardam o conteúdo de cada página.

Estrutura física:

    dados/
    └── paginas/
        └── www.ifpb.edu.br/
            ├── index.txt                 -> https://www.ifpb.edu.br
            └── tsi/
                ├── index.txt             -> https://www.ifpb.edu.br/tsi
                └── alunos/
                    └── index.txt         -> https://www.ifpb.edu.br/tsi/alunos

Os métodos recebem sempre o par (dominio, segmentos) devolvido por
urls.decompor_url(); o caminho do arquivo é montado aqui dentro.

    dominio, segmentos = decompor_url(url)
    armazenamento.criar_pagina(dominio, segmentos, "texto da página")

Este módulo NÃO decide se uma URL é cadastrada (isso é papel da árvore e do
arquivo urls.txt) e NÃO imprime nada na tela: ele só lança exceções, que a
interface trata e transforma em mensagens para o usuário.
"""

# BIBLIOTECAS
import shutil
from pathlib import Path

from urls import validar_dominio, validar_segmento


# CONSTANTES
CAMINHO_PAGINAS = Path(__file__).parent / "dados" / "paginas"
NOME_ARQUIVO = "index.txt"


# EXCEÇÕES
class ErroPagina(Exception):
    """Erro base de todas as operações com páginas."""


class PaginaInvalida(ErroPagina, ValueError):
    """Domínio ou segmentos não formam um caminho de página válido."""


class PaginaNaoEncontrada(ErroPagina):
    """O arquivo index.txt da página não existe em disco."""


class PaginaJaExiste(ErroPagina):
    """Tentativa de criar uma página que já possui arquivo em disco."""


class ArmazenamentoPaginas:
    """
    Gerencia os arquivos index.txt das páginas dentro de uma pasta base.

    A pasta base pode ser trocada (por exemplo, por uma pasta temporária
    nos testes) sem afetar os dados reais do projeto.
    """

    def __init__(self, pasta_base: Path | str = CAMINHO_PAGINAS) -> None:
        self._pasta_base = Path(pasta_base).resolve()

    @property
    def pasta_base(self) -> Path:
        """Pasta onde ficam os diretórios dos domínios."""
        return self._pasta_base

    # CAMINHOS
    def caminho_pasta(self, dominio: str, segmentos: list[str]) -> Path:
        """
        Monta o diretório da página: <base>/<dominio>/<seg1>/<seg2>/...

        Lança PaginaInvalida se o domínio ou algum segmento não for válido
        ou se o caminho resultante escapar da pasta base.
        """
        if not isinstance(dominio, str) or not validar_dominio(dominio):
            raise PaginaInvalida(f"Domínio inválido: {dominio!r}")

        if not isinstance(segmentos, (list, tuple)):
            raise PaginaInvalida("Os segmentos devem ser uma lista de textos.")

        for segmento in segmentos:
            if not validar_segmento(segmento):
                raise PaginaInvalida(f"Segmento inválido: {segmento!r}")

        pasta = self._pasta_base.joinpath(dominio.lower(), *segmentos).resolve()

        # Defesa extra: o caminho final precisa ficar dentro da pasta base.
        if not pasta.is_relative_to(self._pasta_base) or pasta == self._pasta_base:
            raise PaginaInvalida("Caminho da página fora da pasta de dados.")

        return pasta

    def caminho_arquivo(self, dominio: str, segmentos: list[str]) -> Path:
        """Monta o caminho do index.txt da página."""
        return self.caminho_pasta(dominio, segmentos) / NOME_ARQUIVO

    # VERIFICAÇÃO
    def pagina_existe(self, dominio: str, segmentos: list[str]) -> bool:
        """Indica se a página possui arquivo index.txt em disco."""
        try:
            return self.caminho_arquivo(dominio, segmentos).is_file()
        except PaginaInvalida:
            return False

    # CRIAÇÃO
    def criar_pagina(
        self,
        dominio: str,
        segmentos: list[str],
        conteudo: str = ""
    ) -> Path:
        """
        Cria os diretórios necessários e o index.txt preenchido.

        Retorna o Path do arquivo criado. Lança PaginaJaExiste se a página
        já tiver arquivo e ErroPagina se não for possível gravar.
        """
        arquivo = self.caminho_arquivo(dominio, segmentos)

        try:
            arquivo.parent.mkdir(parents=True, exist_ok=True)

            # Modo "x": falha se o arquivo já existir (não sobrescreve).
            with arquivo.open("x", encoding="utf-8") as saida:
                saida.write(conteudo)

        except FileExistsError as erro:
            raise PaginaJaExiste(f"A página já existe: {arquivo}") from erro

        except OSError as erro:
            raise ErroPagina(f"Não foi possível criar a página: {erro}") from erro

        return arquivo

    # LEITURA
    def ler_pagina(self, dominio: str, segmentos: list[str]) -> str:
        """
        Retorna o conteúdo do index.txt da página.

        Lança PaginaNaoEncontrada se o arquivo não existir.
        """
        arquivo = self.caminho_arquivo(dominio, segmentos)

        try:
            with arquivo.open("r", encoding="utf-8") as entrada:
                return entrada.read()

        except FileNotFoundError as erro:
            raise PaginaNaoEncontrada(f"Página não encontrada: {arquivo}") from erro

        except OSError as erro:
            raise ErroPagina(f"Não foi possível ler a página: {erro}") from erro

    # ATUALIZAÇÃO
    def atualizar_pagina(
        self,
        dominio: str,
        segmentos: list[str],
        conteudo: str
    ) -> Path:
        """
        Substitui o conteúdo de uma página que já existe.

        Lança PaginaNaoEncontrada se a página ainda não tiver arquivo.
        """
        arquivo = self.caminho_arquivo(dominio, segmentos)

        if not arquivo.is_file():
            raise PaginaNaoEncontrada(f"Página não encontrada: {arquivo}")

        try:
            with arquivo.open("w", encoding="utf-8") as saida:
                saida.write(conteudo)

        except OSError as erro:
            raise ErroPagina(f"Não foi possível atualizar a página: {erro}") from erro

        return arquivo

    # REMOÇÃO
    def remover_pagina(self, dominio: str, segmentos: list[str]) -> bool:
        """
        Remove o diretório da página e todas as suas subpáginas.

        Acompanha a árvore: remover um nó também remove a sua subárvore.
        Retorna False se a página não existir em disco.
        """
        pasta = self.caminho_pasta(dominio, segmentos)

        if not pasta.is_dir():
            return False

        try:
            shutil.rmtree(pasta)

        except OSError as erro:
            raise ErroPagina(f"Não foi possível remover a página: {erro}") from erro

        return True

    # CONSULTA
    def listar_paginas(self) -> list[tuple[str, list[str]]]:
        """
        Lista todas as páginas com index.txt em disco.

        Retorna pares (dominio, segmentos), no mesmo formato de
        decompor_url(), ordenados para facilitar a montagem da árvore.
        """
        if not self._pasta_base.is_dir():
            return []

        paginas = []

        for arquivo in self._pasta_base.rglob(NOME_ARQUIVO):
            partes = arquivo.parent.relative_to(self._pasta_base).parts

            if not partes:
                continue  # index.txt solto na pasta base: não é página.

            paginas.append((partes[0], list(partes[1:])))

        return sorted(paginas)
