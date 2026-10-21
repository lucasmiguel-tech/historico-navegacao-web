
"""
Gerencia as URLs disponíveis para navegação.

Responsabilidades:
- Carregar URLs de dados/urls.txt.
- Validar o formato das URLs.
- Cadastrar novas URLs no arquivo.
"""

from pathlib import Path
from urllib.parse import urlsplit


CAMINHO_URLS = Path(__file__).parent / "dados" / "urls.txt"


def carregar_urls() -> list[str]:
    """Carrega as URLs cadastradas no arquivo."""
    urls = []

    try:
        with open(CAMINHO_URLS, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                url = linha.strip()

                if url and validar_url(url) and url not in urls:
                    urls.append(url)

    except FileNotFoundError:
        # O arquivo ainda não existe.
        return []

    except OSError as erro:
        raise RuntimeError(
            f"Erro ao ler o arquivo de URLs: {erro}"
        ) from erro

    return urls


def validar_url(url: str) -> bool:
    """Verifica se a URL possui um formato básico válido."""
    url = url.strip()

    if not url or any(caractere.isspace() for caractere in url):
        return False

    # Permite endereços como www.ifpb.edu.br.
    if url.startswith("www."):
        url = "https://" + url

    try:
        partes = urlsplit(url)

        if partes.scheme not in ("http", "https"):
            return False

        dominio = partes.hostname

        if not dominio or "." not in dominio:
            return False

        # Evita domínios com pontos vazios nas extremidades.
        if dominio.startswith(".") or dominio.endswith("."):
            return False

        # Acessar .port também identifica portas malformadas.
        _ = partes.port

        return True

    except ValueError:
        return False


def adicionar_url(
    url: str,
    urls_conhecidas: list[str]
) -> tuple[bool, str]:
    """Valida, salva e adiciona uma URL à lista em memória."""
    url = url.strip()

    if not validar_url(url):
        return False, "URL possui formato inválido."

    if url in urls_conhecidas:
        return False, "URL já cadastrada."

    try:
        with open(CAMINHO_URLS, "a+", encoding="utf-8") as arquivo:
            arquivo.seek(0, 2)
            arquivo.seek(arquivo.tell() - 1) if arquivo.tell() else None
            ultimo_caractere = arquivo.read() if arquivo.tell() else ""

            arquivo.seek(0, 2)

            if arquivo.tell() > 0 and ultimo_caractere != "\n":
                arquivo.write("\n")

            arquivo.write(url + "\n")

    except OSError:
        return False, "Não foi possível salvar a URL."

    # Atualiza a lista somente depois de salvar no arquivo.
    urls_conhecidas.append(url)

    return True, "URL cadastrada com sucesso!"