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

from urls import adicionar_url,carregar_urls

urls_cadastradas = carregar_urls()

sucesso,mensagem = adicionar_url(
    "www.firefox.com.br",
    urls_cadastradas
)

assert sucesso is False
print(mensagem)

sucesso,mensagem = adicionar_url(
    "www.ifpb.edu.br",
    urls_cadastradas
)

assert sucesso is False
print(mensagem)