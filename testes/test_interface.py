"""Testes unitários da interface/interfaces.py usando unittest.

Execute a partir da raiz do projeto:
    python -m unittest discover -s testes -p "test_interface.py" -v

Os testes de cadastro usam diretório temporário para os arquivos das páginas.
Não executam o navegador real nem alteram dados/urls.txt.
"""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from arvore_urls import ArvoreURLs
from historico import Historico
from paginas import ArmazenamentoPaginas, ErroPagina
from interface import interfaces


class TestResolverEntrada(unittest.TestCase):
    def test_resolve_url_completa_e_padroniza_protocolo(self):
        resultado = interfaces.resolver_entrada("http://www.ifpb.edu.br/tsi", None)
        self.assertEqual(resultado, "https://www.ifpb.edu.br/tsi")

    def test_resolve_link_interno_relativo_ao_home(self):
        home = "https://www.ifpb.edu.br/tsi"
        resultado = interfaces.resolver_entrada("/professores", home)
        self.assertEqual(resultado, "https://www.ifpb.edu.br/tsi/professores")

    def test_resolve_link_interno_com_mais_de_um_segmento(self):
        home = "https://www.ifpb.edu.br/tsi"
        resultado = interfaces.resolver_entrada("/professores/turma-a", home)
        self.assertEqual(
            resultado,
            "https://www.ifpb.edu.br/tsi/professores/turma-a",
        )

    def test_rejeita_link_interno_sem_home(self):
        with patch("builtins.print") as imprimir:
            resultado = interfaces.resolver_entrada("/tsi", None)

        self.assertIsNone(resultado)
        imprimir.assert_called()

    def test_rejeita_barra_sem_nome_de_pagina(self):
        with patch("builtins.print"):
            resultado = interfaces.resolver_entrada("/", "https://www.ifpb.edu.br")

        self.assertIsNone(resultado)

    def test_rejeita_url_com_formato_invalido(self):
        with patch("builtins.print"):
            resultado = interfaces.resolver_entrada("ftp://www.ifpb.edu.br", None)

        self.assertIsNone(resultado)

    def test_rejeita_link_interno_com_caractere_invalido(self):
        with patch("builtins.print"):
            resultado = interfaces.resolver_entrada(
                "/pagina?busca=teste",
                "https://www.ifpb.edu.br",
            )

        self.assertIsNone(resultado)


class TestLerConteudo(unittest.TestCase):
    def test_le_multiplas_linhas_ate_comando_fim(self):
        entradas = ["Primeira linha", "", "Terceira linha", "#fim"]

        with patch("builtins.input", side_effect=entradas):
            with patch("builtins.print"):
                conteudo = interfaces.ler_conteudo()

        self.assertEqual(conteudo, "Primeira linha\n\nTerceira linha")

    def test_preserva_linhas_em_branco_no_meio(self):
        with patch("builtins.input", side_effect=["A", "", "B", "#fim"]):
            with patch("builtins.print"):
                conteudo = interfaces.ler_conteudo()

        self.assertEqual(conteudo, "A\n\nB")

    def test_eof_encerra_leitura(self):
        with patch("builtins.input", side_effect=["Texto", EOFError]):
            with patch("builtins.print"):
                conteudo = interfaces.ler_conteudo()

        self.assertEqual(conteudo, "Texto")


class TestExecutarComando(unittest.TestCase):
    def setUp(self):
        self.home = "https://www.ifpb.edu.br"
        self.hist = Historico()
        self.arvore = ArvoreURLs()
        self.armazenamento = Mock(spec=ArmazenamentoPaginas)

    def executar(self, comando):
        return interfaces.executar_comando(
            comando,
            self.home,
            self.hist,
            self.arvore,
            self.armazenamento,
        )

    def test_back_retorna_ultima_pagina_do_historico(self):
        self.hist.registrar("https://www.google.com")
        self.hist.registrar("https://www.apple.com")

        resultado = self.executar("#back")

        self.assertEqual(resultado, "https://www.apple.com")
        self.assertEqual(self.hist.exibir(), ["https://www.google.com"])

    def test_back_sem_historico_mantem_home(self):
        with patch("builtins.print"):
            resultado = self.executar("#back")

        self.assertEqual(resultado, self.home)

    def test_showhist_exibe_historico(self):
        self.hist.registrar("https://www.google.com")

        with patch("builtins.print") as imprimir:
            resultado = self.executar("#showhist")

        self.assertEqual(resultado, self.home)
        mensagens = " ".join(str(chamada) for chamada in imprimir.call_args_list)
        self.assertIn("https://www.google.com", mensagens)

    def test_urls_exibe_urls_carregadas(self):
        with patch.object(
            interfaces,
            "carregar_urls",
            return_value=["https://www.ifpb.edu.br"],
        ):
            with patch("builtins.print") as imprimir:
                resultado = self.executar("#urls")

        self.assertEqual(resultado, self.home)
        mensagens = " ".join(str(chamada) for chamada in imprimir.call_args_list)
        self.assertIn("https://www.ifpb.edu.br", mensagens)

    def test_help_exibe_comandos(self):
        with patch("builtins.print") as imprimir:
            resultado = self.executar("#help")

        self.assertEqual(resultado, self.home)
        mensagens = " ".join(str(chamada) for chamada in imprimir.call_args_list)
        self.assertIn("#back", mensagens)
        self.assertIn("#add", mensagens)
        self.assertIn("#sair", mensagens)

    def test_add_chama_cadastrar_url(self):
        with patch.object(interfaces, "cadastrar_url") as cadastrar:
            resultado = self.executar("#add")

        self.assertEqual(resultado, self.home)
        cadastrar.assert_called_once_with(self.arvore, self.armazenamento)

    def test_comando_nao_tratado_mantem_home(self):
        self.assertEqual(self.executar("#comando-desconhecido"), self.home)


