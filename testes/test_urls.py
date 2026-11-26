"""Testes unitários do módulo urls.py usando unittest.

Execute a partir da raiz do projeto:
    python -m unittest discover -s testes -p "test_urls.py" -v

Os testes substituem CAMINHO_URLS por um arquivo temporário, portanto
não alteram o arquivo dados/urls.txt utilizado pela aplicação.
"""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import urls


class TestPadronizacaoEValidacao(unittest.TestCase):
    def test_padronizar_url_sem_protocolo(self):
        self.assertEqual(
            urls.padronizar_url("www.ifpb.edu.br"),
            "https://www.ifpb.edu.br",
        )

    def test_padronizar_url_converte_http_para_https(self):
        self.assertEqual(
            urls.padronizar_url("http://www.ifpb.edu.br/tsi"),
            "https://www.ifpb.edu.br/tsi",
        )

    def test_padronizar_url_remove_espacos_externos(self):
        self.assertEqual(
            urls.padronizar_url("  www.ifpb.edu.br  "),
            "https://www.ifpb.edu.br",
        )

    def test_padronizar_url_preserva_protocolo_nao_suportado(self):
        self.assertEqual(
            urls.padronizar_url("ftp://www.ifpb.edu.br"),
            "ftp://www.ifpb.edu.br",
        )

    def test_validar_rotulo_valido(self):
        for rotulo in ("www", "ifpb", "ifpb-edu", "123abc"):
            with self.subTest(rotulo=rotulo):
                self.assertTrue(urls.validar_rotulo(rotulo))

    def test_validar_rotulo_invalido(self):
        for rotulo in ("", "-ifpb", "ifpb-", "ifpb edu", "área", "a" * 64):
            with self.subTest(rotulo=rotulo):
                self.assertFalse(urls.validar_rotulo(rotulo))

    def test_validar_dominio_valido(self):
        for dominio in (
            "www.ifpb.edu.br",
            "google.com",
            "site.com.br",
            "subdominio.exemplo.org",
        ):
            with self.subTest(dominio=dominio):
                self.assertTrue(urls.validar_dominio(dominio))

    def test_validar_dominio_invalido(self):
        for dominio in (
            "www.ifpb.invalid",
            "www..com",
            "-site.com",
            "site-.com",
            "site .com",
            "",
        ):
            with self.subTest(dominio=dominio):
                self.assertFalse(urls.validar_dominio(dominio))

    def test_validar_segmento_valido(self):
        for segmento in ("tsi", "professores", "matriz_curricular", "pagina-2"):
            with self.subTest(segmento=segmento):
                self.assertTrue(urls.validar_segmento(segmento))

    def test_validar_segmento_invalido(self):
        for segmento in ("", ".", "..", "dois nomes", "a/b", "a\\b", "a?b", "a#b"):
            with self.subTest(segmento=segmento):
                self.assertFalse(urls.validar_segmento(segmento))

    def test_validar_url_com_dominio(self):
        self.assertTrue(urls.validar_url("www.ifpb.edu.br"))

    def test_validar_url_com_caminho(self):
        self.assertTrue(urls.validar_url("https://www.ifpb.edu.br/tsi/professores"))

    def test_validar_url_aceita_http_por_normalizar_para_https(self):
        self.assertTrue(urls.validar_url("http://www.ifpb.edu.br/tsi"))

    def test_validar_url_rejeita_dominio_nao_permitido(self):
        self.assertFalse(urls.validar_url("https://www.ifpb.invalid"))

    def test_validar_url_rejeita_espacos_internos(self):
        self.assertFalse(urls.validar_url("https://www.ifpb.edu.br/pagina inicial"))

    def test_validar_url_rejeita_credenciais(self):
        self.assertFalse(urls.validar_url("https://usuario:senha@www.ifpb.edu.br"))

    def test_validar_url_rejeita_porta(self):
        self.assertFalse(urls.validar_url("https://www.ifpb.edu.br:8080"))

    def test_validar_url_rejeita_consulta(self):
        self.assertFalse(urls.validar_url("https://www.ifpb.edu.br/tsi?pagina=2"))

    def test_validar_url_rejeita_fragmento(self):
        self.assertFalse(urls.validar_url("https://www.ifpb.edu.br/tsi#topo"))

    def test_validar_url_rejeita_url_nao_string(self):
        self.assertFalse(urls.validar_url(None))

    def test_decompor_url_retorna_dominio_e_segmentos(self):
        resultado = urls.decompor_url("http://www.ifpb.edu.br/tsi/professores")
        self.assertEqual(resultado, ("www.ifpb.edu.br", ["tsi", "professores"]))

    def test_decompor_url_ignora_barras_repetidas_e_finais(self):
        resultado = urls.decompor_url("https://www.ifpb.edu.br//tsi///alunos/")
        self.assertEqual(resultado, ("www.ifpb.edu.br", ["tsi", "alunos"]))

    def test_montar_url(self):
        resultado = urls.montar_url("WWW.IFPB.EDU.BR", ["tsi", "professores"])
        self.assertEqual(resultado, "https://www.ifpb.edu.br/tsi/professores")

    def test_montar_e_decompor_sao_compativeis(self):
        url = urls.montar_url("www.ifpb.edu.br", ["tsi", "alunos"])
        self.assertEqual(
            urls.decompor_url(url),
            ("www.ifpb.edu.br", ["tsi", "alunos"]),
        )


