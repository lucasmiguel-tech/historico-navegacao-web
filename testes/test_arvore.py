
import unittest

from arvore_urls import ArvoreURLs


class TestArvoreURLs(unittest.TestCase):

    def setUp(self):
        """Cria uma árvore nova antes de cada teste."""
        self.arvore = ArvoreURLs()
        self.dominio = "www.ifpb.edu.br"
        self.arvore.adicionar_dominio(self.dominio)

    # -----------------------------------------
    # TESTES DE DOMÍNIO
    # -----------------------------------------

    def test_adicionar_dominio(self):
        self.assertTrue(
            self.arvore.adicionar_dominio("www.google.com")
        )

    def test_adicionar_dominio_duplicado(self):
        self.assertFalse(
            self.arvore.adicionar_dominio(self.dominio)
        )

    def test_adicionar_dominio_invalido(self):
        self.assertFalse(
            self.arvore.adicionar_dominio(123)
        )

    # -----------------------------------------
    # TESTES DE BUSCA
    # -----------------------------------------

    def test_buscar_no_existente(self):
        self.arvore.inserir_pagina(
            self.dominio,
            ["tsi", "professores"]
        )

        no = self.arvore.buscar_no(
            self.dominio,
            ["tsi", "professores"]
        )

        self.assertIsNotNone(no)
        self.assertEqual(no.segmento, "professores")

    def test_buscar_no_inexistente(self):
        no = self.arvore.buscar_no(
            self.dominio,
            ["tsi", "alunos"]
        )

        self.assertIsNone(no)

    def test_buscar_dominio_inexistente(self):
        no = self.arvore.buscar_no(
            "www.inexistente.com",
            ["tsi"]
        )

        self.assertIsNone(no)

    # -----------------------------------------
    # TESTES DE CADASTRO
    # -----------------------------------------

    def test_pagina_cadastrada(self):
        self.arvore.inserir_pagina(
            self.dominio,
            ["tsi", "professores"]
        )

        self.assertTrue(
            self.arvore.pagina_cadastrada(
                self.dominio,
                ["tsi", "professores"]
            )
        )

    def test_pagina_intermediaria_nao_cadastrada(self):
        self.arvore.inserir_pagina(
            self.dominio,
            ["tsi", "professores"]
        )

        self.assertFalse(
            self.arvore.pagina_cadastrada(
                self.dominio,
                ["tsi"]
            )
        )

    def test_pagina_ja_cadastrada(self):
        self.arvore.inserir_pagina(
            self.dominio,
            ["tsi"]
        )

        self.assertFalse(
            self.arvore.verificar_insercao(
                self.dominio,
                ["tsi"]
            )
        )

    # -----------------------------------------
    # TESTES DE INSERÇÃO
    # -----------------------------------------

    def test_inserir_pagina(self):
        resultado = self.arvore.inserir_pagina(
            self.dominio,
            ["tsi", "professores"]
        )

        self.assertTrue(resultado)

    def test_inserir_pagina_com_caminho_compartilhado(self):
        self.arvore.inserir_pagina(
            self.dominio,
            ["tsi", "professores"]
        )

        resultado = self.arvore.inserir_pagina(
            self.dominio,
            ["tsi", "alunos"]
        )

        self.assertTrue(resultado)

    def test_limite_de_dois_filhos(self):
        self.arvore.inserir_pagina(
            self.dominio,
            ["tsi", "professores"]
        )

        self.arvore.inserir_pagina(
            self.dominio,
            ["tsi", "alunos"]
        )

        resultado = self.arvore.inserir_pagina(
            self.dominio,
            ["tsi", "coordenacao"]
        )

        self.assertFalse(resultado)

    def test_verificar_insercao_dominio_inexistente(self):
        self.assertFalse(
            self.arvore.verificar_insercao(
                "www.inexistente.com",
                ["tsi"]
            )
        )

    # -----------------------------------------
    # TESTES DE LINKS
    # -----------------------------------------

    def test_listar_links(self):
        self.arvore.inserir_pagina(
            self.dominio,
            ["tsi"]
        )

        self.arvore.inserir_pagina(
            self.dominio,
            ["tsi", "professores"]
        )

        self.arvore.inserir_pagina(
            self.dominio,
            ["tsi", "alunos"]
        )

        links = self.arvore.listar_links(
            self.dominio,
            ["tsi"]
        )

        self.assertEqual(
            links,
            ["/professores", "/alunos"]
        )

    def test_listar_links_pagina_inexistente(self):
        links = self.arvore.listar_links(
            self.dominio,
            ["inexistente"]
        )

        self.assertEqual(links, [])

    def test_listar_links_nao_mostra_no_intermediario(self):
        self.arvore.inserir_pagina(
            self.dominio,
            ["tsi", "professores"]
        )

        links = self.arvore.listar_links(
            self.dominio,
            []
        )

        self.assertEqual(links, [])

    # -----------------------------------------
    # TESTES DE LISTAGEM DE PÁGINAS
    # -----------------------------------------

    def test_listar_paginas_por_dominio(self):
        self.arvore.inserir_pagina(
            self.dominio,
            ["tsi"]
        )

        self.arvore.inserir_pagina(
            self.dominio,
            ["tsi", "professores"]
        )

        paginas = self.arvore.listar_paginas(
            self.dominio
        )

        self.assertEqual(
            paginas,
            [
                "https://www.ifpb.edu.br/tsi",
                "https://www.ifpb.edu.br/tsi/professores"
            ]
        )

    def test_listar_paginas_todos_os_dominios(self):
        self.arvore.inserir_pagina(
            self.dominio,
            ["tsi"]
        )

        self.arvore.adicionar_dominio("www.google.com")

        self.arvore.inserir_pagina(
            "www.google.com",
            ["pesquisa"]
        )

        paginas = self.arvore.listar_paginas()

        self.assertEqual(
            paginas,
            [
                "https://www.ifpb.edu.br/tsi",
                "https://www.google.com/pesquisa"
            ]
        )

    # -----------------------------------------
    # TESTES DE REMOÇÃO
    # -----------------------------------------

    def test_remover_pagina(self):
        self.arvore.inserir_pagina(
            self.dominio,
            ["tsi"]
        )

        resultado = self.arvore.remover_pagina(
            self.dominio,
            ["tsi"]
        )

        self.assertTrue(resultado)

        self.assertIsNone(
            self.arvore.buscar_no(
                self.dominio,
                ["tsi"]
            )
        )

    def test_remover_pagina_com_descendentes(self):
        self.arvore.inserir_pagina(
            self.dominio,
            ["tsi", "professores"]
        )

        self.arvore.inserir_pagina(
            self.dominio,
            ["rc"]
        )

        resultado = self.arvore.remover_pagina(
            self.dominio,
            ["tsi"]
        )

        self.assertTrue(resultado)

        self.assertIsNone(
            self.arvore.buscar_no(
                self.dominio,
                ["tsi", "professores"]
            )
        )

        self.assertIsNotNone(
            self.arvore.buscar_no(
                self.dominio,
                ["rc"]
            )
        )

    def test_remover_pagina_nao_cadastrada(self):
        self.arvore.inserir_pagina(
            self.dominio,
            ["tsi", "professores"]
        )

        resultado = self.arvore.remover_pagina(
            self.dominio,
            ["tsi"]
        )

        self.assertFalse(resultado)

    def test_remover_dominio(self):
        self.arvore.inserir_pagina(
            self.dominio,
            []
        )

        resultado = self.arvore.remover_pagina(
            self.dominio,
            []
        )

        self.assertTrue(resultado)
        self.assertNotIn(self.dominio, self.arvore.dominios)


if __name__ == "__main__":
    unittest.main()