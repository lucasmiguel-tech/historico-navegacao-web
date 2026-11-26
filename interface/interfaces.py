'''
Esse será o ponto de entrada do programa.
É aqui que o usuário verá o navegador simulado e digitará os comandos.

Conceitos de Python
- Entrada e saída com input() e print().
- Laços de repetição com while.
- Condicionais com if, elif e else.
- Modularização com import.
- Manipulação de strings.
- Tratamento de exceções e mensagens de erro.

Módulos utilizados
- urls.py        -> valida, padroniza e decompõe URLs; persiste dados/urls.txt.
- arvore_urls.py -> estrutura de dados (árvore) com domínios e páginas internas.
- paginas.py     -> arquivos index.txt com o conteúdo de cada página.
- historico.py   -> pilha com as páginas visitadas.
'''

from urls import (
    carregar_urls,
    validar_url,
    adicionar_url,
    remover_url,
    padronizar_url,
    decompor_url,
    montar_url,
)
from historico import Historico
from arvore_urls import ArvoreURLs
from paginas import ArmazenamentoPaginas, ErroPagina, PaginaJaExiste

"""
Dicionário dos comandos internos e suas funcionalidades.
"""
comandos = {
    "#back" : "Voltar para a página anterior.",
    "#showhist" : "Listar o histórico de páginas visitadas.",
    "#urls" : "Listar as urls cadastradas no arquivo .txt.",
    "#help" : "Listar os comandos disponiveis e suas funções.",
    "#add" : "Cadastrar uma nova url (domínio ou página interna) e o seu conteúdo.",
    "#recarregar" : "Limpar o terminal e exibir novamente a página atual.",
    "#sair" : "Encerrar o navegador.",
}


# ----- MONTAGEM DA ÁRVORE -----
def montar_arvore(armazenamento: ArmazenamentoPaginas) -> ArvoreURLs:
    """
    Cria a árvore a partir de dados/urls.txt e garante que cada URL
    cadastrada tenha o seu arquivo index.txt em disco.
    """
    arvore = ArvoreURLs()

    for url in carregar_urls():
        dominio, segmentos = decompor_url(url)

        arvore.adicionar_dominio(dominio)  # Ignorado se o domínio já existe.

        # Verifica se a página pode ser inserida na árvore.
        if not arvore.verificar_insercao(dominio, segmentos):
            print(
                f"AVISO: '{url}' ignorada "
                "(repetida ou limite de dois links atingido)."
            )
            continue

        try:
            if not armazenamento.pagina_existe(dominio, segmentos):
                armazenamento.criar_pagina(
                    dominio, segmentos, f"Página {url} (sem conteúdo cadastrado)."
                )

            caminho = armazenamento.caminho_arquivo(dominio, segmentos)

        except ErroPagina as erro:
            print(f"AVISO: {erro}")
            continue

        if not arvore.inserir_pagina(dominio, segmentos, caminho):
            print(f"AVISO: Não foi possível inserir a url na árvore.")

    return arvore


# ----- TELA -----
def carregar_pagina(
    url: str | None,
    hist: Historico,
    arvore: ArvoreURLs,
    armazenamento: ArmazenamentoPaginas
) -> None:
    # Limpa a tela (2J) sem mover o cursor: o conteúdo antigo é empurrado
    # para longe no histórico de rolagem e a página nova aparece embaixo.
    print("\x1b[2J", end="")

    if url is None:
        print("-> Digite #help para ver os comandos disponíveis.\n")
        print("Digite a URL que deseja acessar:")
        return

    dominio, segmentos = decompor_url(url)

    print(f"Páginas Visitadas: [{', '.join(hist.exibir())}]") #exibe o histórico de páginas.
    print(f"Home: [{url}]")
    print("-----------------------------------")
    print("Digite a url ou digite #back para retornar à última página visitada.")
    print("\nPágina encontrada!\n")

    # Conteúdo da página, no padrão "url: <endereço>" + texto livre.
    print(f"url: {url}\n")

    try:
        print(armazenamento.ler_pagina(dominio, segmentos))
    except ErroPagina as erro:
        print(f"(Não foi possível exibir o conteúdo: {erro})")

    links = arvore.listar_links(dominio, segmentos)

    print("\nLinks disponíveis:\n")

    if not links:
        print("(nenhum link interno)")

    for link in links:
        print(link)

    print("-"*15)


