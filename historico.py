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
    """
    Controla o histórico de páginas anteriores usando uma pilha
    """
    def __init__(self):
        self._pilha = []
    
    def registrar(self,url:str):
        """Adiciona uma página anterior ao histórico."""
        self._pilha.append(url)

    def voltar(self) -> str | None:
        """Remove e retorna a página mais recente do histórico."""
        if not self._pilha:
            return None
        
        return self._pilha.pop()

    def exibir(self):
        """Retorna uma cópia das páginas armazenadas."""
        return self._pilha.copy()