# Histórico de Navegação em Websites — Checkpoint 2

Projeto acadêmico desenvolvido em Python para simular a navegação entre websites previamente cadastrados. A aplicação funciona pelo terminal e permite acessar páginas, navegar por links internos, consultar o histórico de visitas e cadastrar novos endereços com conteúdo próprio.

> **Importante:** este projeto é uma simulação de navegador. Ele não realiza requisições HTTP/HTTPS, não consulta servidores DNS e não acessa páginas reais da internet. Os endereços e seus conteúdos são mantidos localmente em arquivos de texto.

## Sobre o projeto

O objetivo é representar, por meio de estruturas de dados, o funcionamento básico de um navegador. Cada domínio cadastrado pode possuir páginas internas, e cada página válida está associada a um arquivo `index.txt`, cujo conteúdo é exibido quando ela é acessada.

O projeto foi desenvolvido em etapas. O Checkpoint 1 contemplou a interface inicial, o cadastro e a validação de URLs e o histórico de navegação. O Checkpoint 2 amplia a aplicação com a representação dos domínios e das páginas internas por uma árvore binária, a navegação por caminhos iniciados em `/`, o cadastro de páginas internas e a exibição do conteúdo armazenado em arquivos.

## Funcionalidades

- Carregar as URLs iniciais a partir de `dados/urls.txt`.
- Padronizar URLs para utilizar HTTPS como protocolo canônico. Endereços informados sem protocolo ou com HTTP são normalizados para HTTPS.
- Validar domínios, URLs e segmentos dos caminhos internos.
- Representar os domínios e suas páginas internas em uma árvore binária.
- Limitar a dois links internos diretos por página, conforme as regras do projeto. A árvore pode possuir vários níveis de profundidade.
- Acessar uma URL completa previamente cadastrada.
- Acessar páginas internas digitando um caminho iniciado por `/`, relativo à página que está sendo exibida.
- Associar cada página válida a um arquivo `index.txt` e exibir seu conteúdo na tela.
- Cadastrar manualmente novos domínios e páginas internas por meio do comando `#add`.
- Registrar as páginas anteriores em um histórico implementado como pilha.
- Consultar as páginas armazenadas no histórico e retornar à página anterior.

## Requisitos

- **Python 3.10 ou superior.** O código utiliza `match/case` e anotações de tipo como `str | None`.
- Terminal ou console integrado do Visual Studio Code.
- Não há dependências externas necessárias; a aplicação utiliza módulos da biblioteca padrão do Python.

## Como obter e executar o projeto

Clone o repositório e acesse a pasta do projeto:

```bash
git clone <URL_DO_REPOSITORIO>
cd historico-navegacao-web
```

Confira a versão do Python instalada:

```bash
python --version
```

### Ambiente virtual (opcional, recomendado)

No Windows, crie e ative o ambiente virtual com:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

No Linux ou macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Como o projeto não possui dependências externas, não é necessário instalar pacotes com `pip`.

### Inicialização

Na pasta raiz do projeto, execute:

```bash
python main.py
```

No Linux ou macOS, caso o comando `python` não esteja associado ao Python 3, utilize:

```bash
python3 main.py
```

## Como utilizar

Ao iniciar, a aplicação carrega as URLs cadastradas em `dados/urls.txt` e monta a estrutura de navegação. Para acessar uma página, digite sua URL completa, desde que esteja cadastrada e passe pela validação.

Exemplo de acesso a um domínio:

```text
www.ifpb.edu.br
```

Quando a página for encontrada, a aplicação exibe o endereço atual, o conteúdo do seu arquivo `index.txt` e os links internos cadastrados para aquela página.

### Navegação por páginas internas

Para acessar uma página interna, digite `/` seguido do caminho apresentado entre os links disponíveis. O caminho é interpretado em relação à página atualmente aberta.

Exemplo de navegação:

```text
URL atual: www.ifpb.edu.br
Entrada:   /tsi
Resultado: https://www.ifpb.edu.br/tsi

URL atual: www.ifpb.edu.br/tsi
Entrada:   /professores
Resultado: https://www.ifpb.edu.br/tsi/professores
```

Também é possível informar diretamente uma URL completa com o caminho interno, desde que a página esteja cadastrada.

### Comandos disponíveis

| Comando | Descrição |
|---|---|
| `#help` | Exibe a ajuda com os comandos disponíveis e orientações de navegação. |
| `#add` | Inicia o cadastro de um domínio ou de uma página interna e solicita o conteúdo da página. |
| `#back` | Retorna à página anterior registrada no histórico. |
| `#showhist` | Exibe as páginas armazenadas no histórico de navegação. |
| `#urls` | Lista as URLs cadastradas em `dados/urls.txt`. |
| `#recarregar` | Limpa a tela e exibe novamente a página atual. |
| `#sair` | Encerra a aplicação. |

Durante o fluxo de cadastro iniciado por `#add`, o comando `#cancelar` interrompe o cadastro e retorna à navegação.

### Cadastro de páginas

1. Digite `#add`.
2. Informe a URL do domínio ou o endereço completo da página interna.
3. Digite o conteúdo que será armazenado no arquivo `index.txt`.
4. Para finalizar a entrada do conteúdo, digite `#fim` sozinho em uma linha.

O cadastro respeita o limite de dois links internos diretos por página. URLs e páginas que não passam pela validação ou que não podem ser inseridas na estrutura são rejeitadas pela aplicação.

## Organização dos dados

