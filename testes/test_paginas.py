'''
Testes do módulo paginas.py (armazenamento físico das páginas).

Cada teste usa uma pasta temporária, então os dados reais em
dados/paginas nunca são alterados.
'''

import tempfile
import unittest
from pathlib import Path

from paginas import (
    ArmazenamentoPaginas,
    PaginaInvalida,
    PaginaJaExiste,
    PaginaNaoEncontrada,
)
from urls import decompor_url


class TestArmazenamentoPaginas(unittest.TestCase):

    def setUp(self):
        self._temp = tempfile.TemporaryDirectory()
        self.base = Path(self._temp.name)
        self.paginas = ArmazenamentoPaginas(self.base)

    def tearDown(self):
        self._temp.cleanup()

    def test_criar_pagina_monta_estrutura_de_pastas(self):
        dominio, segmentos = decompor_url("www.ifpb.edu.br/tsi/alunos")

        arquivo = self.paginas.criar_pagina(dominio, segmentos, "Alunos do TSI")

        esperado = self.base.resolve() / "www.ifpb.edu.br" / "tsi" / "alunos" / "index.txt"
        self.assertEqual(arquivo, esperado)
        self.assertTrue(arquivo.is_file())

    def test_criar_pagina_raiz_do_dominio(self):
        arquivo = self.paginas.criar_pagina("www.ifpb.edu.br", [], "Home IFPB")

        self.assertEqual(arquivo.parent.name, "www.ifpb.edu.br")
        self.assertEqual(self.paginas.ler_pagina("www.ifpb.edu.br", []), "Home IFPB")

    def test_ler_pagina_retorna_conteudo(self):
        self.paginas.criar_pagina("www.ifpb.edu.br", ["tsi"], "Curso de TSI\nlinha 2")

        self.assertEqual(
            self.paginas.ler_pagina("www.ifpb.edu.br", ["tsi"]),
            "Curso de TSI\nlinha 2"
        )

    def test_ler_pagina_inexistente_lanca_erro(self):
        with self.assertRaises(PaginaNaoEncontrada):
            self.paginas.ler_pagina("www.ifpb.edu.br", ["rc"])

    def test_criar_pagina_existente_nao_sobrescreve(self):
        self.paginas.criar_pagina("www.ifpb.edu.br", ["tsi"], "original")

        with self.assertRaises(PaginaJaExiste):
            self.paginas.criar_pagina("www.ifpb.edu.br", ["tsi"], "outro")

        self.assertEqual(self.paginas.ler_pagina("www.ifpb.edu.br", ["tsi"]), "original")

    def test_pagina_existe(self):
        self.assertFalse(self.paginas.pagina_existe("www.ifpb.edu.br", ["tsi"]))

        self.paginas.criar_pagina("www.ifpb.edu.br", ["tsi"])

        self.assertTrue(self.paginas.pagina_existe("www.ifpb.edu.br", ["tsi"]))
        # A pasta intermediária sozinha não conta como página.
        self.assertFalse(self.paginas.pagina_existe("www.ifpb.edu.br", []))

    def test_atualizar_pagina(self):
        self.paginas.criar_pagina("www.ifpb.edu.br", ["tsi"], "antigo")

        self.paginas.atualizar_pagina("www.ifpb.edu.br", ["tsi"], "novo")

        self.assertEqual(self.paginas.ler_pagina("www.ifpb.edu.br", ["tsi"]), "novo")

    def test_atualizar_pagina_inexistente_lanca_erro(self):
        with self.assertRaises(PaginaNaoEncontrada):
            self.paginas.atualizar_pagina("www.ifpb.edu.br", ["tsi"], "novo")

    def test_remover_pagina_remove_subpaginas(self):
        self.paginas.criar_pagina("www.ifpb.edu.br", ["tsi"])
        self.paginas.criar_pagina("www.ifpb.edu.br", ["tsi", "alunos"])

        self.assertTrue(self.paginas.remover_pagina("www.ifpb.edu.br", ["tsi"]))

        self.assertFalse(self.paginas.pagina_existe("www.ifpb.edu.br", ["tsi"]))
        self.assertFalse(self.paginas.pagina_existe("www.ifpb.edu.br", ["tsi", "alunos"]))

    def test_remover_pagina_inexistente_retorna_false(self):
        self.assertFalse(self.paginas.remover_pagina("www.ifpb.edu.br", ["tsi"]))

    def test_dominio_e_segmentos_invalidos(self):
        casos = [
            ("dominio-sem-extensao", []),
            ("www.ifpb.edu.br", [".."]),
            ("www.ifpb.edu.br", ["a/b"]),
            ("www.ifpb.edu.br", ["a\\b"]),
            ("www.ifpb.edu.br", [""]),
        ]

        for dominio, segmentos in casos:
            with self.subTest(dominio=dominio, segmentos=segmentos):
                with self.assertRaises(PaginaInvalida):
                    self.paginas.criar_pagina(dominio, segmentos, "x")

    def test_listar_paginas(self):
        self.paginas.criar_pagina("www.ifpb.edu.br", [])
        self.paginas.criar_pagina("www.ifpb.edu.br", ["tsi", "alunos"])
        self.paginas.criar_pagina("www.google.com.br", ["imagens"])

        self.assertEqual(
            self.paginas.listar_paginas(),
            [
                ("www.google.com.br", ["imagens"]),
                ("www.ifpb.edu.br", []),
                ("www.ifpb.edu.br", ["tsi", "alunos"]),
            ]
        )


if __name__ == "__main__":
    unittest.main()
