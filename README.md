# Histórico de Navegação em Websites — Checkpoint 1

Projeto acadêmico desenvolvido em Python para simular a navegação entre páginas web previamente cadastradas. O programa funciona no terminal: o usuário informa uma URL, consulta as URLs disponíveis, registra páginas visitadas e executa comandos de navegação.

> **Escopo:** este README descreve os arquivos presentes na versão analisada do projeto. A aplicação é uma simulação e não realiza requisições HTTP nem carrega páginas reais da internet.

## Objetivos do Checkpoint 1

- Disponibilizar uma interface de interação por terminal.
- Carregar uma lista inicial de URLs a partir de um arquivo de texto.
- Validar o formato das URLs e permitir o cadastro de novos endereços.
- Manter em memória o histórico de páginas por meio de uma estrutura de pilha.
- Separar a interface, o gerenciamento de URLs e a lógica do histórico em módulos distintos.

## Requisitos

- Python **3.10 ou superior** (o código utiliza `match/case` e anotações como `str | None`).
- Terminal ou console integrado do Visual Studio Code.
- Não há dependências externas declaradas; o projeto usa recursos da biblioteca padrão do Python.

## Como executar

1. Faça o download ou clone o repositório e abra a pasta `historico-navegacao-web` no terminal.
2. Confira se o Python está instalado:

   ```bash
   python --version
   ```

   No Linux ou macOS, se o comando `python` não funcionar, tente `python3 --version`.

3. Execute o programa na pasta raiz do projeto:

   ```bash
   python main.py
   ```

   No Linux ou macOS, também é possível usar `python3 main.py`.

## Como utilizar

Quando o programa iniciar, digite uma URL cadastrada em `dados/urls.txt`. O endereço precisa passar pela validação de formato e estar registrado no arquivo para ser aceito para navegação.

### Comandos disponíveis

| Comando | Função |
|---|---|
| `#add` | Inicia o cadastro de uma URL. Depois de digitar o comando, informe o novo endereço quando solicitado. |
| `#cancelar` | Cancela o cadastro em andamento e retorna à navegação. É usado dentro do fluxo de `#add`. |
| `#back` | Aciona a operação de retorno do histórico. **A lógica de retorno ainda precisa de correção/validação**, conforme a observação na seção de limitações. |
| `#showhist` | Exibe as URLs armazenadas no histórico em memória. |
| `#urls` | Exibe as URLs válidas carregadas do arquivo de dados. |
| `#cmds` | Exibe a lista de comandos reconhecidos pela interface. |
| `#sair` | Encerra o programa. |

Para cadastrar uma URL, execute `#add` e digite o endereço no prompt apresentado. O código aceita endereços iniciados por `www.`, `http://` ou `https://`, desde que passem pela validação. O cadastro é persistido em `dados/urls.txt`.

## Estrutura do projeto

```text
historico-navegacao-web/
├── main.py                    # Ponto de entrada; chama a interface
├── interface/
│   ├── __init__.py             # Inicializador do pacote
│   └── interfaces.py           # Interface do terminal e interpretação dos comandos
├── historico.py                # Classe Historico e operações da pilha
├── urls.py                     # Carregamento, validação e cadastro de URLs
├── dados/
│   ├── urls.txt                # Arquivo de URLs cadastradas
│   └── urls_informacoes.py     # Arquivo presente, ainda vazio/não utilizado
├── testes/
│   ├── test_historico.py       # Testes unitários da classe Historico
│   └── test_urls.py            # Verificações simples do cadastro de URLs
└── README.md
```

## Organização dos módulos

- **`main.py`**: importa e executa a função `main()` da interface.
- **`interface/interfaces.py`**: apresenta a interface de terminal, recebe entradas, reconhece os comandos e conecta a interface às funções de URLs e à classe `Historico`.
- **`urls.py`**: define o caminho de `dados/urls.txt`, carrega endereços válidos sem repetir linhas idênticas, verifica o formato básico e grava novos endereços.
- **`historico.py`**: implementa a classe `Historico`, que usa uma lista como pilha. `registrar()` adiciona um endereço, `voltar()` retira e retorna o elemento do topo e `exibir()` retorna uma cópia da lista.
- **`dados/urls.txt`**: fornece a lista inicial de URLs reconhecidas pela simulação.
- **`testes/`**: contém verificações da estrutura do histórico e do comportamento de URLs já cadastradas.

## Testes

Na raiz do projeto, execute:

```bash
python -m unittest discover -s testes -v
```

O comando executa os seis testes unitários de `test_historico.py`. O arquivo `test_urls.py` também realiza verificações por `assert` quando é carregado pela descoberta de testes. Atualmente, essas verificações de URLs são limitadas: não formam uma suíte abrangente de testes unitários e não cobrem todos os casos descritos nos comentários do próprio arquivo.

## Estrutura de dados: histórico em pilha

A classe `Historico` armazena as URLs em uma pilha baseada em lista do Python. Uma pilha segue o princípio **LIFO** (*Last In, First Out*): o último elemento inserido é o primeiro a ser removido. No código atual:

- `registrar(url)` usa `append()` para adicionar uma URL;
- `voltar()` usa `pop()` para remover e retornar a URL mais recente, ou retorna `None` quando a pilha está vazia;
- `exibir()` retorna uma cópia da pilha, evitando que a lista interna seja alterada diretamente pela interface.

## Limitações conhecidas nesta versão

- **`#back` precisa de ajuste:** a interface registra a URL informada ao acessar uma página e, no retorno, retira o elemento mais recente da pilha. Dessa forma, pode devolver a própria página atual, em vez da página visitada anteriormente. A operação deve ser corrigida e testada antes de ser apresentada como retorno de navegação concluído.
- **Histórico em memória:** as páginas do histórico não são salvas em arquivo; o histórico é reiniciado ao encerrar e iniciar o programa.
- **Páginas reais e páginas internas:** a aplicação não faz acesso HTTP nem implementa, nesta versão, a navegação entre páginas internas com caminhos como `/tsi`.
- **Testes de URLs:** há verificações básicas de duplicidade, mas ainda faltam testes automatizados abrangentes para formato válido/inválido, gravação de uma URL nova e tratamento de erros de arquivo.

## Próximas etapas

Para fortalecer a entrega, recomenda-se corrigir e testar o comando `#back`, ampliar os testes de `urls.py` e verificar o comportamento da interface com entradas válidas, inválidas e comandos desconhecidos. Funcionalidades previstas para etapas posteriores, como `#help` e conteúdo associado a páginas internas, devem ser documentadas quando estiverem efetivamente implementadas.

## Informações acadêmicas

- **Disciplina:** Programação e Estrutura de Dados (PED)
- **Curso:** Redes de Computadores
- **Professor:** Wallennon Germano
- **Etapa:** Checkpoint 1
- **Integrantes:** Lucas Miguel e Ronaldo Firmino
