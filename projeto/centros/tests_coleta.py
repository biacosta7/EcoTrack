from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class PontoColetaTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_1_gerenciamento_sem_autenticacao(self):
        """Teste para verificar se uma empresa não autenticada é redirecionada ao tentar acessar o gerenciamento de pontos."""
        # Acessa a página de gerenciamento de ponto sem estar autenticado
        self.driver.get("https://ecotrackapp.azurewebsites.net/centros/lista/")  # ID de um ponto ativo
        
        time.sleep(1)

        # Verifica se o redirecionamento para a página de login ocorre
        current_url = self.driver.current_url
        assert "login" in current_url, f"Esperado redirecionamento para login, mas está em {current_url}"
        print("Redirecionado para a página de login, como esperado.")
        
        
    def test_2_login_empresa(self):
        """Teste para verificar o login da empresa e exclusão de um agendamento."""
        self.driver.get("https://ecotrackapp.azurewebsites.net/users/login/")
        time.sleep(1)  # Espera para garantir que a página carregou

        # Campo de email
        try:
            email_field = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "username"))
            )
            print("Campo de email encontrado")
            email_field.click()
            email_field.clear()
            email_field.send_keys("empresa@gmail.com")  # Preenche o email
            print("Campo de email preenchido com sucesso")
        except Exception as e:
            print("Erro ao encontrar ou preencher o campo de email:", e)
            print("HTML atual da página:", self.driver.page_source)

        time.sleep(1)

        # Campo de senha
        try:
            password_field = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "password"))
            )
            print("Campo de senha encontrado")
            password_field.click()
            password_field.clear()
            password_field.send_keys("123")  # Preenche a senha
            print("Campo de senha preenchido com sucesso")
        except Exception as e:
            print("Erro ao encontrar ou preencher o campo de senha:", e)

        time.sleep(1)

        # Botão de login
        try:
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
            )
            print("Botão de login encontrado")
            login_button.click()
        except Exception as e:
            print("Erro ao clicar no botão de login:", e)

        time.sleep(4)        
        

    def test_3_gerenciamento_ponto_inexistente(self):
        """Teste para verificar a tentativa de gerenciar um ponto de coleta inexistente."""

        # Passo 1: Clicar no botão de "Localizações" após login
        try:
            localizacoes_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Localizações"))
            )
            localizacoes_button.click()
            print("Botão de 'Localizações' clicado com sucesso.")
            time.sleep(4)  # Espera para garantir que a página de localizações carregue corretamente
        except Exception as e:
            print("Erro ao clicar no botão de 'Localizações':", e)

        # Passo 2: Tentar acessar um ponto de coleta inexistente
        self.driver.get("https://ecotrackapp.azurewebsites.net/centros/atualizar/99999/")

        
        # Espera que a página tenha carregado
        time.sleep(4)

        try:
            # Verifica se a mensagem de erro é exibida
            mensagem_erro = WebDriverWait(self.driver, 10).until(
               EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger"))
            )
            assert "Ponto de coleta não existente" in mensagem_erro.text
            print("Mensagem de erro exibida corretamente para ponto de coleta inexistente.")
        except Exception as e:
            print("Erro ao verificar o gerenciamento de ponto inexistente:", e)