class TestPersistenciaURLs(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.arquivo_urls = Path(self.temp.name) / "urls.txt"
        self.patch_caminho = patch.object(urls, "CAMINHO_URLS", self.arquivo_urls)
        self.patch_caminho.start()
        self.addCleanup(self.patch_caminho.stop)
        self.addCleanup(self.temp.cleanup)

    def test_carregar_urls_arquivo_com_urls_validas_invalidas_e_duplicadas(self):
        self.arquivo_urls.write_text(
            "www.ifpb.edu.br\n"
            "http://www.google.com\n"
            "linha-invalida\n"
            "\n"
            "https://www.ifpb.edu.br\n",
            encoding="utf-8",
        )

        resultado = urls.carregar_urls()

        self.assertEqual(
            resultado,
            ["https://www.ifpb.edu.br", "https://www.google.com"],
        )

    def test_carregar_urls_arquivo_inexistente_retorna_lista_vazia(self):
        self.assertEqual(urls.carregar_urls(), [])

    def test_carregar_urls_trata_erro_de_leitura(self):
        with patch("builtins.open", side_effect=PermissionError("sem permissão")):
            with self.assertRaises(RuntimeError):
                urls.carregar_urls()

    def test_adicionar_url_salva_e_atualiza_lista(self):
        conhecidas = []

        sucesso, mensagem = urls.adicionar_url("www.ifpb.edu.br", conhecidas)

        self.assertTrue(sucesso)
        self.assertIn("sucesso", mensagem.lower())
        self.assertEqual(conhecidas, ["https://www.ifpb.edu.br"])
        self.assertEqual(
            self.arquivo_urls.read_text(encoding="utf-8"),
            "https://www.ifpb.edu.br\n",
        )

    def test_adicionar_url_rejeita_duplicada(self):
        conhecidas = ["https://www.ifpb.edu.br"]

        sucesso, mensagem = urls.adicionar_url("http://www.ifpb.edu.br", conhecidas)

        self.assertFalse(sucesso)
        self.assertIn("já cadastrada", mensagem.lower())
        self.assertEqual(len(conhecidas), 1)
        self.assertFalse(self.arquivo_urls.exists())

    def test_adicionar_url_rejeita_formato_invalido(self):
        conhecidas = []
        sucesso, mensagem = urls.adicionar_url("endereço inválido", conhecidas)

        self.assertFalse(sucesso)
        self.assertIn("inválido", mensagem.lower())
        self.assertEqual(conhecidas, [])

    def test_adicionar_url_rejeita_valor_que_nao_e_string(self):
        sucesso, _ = urls.adicionar_url(None, [])
        self.assertFalse(sucesso)

    def test_adicionar_url_nao_atualiza_lista_se_escrita_falhar(self):
        conhecidas = []

        with patch("builtins.open", side_effect=OSError("falha de escrita")):
            sucesso, mensagem = urls.adicionar_url("www.ifpb.edu.br", conhecidas)

        self.assertFalse(sucesso)
        self.assertIn("salvar", mensagem.lower())
        self.assertEqual(conhecidas, [])

    def test_remover_url_remove_do_arquivo_e_da_lista(self):
        conhecidas = ["https://www.ifpb.edu.br", "https://www.google.com"]
        self.arquivo_urls.write_text("\n".join(conhecidas) + "\n", encoding="utf-8")

        sucesso, mensagem = urls.remover_url("http://www.ifpb.edu.br", conhecidas)

        self.assertTrue(sucesso)
        self.assertIn("removida", mensagem.lower())
        self.assertEqual(conhecidas, ["https://www.google.com"])
        self.assertEqual(
            self.arquivo_urls.read_text(encoding="utf-8"),
            "https://www.google.com\n",
        )

    def test_remover_url_rejeita_url_nao_cadastrada(self):
        conhecidas = ["https://www.google.com"]
        self.arquivo_urls.write_text("https://www.google.com\n", encoding="utf-8")

        sucesso, mensagem = urls.remover_url("www.ifpb.edu.br", conhecidas)

        self.assertFalse(sucesso)
        self.assertIn("não cadastrada", mensagem.lower())
        self.assertEqual(conhecidas, ["https://www.google.com"])

    def test_remover_url_rejeita_formato_invalido(self):
        conhecidas = ["https://www.google.com"]
        sucesso, _ = urls.remover_url("url inválida", conhecidas)
        self.assertFalse(sucesso)
        self.assertEqual(conhecidas, ["https://www.google.com"])

    def test_remover_url_nao_atualiza_lista_se_escrita_falhar(self):
        conhecidas = ["https://www.ifpb.edu.br"]

        with patch("builtins.open", side_effect=OSError("falha de escrita")):
            sucesso, mensagem = urls.remover_url("www.ifpb.edu.br", conhecidas)

        self.assertFalse(sucesso)
        self.assertIn("remover", mensagem.lower())
        self.assertEqual(conhecidas, ["https://www.ifpb.edu.br"])


if __name__ == "__main__":
    unittest.main(verbosity=2)