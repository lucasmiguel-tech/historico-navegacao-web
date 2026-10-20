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

historico = []
home = None

def carregar_pagina(url: str | None) -> None:

    if (url != None):
        print("\x1b[2J")
        print(f"URL: {url}\n Você está na página: {url}")
        return

    print("\x1b[2J")
    print("Digite a URL que deseja acessar\n")


def executar_comando(cmd) -> None:
     match cmd:
        case "#back":
            if (len(historico) > 0):
                home = historico[len(historico) -1]
                historico.pop()
                carregar_pagina(home)
                return
            
        case "#sair":
            home = None
            carregar_pagina(home)
            return
        
        case "#showhist":
             print("Histórico: \n")
             for i in historico:
                 print(i)


def main():

    while True:
        carregar_pagina(home)

        entrada = input("> ")

        if (entrada.startswith("#") and entrada in comandos):
           executar_comando(entrada)
           return
        
        if (validar_url(entrada)):
            home = entrada
            historico.append(entrada)
            return


if __name__ == "main":
    main()