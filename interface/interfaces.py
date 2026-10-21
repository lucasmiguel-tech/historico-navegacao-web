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
'''

from urls import carregar_urls, validar_url, adicionar_url
from historico import Historico

comandos = ["#back", "#showhist", "#urls", "#cmds", "#add", "#sair"]

def carregar_pagina(url: str | None) -> None:
    print("\x1b[2J", end="")

    if url is not None:
        print(f"URL: {url}")
        print("-----------------------------------\n")
        print(f"\nVocê está na página: {url}\n")
        return
    
    print("-> Digite #cmds para ver os comandos disponíveis.\n")
    print("Digite a URL que deseja acessar:")


def executar_comando(cmd: str, home: str, hist: Historico) -> None:
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

        case "#cmds":
            print("Comando disponíveis: \n")
            for i in comandos:
                print(i)

            return home

        case "#add":
            urls = carregar_urls()

            print("URLs devem começar com: 'www.', 'http://', 'https://'")
            print("Digite #cancelar para voltar à navegação.")

            while True:
                newUrl = input("\nDigite a nova URL: ").strip()

                if newUrl == "#cancelar" or not newUrl:
                    print("Cadastro cancelado.")
                    return home

                valida, msg = adicionar_url(newUrl, urls)

                print(msg)

                if valida:
                    return home


def main():
    hist = Historico()
    home = None
    redesenhar = True

    while True:

        if redesenhar:
            carregar_pagina(home)
            redesenhar = False

        entrada = input("\n> ").strip()

        if entrada.startswith("#"):
            if entrada in comandos:

                if entrada == "#sair":
                    print("Encerrando navegador...")
                    break

                pagina_anterior = home
                home = executar_comando(entrada, home, hist)

                if entrada == "#back" and home != pagina_anterior:
                    redesenhar = True

                continue

            else:
                print("\nERRO: Comando não reconhecido.")
                continue
            

        if validar_url(entrada):
            urls = carregar_urls()

            if entrada in urls:
                home = entrada
                hist.registrar(entrada)
                redesenhar = True
                continue

            print("\nERROR: URL não encontrada.")
            continue


if __name__ == "__main__":
    main()