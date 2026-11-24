from arvore_urls import ArvoreURLs
from urls import decompor_url


arvore : ArvoreURLs = ArvoreURLs()

dominio1 , segmentos1 = decompor_url("www.ifpb.edu.br/tsi")
dominio2 , segmentos2 = decompor_url("https://www.google.com.br/imagens")

if arvore.adicionar_dominio(dominio1):
    print(f"Dominio : {dominio1} , adicionado com sucesso\n")

if arvore.inserir_pagina(dominio1 , segmentos1):
    print(f"Pagina do Dominio {dominio1} Inserida com sucesso\n")

raiz1 = arvore.dominios[dominio1]

print(raiz1.link_esquerdo.segmento)
print(raiz1.link_esquerdo.cadastrada)
print(raiz1.link_esquerdo.conteudo_pag)

segmentos1 = ["tsi","alunos"]

if arvore.inserir_pagina(dominio1 , segmentos1):
    print(f"Pagina do Dominio {dominio1} Inserida com sucesso\n")

print(raiz1.link_esquerdo.segmento)
print(raiz1.link_esquerdo.link_esquerdo.segmento)
print(raiz1.link_esquerdo.link_esquerdo.cadastrada)

segmentos1 = ["tsi","professores"]

if arvore.inserir_pagina(dominio1 , segmentos1):
    print(f"Pagina do Dominio {dominio1} Inserida com sucesso\n")

print(raiz1.link_esquerdo.segmento)
print(raiz1.link_esquerdo.link_direito.segmento)
print(raiz1.link_esquerdo.link_direito.cadastrada)


segmentos1 = ["tsi", "coordenacao"]

if arvore.inserir_pagina(dominio1 , segmentos1):
    print(f"Pagina do Dominio {dominio1} Inserida com sucesso\n")
else:
    print("Pagina não Inserida.")


print("===================")


if arvore.adicionar_dominio(dominio2):
    print(f"Dominio : {dominio2} , adicionado com sucesso\n")

if arvore.inserir_pagina(dominio2 , segmentos2):
    print(f"Pagina do Dominio {dominio2} Inserida com sucesso\n")


raiz2 = arvore.dominios[dominio2]

print(raiz2.link_esquerdo.segmento)
print(raiz2.link_esquerdo.cadastrada)
print(raiz2.link_esquerdo.conteudo_pag)

segmentos2 = ["imagens","animais"]

if arvore.inserir_pagina(dominio2 , segmentos2):
    print(f"Pagina do Dominio {dominio2} Inserida com sucesso\n")

print(raiz2.link_esquerdo.segmento)
print(raiz2.link_esquerdo.link_esquerdo.segmento)
print(raiz2.link_esquerdo.link_esquerdo.cadastrada)

segmentos2 = ["imagens","flores"]

if arvore.inserir_pagina(dominio2 , segmentos2):
    print(f"Pagina do Dominio {dominio2} Inserida com sucesso\n")

print(raiz2.link_esquerdo.segmento)
print(raiz2.link_esquerdo.link_direito.segmento)
print(raiz2.link_esquerdo.link_direito.cadastrada)


segmentos2 = ["imagens", "TI"]

if arvore.inserir_pagina(dominio2 , segmentos2):
    print(f"Pagina do Dominio {dominio2} Inserida com sucesso\n")
else:
    print("Pagina não Inserida.")

print("-------------")
print(arvore.dominios)


print("=============")