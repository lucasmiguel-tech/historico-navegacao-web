'''
Esse módulo cuidará das URLs disponíveis para navegação e das regras para adicionar novas URLs.
------------------
Conceitos de Python

    Manipulação de arquivos com open() e with.

    Leitura de linhas com readlines() ou iteração sobre o arquivo.

    Manipulação de strings com strip().

    Validação de entradas com condicionais.

    Listas para armazenar URLs e exceções para tratar falhas de leitura.
'''

from pathlib import Path


def carregar_urls() -> list:
    
    caminho = Path(__file__).parent / "dados" / "urls.txt"
    urls = []

    try:

        with open(caminho,"r",encoding="utf-8") as arq:
            for linha in arq:
                url = linha.strip()
                
                if not url:
                    continue

                if validar_url(url):
                    urls.append(url)
        
    except FileNotFoundError:
        pass
    
    except OSError as erro:
        pass

    
    return urls


def validar_url(url) -> bool:
    url = url.strip()

    #Caso de url Inválida
    if not url:
        return False
    
    #Caso de url válida
    if url.startswith("www."):
        return True
    
    if url.startswith("https//"):
        return True

    return False



def adicionar_url(url,urls):
    caminho = Path(__file__).parent / "dados" / "urls.txt"
    url = url.strip()

    if not validar_url(url):
        return False,"Url possui formato inválido"

    if url in urls:
        return False,"Url já cadastrada"
    
    try:

        with open(caminho,"a",encoding="utf-8") as arquivo:
            arquivo.write("\n" + url + "\n")
        
    except OSError as erro:
        return False,"Não foi possivel salvar a Url"

    urls.append(url)

    return True,"Url cadastrada com sucesso!"


print(carregar_urls())