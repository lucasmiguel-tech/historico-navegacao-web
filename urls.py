
"""
Gerencia as URLs disponíveis para navegação.

Responsabilidades:
- Carregar URLs de dados/urls.txt.
- Padronizar e validar o formato das URLs.
- Decompor URLs em domínio e segmentos.
- Cadastrar e remover URLs do arquivo.
"""

# BIBLIOTECAS
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


# CONSTANTES
CAMINHO_URLS = Path(__file__).parent / "dados" / "urls.txt"

EXTENSOES = sorted(
    [
        # Extensões genéricas
        ".com",
        ".org",
        ".net",
        ".edu",
        ".gov",
        ".mil",
        ".int",

        # Extensões brasileiras
        ".com.br",
        ".org.br",
        ".net.br",
        ".edu.br",
        ".gov.br",
        ".mil.br",
        ".app.br",
        ".blog.br",
        ".dev.br",
        ".info.br",
    ],
    key=len,
    reverse=True
)


# PADRONIZAÇÃO DA URL
def padronizar_url(url: str) -> str:
    """Converte a URL para o protocolo HTTPS."""

    url = url.strip()

    if not url:
        return url

    # Se não possui protocolo, acrescenta HTTPS.
    if "://" not in url:
        url = "https://" + url

    partes = urlsplit(url)

    protocolo = partes.scheme.lower()

    # Aceita somente HTTP e HTTPS para a normalização.
    if protocolo not in ("http", "https"):
        return url

    # Preserva a autoridade para que portas e credenciais
    # possam ser identificadas e rejeitadas na validação.
    autoridade = partes.netloc.lower()

    return urlunsplit((
        "https",
        autoridade,
        partes.path,
        partes.query,
        partes.fragment
    ))


# VALIDAÇÃO DE RÓTULO, DOMÍNIO E SEGMENTOS
def validar_rotulo(rotulo: str) -> bool:
    """Verifica se um rótulo de domínio possui formato válido."""

    if not isinstance(rotulo, str):
        return False

    if not rotulo or not rotulo.isascii():
        return False

    if not (1 <= len(rotulo) <= 63):
        return False

    if rotulo.startswith("-") or rotulo.endswith("-"):
        return False

    permitidos = "abcdefghijklmnopqrstuvwxyz0123456789-"

    if any(caractere.lower() not in permitidos for caractere in rotulo):
        return False

    return True


def validar_dominio(dominio: str) -> bool:
    """Verifica se o domínio possui rótulos e extensão permitidos."""

    if not isinstance(dominio, str):
        return False

    if not (1 <= len(dominio) <= 253):
        return False

    rotulos = dominio.split(".")

    if any(not validar_rotulo(rotulo) for rotulo in rotulos):
        return False

    # Verifica se a extensão corresponde aos rótulos finais.
    rotulos_dominio = dominio.lower().split(".")

    for extensao in EXTENSOES:
        rotulos_extensao = extensao.lstrip(".").split(".")

        if rotulos_dominio[-len(rotulos_extensao):] == rotulos_extensao:
            return True

    return False


def validar_segmento(segmento: str) -> bool:
    """Verifica se um segmento pode ser utilizado no caminho da URL."""

    if not isinstance(segmento, str):
        return False

    if not segmento or any(caractere.isspace() for caractere in segmento):
        return False

    if segmento in (".", ".."):
        return False

    rejeicoes = [
        "/", "\\", "|", "?", "#", ":", "*",
        "<", ">", '"'
    ]

    if any(simbolo in segmento for simbolo in rejeicoes):
        return False

    # Impede caracteres de controle.
    if any(ord(caractere) < 32 for caractere in segmento):
        return False

    return True


# VALIDAÇÃO E DECOMPOSIÇÃO DA URL
def validar_url(url: str) -> bool:
    """Verifica se a URL possui um formato básico válido."""

    if not isinstance(url, str):
        return False

    url = url.strip()

    if not url or any(caractere.isspace() for caractere in url):
        return False

    try:
        # Padroniza antes de validar.
        url = padronizar_url(url)

        partes = urlsplit(url)

        if partes.scheme != "https":
            return False

        if partes.hostname is None:
            return False

        # Rejeita credenciais.
        if partes.username is not None or partes.password is not None:
            return False

        # Rejeita portas.
        if partes.port is not None:
            return False

        # Rejeita parâmetros de consulta e fragmentos.
        if partes.query or partes.fragment:
            return False

        dominio, segmentos = decompor_url(url)

        if not validar_dominio(dominio):
            return False

        for segmento in segmentos:
            if not validar_segmento(segmento):
                return False

        return True

    except ValueError:
        return False


def decompor_url(url: str) -> tuple[str, list[str]]:
    """Separa a URL em domínio e segmentos."""

    url = padronizar_url(url)

    partes = urlsplit(url)

    dominio = partes.hostname

    segmentos = [
        segmento
        for segmento in partes.path.split("/")
        if segmento
    ]

    return dominio, segmentos


# PERSISTÊNCIA DAS URLs
def carregar_urls() -> list[str]:
    """Carrega as URLs cadastradas no arquivo."""

    urls = []

    try:
        with open(CAMINHO_URLS, "r", encoding="utf-8") as arquivo:

            for linha in arquivo:
                url = linha.strip()

                if not url:
                    continue

                if validar_url(url):
                    url = padronizar_url(url)

                    if url not in urls:
                        urls.append(url)

    except FileNotFoundError:
        return []

    except OSError as erro:
        raise RuntimeError(
            f"Erro ao ler o arquivo de URLs: {erro}"
        ) from erro

    return urls


def adicionar_url(
    url: str,
    urls_conhecidas: list[str]
) -> tuple[bool, str]:
    """Valida, salva e adiciona uma URL à lista em memória."""

    if not isinstance(url, str):
        return False, "URL possui formato inválido."

    url = padronizar_url(url)

    if not validar_url(url):
        return False, "URL possui formato inválido."

    if url in urls_conhecidas:
        return False, "URL já cadastrada."

    try:
        with open(CAMINHO_URLS, "a", encoding="utf-8") as arquivo:
            arquivo.write(url + "\n")

    except OSError:
        return False, "Não foi possível salvar a URL."

    # Atualiza a lista somente depois de salvar.
    urls_conhecidas.append(url)

    return True, "URL cadastrada com sucesso!"


def remover_url(
    url: str,
    urls_conhecidas: list[str]
) -> tuple[bool, str]:
    """Remove uma URL do arquivo e da lista em memória."""

    if not isinstance(url, str):
        return False, "URL possui formato inválido."

    url = padronizar_url(url)

    if not validar_url(url):
        return False, "URL possui formato inválido."

    if url not in urls_conhecidas:
        return False, "URL não cadastrada."

    try:
        with open(CAMINHO_URLS, "w", encoding="utf-8") as arquivo:

            for linha in urls_conhecidas:
                if linha != url:
                    arquivo.write(linha + "\n")

    except OSError:
        return False, "Não foi possível remover a URL."

    # Atualiza a lista somente depois de remover.
    urls_conhecidas.remove(url)

    return True, "URL removida com sucesso!"