# ----- NAVEGAÇÃO -----
def resolver_entrada(entrada: str, home: str | None) -> str | None:
    """
    Converte o que foi digitado em uma URL padronizada.

    Entradas iniciadas por "/" são páginas internas do domínio atual (home).
    Retorna None se a entrada não puder virar uma URL válida.
    """
    if entrada.startswith("/"):
        if home is None:
            print("\nERRO: Acesse um domínio antes de usar um link interno (/pagina).")
            return None

        dominio, segmentos = decompor_url(home)
        novos = [segmento for segmento in entrada.split("/") if segmento]

        if not novos:
            print("\nERRO: Informe a página interna. Ex.: /tsi")
            return None

        entrada = montar_url(dominio, segmentos + novos)

    entrada = padronizar_url(entrada)

    if not validar_url(entrada):
        print("\nERRO: URL possui formato inválido.")
        return None

    # Forma canônica (remove barras finais, etc.) para comparar URLs.
    return montar_url(*decompor_url(entrada))


# ----- COMANDOS -----
FIM_CONTEUDO = "#fim"


def ler_conteudo() -> str:
    """
    Lê várias linhas digitadas pelo usuário.

    Linhas vazias fazem parte do texto (permitem separar parágrafos).
    A leitura termina com uma linha contendo apenas #fim ou com EOF
    (Ctrl+Z + Enter no Windows, Ctrl+D no Linux/macOS).
    """
    print(f"Digite o conteúdo da página. Para terminar, digite {FIM_CONTEUDO} em uma linha sozinha.")

    linhas = []

    while True:
        try:
            linha = input()
        except EOFError:
            break

        if linha.strip() == FIM_CONTEUDO:
            break

        linhas.append(linha)

    # Remove linhas vazias sobrando no fim do texto.
    return "\n".join(linhas).rstrip("\n")


def cadastrar_url(arvore: ArvoreURLs, armazenamento: ArmazenamentoPaginas) -> None:
    """Fluxo do #add: cadastra a URL na árvore, no urls.txt e cria o index.txt."""
    urls = carregar_urls()

    print("URLs devem começar com: 'www.', 'http://', 'https://'")
    print("Páginas internas usam '/'. Ex.: www.ifpb.edu.br/tsi/alunos")
    print("Cada página pode ter no máximo 2 links internos.")
    print("Digite #cancelar para voltar à navegação.")

    while True:
        nova_url = input("\nDigite a nova URL: ").strip()

        if nova_url == "#cancelar" or not nova_url:
            print("Cadastro cancelado.")
            return

        nova_url = padronizar_url(nova_url)

        if not validar_url(nova_url):
            print("URL possui formato inválido.")
            continue

        dominio, segmentos = decompor_url(nova_url)
        nova_url = montar_url(dominio, segmentos)



        # Verifica se o domínio já existe na árvore.
        dominio_novo = dominio not in arvore.dominios

        if dominio_novo:
            arvore.adicionar_dominio(dominio)

        # Verifica se a página pode ser inserida.
        if not arvore.verificar_insercao(dominio, segmentos):
            print(
                "Não é possível cadastrar: a URL já existe "
                "ou a página pai já possui 2 links."
            )

            if dominio_novo:
                arvore.dominios.pop(dominio, None)

            continue

        conteudo = ler_conteudo()

        # ETAPA 1: Criar o arquivo da página.
        arquivo_criado = False

        try:
            caminho = armazenamento.criar_pagina(
                dominio,
                segmentos,
                conteudo
            )
            arquivo_criado = True

        except PaginaJaExiste:
            # Não apaga nem sobrescreve um arquivo que já existia.
            caminho = armazenamento.caminho_arquivo(
                dominio,
                segmentos
            )
            print(
                "Já havia um arquivo para esta página; "
                "o conteúdo existente foi mantido."
            )

        except ErroPagina as erro:
            print(f"AVISO: {erro}")

            if dominio_novo:
                arvore.dominios.pop(dominio, None)

            continue

        # ETAPA 2: Registrar a URL no arquivo urls.txt.
        valida, msg = adicionar_url(nova_url, urls)

        if not valida:
            print(msg)

            # Desfaz a criação do arquivo, se ele foi criado agora.
            if arquivo_criado:
                try:
                    caminho.unlink()
                except OSError as erro:
                    print(f"AVISO: Não foi possível desfazer o arquivo: {erro}")

            if dominio_novo:
                arvore.dominios.pop(dominio, None)

            continue

        # ETAPA 3: Inserir a página na árvore.
        inserida = arvore.inserir_pagina(
            dominio,
            segmentos,
            caminho
        )

        if not inserida:
            print("Não foi possível inserir a página na árvore.")

            # Desfaz o registro no arquivo urls.txt.
            removida, mensagem = remover_url(nova_url, urls)

            if not removida:
                print(f"AVISO: Não foi possível desfazer o cadastro: {mensagem}")

            # Remove somente o arquivo criado nesta operação.
            if arquivo_criado:
                try:
                    caminho.unlink()
                except OSError as erro:
                    print(f"AVISO: Não foi possível remover o arquivo: {erro}")

            if dominio_novo:
                arvore.dominios.pop(dominio, None)

            continue

        print(msg)
        return

