''' 
Esse módulo será responsável pela lógica do histórico. 
Ele não deve receber comandos diretamente do teclado nem imprimir mensagens da interface; 
deve fornecer funções ou métodos que main.py possa chamar.
-----------------------------------------
Conceitos de Python e Estrutura de Dados
- Pilha (Stack): estrutura LIFO — o último elemento inserido é o primeiro a sair.
- Lista (list): pode representar a pilha por meio de append() e pop().
- Encapsulamento: manter as operações do histórico reunidas em uma classe ou módulo.
- Condicionais: verificar se há páginas anteriores antes de voltar.
- Exceções e casos-limite: evitar erros quando o histórico estiver vazio.
'''

class Historico:
    def __init__(self):
        self.pilha = []
    
    def url_digitada(self,url):
        self.pilha.append(url)

    def voltar(self):
        if not self.pilha:
            return None
        
        return self.pilha.pop()

    def exibir(self):
        return 