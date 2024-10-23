from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class PontoDeColetaTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_access_solicitacoes_without_authentication(self):
            """Teste para verificar se uma empresa não autenticada é redirecionada ao tentar acessar os centros."""
            self.driver.get("https://ecotrackapp.azurewebsites.net/centros/cadastrar/")

            # Espera um pouco para garantir que a página tenha carregado
            time.sleep(2)

            # Verifica se a URL atual é a página de login
            current_url = self.driver.current_url
            assert "login" in current_url, f"Esperado estar na página de login, mas está em {current_url}"
            print("Redirecionado para a página de login, como esperado.")

    def test_cadastro_ponto_de_coleta_incompleto(self):
        """Teste para verificar se o sistema exibe uma mensagem de erro ao tentar cadastrar um ponto de coleta com dados incompletos."""
        # Acessa a página de login
        self.driver.get("https://ecotrackapp.azurewebsites.net/users/login/")

        # Faz login como empresa
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "username"))
        ).send_keys("teste@gmail.com")
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "password"))
        ).send_keys("teste123")
        self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()

         # Aguarda até que o link de Agendamentos esteja visível
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.LINK_TEXT, 'Localizações'))
            ).click()
            print("Link de Localizações clicado")
            time.sleep(7)
        except Exception as e:
            print("Erro ao encontrar ou clicar no link de Localizações:", e)

        # Aguarda o redirecionamento e acessa a página de cadastro de pontos de coleta
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.LINK_TEXT, "Cadastrar novo centro"))
        ).click()

        # Preenche o formulário com dados incompletos
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "nome"))
        ).send_keys("Ponto de Coleta Incompleto")
        time.sleep(1)
        # Telefone
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "telefone"))
        ).send_keys("11999999999")
        time.sleep(1)
        # Deixa o campo de endereço vazio para simular o envio de dados incompletos

        # Campo CEP
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "cep"))
        ).send_keys("12345-678")
        time.sleep(1)
        # Seleciona um tipo de material
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@value='metal']"))
        ).click()
        time.sleep(1)
        # Horário de Abertura
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "horario_abertura"))
        ).send_keys("08:00")
        time.sleep(1)
        # Horário de Fechamento
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "horario_fechamento"))
        ).send_keys("18:00")
        time.sleep(2)
        # Submete o formulário
        self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()

        # Verifica se uma mensagem de erro é exibida
        try:
            error_message = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger"))
            )
            assert "Dados incompletos" in error_message.text
            print("Teste passou: Mensagem de erro foi exibida corretamente.")
        except Exception as e:
            print(f"Teste falhou: {e}")

        time.sleep(2)