def executar_comando(
    cmd: str,
    home: str | None,
    hist: Historico,
    arvore: ArvoreURLs,
    armazenamento: ArmazenamentoPaginas
) -> str | None:
     match cmd:
        case "#back":
            anterior = hist.voltar()

            if anterior is None:
                print("Não há página anterior.")
                return home

            return anterior

        case "#showhist":
            print("Histórico:\n")

            paginas = hist.exibir()

            if not paginas:
                print("Histórico vazio.")

            for url in paginas:
                print(url)

            return home

        case "#urls":
            print("URLs registradas: \n")
            urls = carregar_urls()
            for i in urls:
                print(i)

            return home

        case "#help":
            print("Comando disponíveis: \n")
            for comando,funcionalidade in comandos.items():
                print(f"{comando} -> {funcionalidade}")

            print("\nNavegação:")
            print("www.site.com.br -> Acessar uma URL cadastrada.")
            print("/pagina         -> Acessar uma página interna do domínio atual. Ex.: /tsi")

            return home

        case "#add":
            cadastrar_url(arvore, armazenamento)
            return home

     return home


def main():
    hist = Historico()
    home = None
    redesenhar = True

    armazenamento = ArmazenamentoPaginas()
    arvore = montar_arvore(armazenamento)

    while True:

        if redesenhar:
            carregar_pagina(home, hist, arvore, armazenamento)
            redesenhar = False

        try:
            entrada = input("\nurl -> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando navegador...")
            break

        if not entrada:
            continue

        #Se entrada é um comando interno
        if entrada.startswith("#"):
            if entrada in comandos:

                if entrada == "#sair":
                    print("Encerrando navegador...")
                    break

                # Redesenha a tela; o conteúdo é lido de novo do index.txt.
                if entrada == "#recarregar":
                    redesenhar = True
                    continue

                pagina_anterior = home
                home = executar_comando(entrada, home, hist, arvore, armazenamento)

                if entrada == "#back" and home != pagina_anterior:
                    redesenhar = True

                continue

            else:
                print("\nERRO: Comando não reconhecido.")
                continue

        #Se entrada é uma URL (completa ou interna, iniciada por "/")
        url = resolver_entrada(entrada, home)

        if url is None:
            continue

        dominio, segmentos = decompor_url(url)

        if not arvore.pagina_cadastrada(dominio, segmentos):
            print("\nERRO 404: Página não encontrada.")
            continue

        if url == home:
            print("\nERRO: URL já está sendo acessada!")
            continue

        hist.registrar(home)
        home = url
        redesenhar = True


if __name__ == "__main__":
    main()
