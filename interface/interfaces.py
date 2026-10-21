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

comandos = ["#back", "#showhist", "#urls", "#add", "#sair"]

def carregar_pagina(url: str | None) -> None:
    print("\x1b[2J", end="")

    if url is not None:
        print(f"URL: {url}")
        print("-----------------------------------\n")
        print(f"\nVocê está na página: {url}\n")
        return

    print("Digite a URL que deseja acessar\n")


def executar_comando(cmd: str, home: str, hist: list) -> None:
     match cmd:
        case "#back":
            if (len(hist) > 1):
                hist.pop()
                return hist[-1]

            return home
            
        case "#sair":
            hist.clear()
            home = None

            return home
        
        case "#showhist":
            print("Histórico: \n\n")
            for i in reversed(hist):
                print(i)

            return home

        case "#urls":
            print("URLs registradas: \n\n")
            urls = carregar_urls()
            for i in urls:
                print(i)

            return home

        case "#add":
            urls = carregar_urls()
            
            print("URLs devem começar com um dos seguintes: 'www.', 'http://', 'https://'")
            while True:
                newUrl = input("\nDigite a nova URL: ")
                valida, msg = adicionar_url(newUrl, urls)

                if not valida:
                    print(msg)
                    continue

                print(msg)
                break

            return home


def main():
    hist = []
    home = None
    redesenhar = True

    while True:

        if redesenhar:
            carregar_pagina(home)
            redesenhar = False

        entrada = input("\n> ")

        if entrada.startswith("#"):
            if entrada in comandos:

                if entrada == "#sair":
                    print("Encerrando navegador...")
                    break

                home = executar_comando(entrada, home, hist)

                if entrada == "#back":
                    redesenhar = True

                continue

            else:
                print("ERRO: Comando não reconhecido.")
                continue
            

        if validar_url(entrada):
            home = entrada
            hist.append(entrada)
            redesenhar = True
            continue


if __name__ == "__main__":
    main()