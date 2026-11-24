'''
Esse arquivo verificará o carregamento e a validação das URLs.

Conceitos: testes unitários, assert, validação e arquivos de teste.

Os testes devem verificar:
1. Se as URLs do arquivo são carregadas.
2. Se linhas vazias são ignoradas.
3. Se uma URL válida é aceita.
4. Se uma entrada inválida é rejeitada.
5. Se a política de duplicatas funciona como foi definida.
6. Se uma falha na leitura do arquivo é tratada adequadamente.
'''

# from urls import carregar_urls,validar_url
# # from paginas import verificar_dominio
# #from arvore_urls import NoPagina

# urls = carregar_urls()

# # for dominio in paginas:
# #     print(verificar_dominio(dominio)

# for url in urls:
#     if validar_url(url):
#         print(f"{url} é válida")


from urls import validar_url , decompor_url , carregar_urls , adicionar_url , remover_url


print(decompor_url("https://www.ifpb.edu.br"))
print(validar_url("https://www.ifpb.edu.br"))


rotulo = "www.ifpb.edu.br".split(".")