class TestCadastrarUrl(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.armazenamento = ArmazenamentoPaginas(
            pasta_base=Path(self.temp.name) / "paginas"
        )
        self.arvore = ArvoreURLs()

    def test_cadastra_url_e_cria_arquivo(self):
        respostas = ["www.exemplo.com", "Conteúdo da página", "#fim"]

        with patch.object(interfaces, "carregar_urls", return_value=[]):
            with patch.object(
                interfaces,
                "adicionar_url",
                return_value=(True, "URL cadastrada com sucesso!"),
            ) as adicionar:
                with patch("builtins.input", side_effect=respostas):
                    with patch("builtins.print"):
                        interfaces.cadastrar_url(self.arvore, self.armazenamento)

        adicionar.assert_called_once()
        no = self.arvore.buscar_no("www.exemplo.com", [])
        self.assertIsNotNone(no)
        self.assertTrue(no.cadastrada)
        self.assertEqual(
            self.armazenamento.ler_pagina("www.exemplo.com", []),
            "Conteúdo da página",
        )

    def test_cancelar_cadastro_nao_insere_pagina(self):
        with patch.object(interfaces, "carregar_urls", return_value=[]):
            with patch.object(interfaces, "adicionar_url") as adicionar:
                with patch("builtins.input", return_value="#cancelar"):
                    with patch("builtins.print"):
                        interfaces.cadastrar_url(self.arvore, self.armazenamento)

        adicionar.assert_not_called()
        self.assertEqual(self.arvore.dominios, {})

    def test_falha_ao_criar_arquivo_nao_deveria_persistir_url_ou_inserir_na_arvore(self):
        """Teste de regressão: atualmente expõe a ordem incorreta do #add.

        O comportamento esperado é não chamar adicionar_url nem inserir a página
        quando criar_pagina falhar. Na implementação atual, adicionar_url é
        chamada antes da criação e a árvore recebe a página com caminho None.
        """
        armazenamento = Mock(spec=ArmazenamentoPaginas)
        armazenamento.criar_pagina.side_effect = ErroPagina("falha ao criar arquivo")

        respostas = ["www.exemplo.com", "Conteúdo", "#fim"]
        with patch.object(interfaces, "carregar_urls", return_value=[]):
            with patch.object(
                interfaces,
                "adicionar_url",
                return_value=(True, "URL cadastrada com sucesso!"),
            ) as adicionar:
                with patch("builtins.input", side_effect=respostas):
                    with patch("builtins.print"):
                        interfaces.cadastrar_url(self.arvore, armazenamento)

        adicionar.assert_not_called()
        self.assertIsNone(self.arvore.buscar_no("www.exemplo.com", []))


class TestFluxoPrincipal(unittest.TestCase):
    def test_main_navega_para_link_interno_e_volta_com_back(self):
        class ArvoreFalsa:
            def pagina_cadastrada(self, dominio, segmentos):
                return True

            def listar_links(self, dominio, segmentos):
                return []

        arvore_falsa = ArvoreFalsa()
        armazenamento_falso = Mock(spec=ArmazenamentoPaginas)
        entradas = [
            "www.ifpb.edu.br",
            "/tsi",
            "#back",
            "#sair",
        ]

        with patch.object(interfaces, "montar_arvore", return_value=arvore_falsa):
            with patch.object(
                interfaces,
                "ArmazenamentoPaginas",
                return_value=armazenamento_falso,
            ):
                with patch.object(interfaces, "carregar_pagina") as carregar:
                    with patch("builtins.input", side_effect=entradas):
                        with patch("builtins.print"):
                            interfaces.main()

        urls_exibidas = [chamada.args[0] for chamada in carregar.call_args_list]
        self.assertEqual(urls_exibidas[0], None)
        self.assertIn("https://www.ifpb.edu.br/tsi", urls_exibidas)
        self.assertGreaterEqual(urls_exibidas.count("https://www.ifpb.edu.br"), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)