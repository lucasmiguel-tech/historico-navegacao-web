'''
Esse arquivo verificará se as operações do histórico funcionam corretamente, 
sem precisar executar toda a interface.
---------
Conceitos: testes unitários, assert, valores esperados e testes de casos-limite.
'''



import unittest
from historico import Historico


class TestHistorico(unittest.TestCase):

    def setUp(self):
        self.historico = Historico()

    def test_historico_inicia_vazio(self):
        self.assertEqual(self.historico.exibir(), [])

    def test_registrar_pagina(self):
        self.historico.registrar("www.ifpb.edu.br")

        self.assertEqual(
            self.historico.exibir(),
            ["www.ifpb.edu.br"]
        )

    def test_voltar_retorna_ultima_pagina(self):
        self.historico.registrar("www.ifpb.edu.br")
        self.historico.registrar("www.google.com")

        pagina = self.historico.voltar()

        self.assertEqual(pagina, "www.google.com")
        self.assertEqual(
            self.historico.exibir(),
            ["www.ifpb.edu.br"]
        )

    def test_voltar_com_historico_vazio(self):
        pagina = self.historico.voltar()

        self.assertIsNone(pagina)

    def test_ordem_da_pilha(self):
        self.historico.registrar("pagina-A")
        self.historico.registrar("pagina-B")
        self.historico.registrar("pagina-C")

        self.assertEqual(self.historico.voltar(), "pagina-C")
        self.assertEqual(self.historico.voltar(), "pagina-B")
        self.assertEqual(self.historico.voltar(), "pagina-A")

    def test_exibir_nao_altera_pilha_original(self):
        self.historico.registrar("www.ifpb.edu.br")

        paginas = self.historico.exibir()
        paginas.clear()

        self.assertEqual(
            self.historico.exibir(),
            ["www.ifpb.edu.br"]
        )


if __name__ == "__main__":
    unittest.main()