As URLs cadastradas são mantidas em `dados/urls.txt`. O conteúdo de cada página fica em um arquivo `index.txt`, organizado em diretórios que representam o domínio e os segmentos do caminho.

Exemplo simplificado:

```text
dados/
├── urls.txt
└── paginas/
    └── www.ifpb.edu.br/
        ├── index.txt
        └── tsi/
            ├── index.txt
            ├── professores/
            │   └── index.txt
            └── alunos/
                └── index.txt
```

Assim, a página `https://www.ifpb.edu.br/tsi/professores` corresponde ao arquivo:

```text
dados/paginas/www.ifpb.edu.br/tsi/professores/index.txt
```

A estrutura de diretórios é gerenciada pelo módulo `paginas.py`. O cadastro de uma URL no arquivo `urls.txt` e o arquivo de conteúdo da página são responsabilidades distintas, coordenadas pela interface.

## Estrutura do projeto

```text
historico-navegacao-web/
├── main.py
├── arvore_urls.py
├── historico.py
├── paginas.py
├── urls.py
├── interface/
│   ├── __init__.py
│   └── interfaces.py
├── dados/
│   ├── urls.txt
│   └── paginas/
│       └── <dominio>/<caminho>/index.txt
├── testes/
│   ├── test_arvore.py
│   ├── test_historico.py
│   ├── test_interface.py
│   ├── test_paginas.py
│   └── test_urls.py
├── .gitignore
└── README.md
```

Os diretórios dentro de `dados/paginas/` variam conforme os domínios e as páginas cadastradas.

## Organização dos módulos

| Módulo | Responsabilidade |
|---|---|
| `main.py` | Ponto de entrada da aplicação. Importa e executa a função principal da interface. |
| `interface/interfaces.py` | Controla o ciclo de interação com o usuário, interpreta entradas, executa comandos e coordena os demais módulos. |
| `urls.py` | Padroniza, valida, decompõe e monta URLs; carrega, cadastra e remove endereços no arquivo `dados/urls.txt`. |
| `arvore_urls.py` | Implementa `NoPagina` e `ArvoreURLs`, representando os domínios e as páginas internas por uma árvore binária. |
| `paginas.py` | Implementa `ArmazenamentoPaginas`, responsável por criar, consultar, ler, atualizar e remover os arquivos e diretórios das páginas. |
| `historico.py` | Implementa a classe `Historico`, que mantém as páginas anteriores em uma pilha. |
| `dados/urls.txt` | Arquivo de texto com a lista inicial e persistida de URLs cadastradas. |
| `dados/paginas/` | Diretório que armazena o conteúdo das páginas em arquivos `index.txt`. |
| `testes/` | Reúne os testes automatizados dos módulos do projeto. |

## Estruturas de dados utilizadas

### Árvore binária para domínios e páginas internas

A classe `ArvoreURLs` mantém um dicionário de domínios. Cada domínio cadastrado funciona como raiz de uma árvore de páginas. Os caminhos internos são representados por nós da classe `NoPagina`, que armazenam o segmento correspondente, referências para os filhos esquerdo e direito, o estado de cadastro e o caminho do arquivo de conteúdo associado.

Cada nó pode possuir no máximo dois filhos, representando os dois links internos diretos permitidos por página. Os níveis da árvore representam a continuação dos caminhos internos. Nós intermediários podem ser utilizados para formar caminhos mais profundos, mesmo quando não representam uma página cadastrada de forma independente.

### Pilha para o histórico de navegação

A classe `Historico` utiliza uma lista do Python como pilha, seguindo o princípio **LIFO** (*Last In, First Out*): o último endereço registrado é o primeiro a ser recuperado no retorno.

- `registrar(url)`: adiciona ao histórico a página que estava aberta antes da navegação.
- `voltar()`: remove e retorna a página mais recente do histórico; retorna `None` quando não há página anterior.
- `exibir()`: retorna uma cópia da lista de páginas armazenadas.

O histórico é mantido em memória durante a execução e não é persistido após o encerramento do programa.

## Testes

Os testes automatizados utilizam o módulo `unittest`, integrante da biblioteca padrão do Python. Para executar os testes a partir da pasta raiz do projeto:

```bash
python -m unittest discover -s testes -v
```

O comando procura e executa os testes dos arquivos `test_*.py` que estejam na pasta `testes/`.

## Regras e decisões de implementação

- **Protocolo canônico:** as URLs são normalizadas para HTTPS antes da validação, comparação, armazenamento e decomposição.
- **Domínio único na árvore:** cada domínio possui uma única raiz na estrutura de navegação.
- **Limite de links:** cada página pode ter no máximo dois links internos diretos, mas não há limite de profundidade definido por essa regra.
- **Conteúdo local:** cada página válida está associada a um arquivo de texto `index.txt`.
- **Navegação interna:** entradas iniciadas por `/` são interpretadas como caminhos internos relativos à página atual.
- **Separação de responsabilidades:** a interface coordena a aplicação; a árvore representa as relações entre páginas; `paginas.py` administra os arquivos; `urls.py` cuida da validação e persistência das URLs; e `historico.py` gerencia a pilha de navegação.

## Informações acadêmicas

- **Curso:** Redes de Computadores
- **Disciplina:** Programação e Estrutura de Dados
- **Professor:** Wallennon Germano
- **Projeto:** Histórico de Navegação em Websites
- **Etapa:** Checkpoint 2
- **Integrantes:** Lucas Miguel e Ronaldo Firmino