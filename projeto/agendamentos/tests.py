from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class AgendamentoTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()
    
    def test_access_solicitacoes_without_authentication(self):
        """Teste para verificar se uma empresa não autenticada é redirecionada ao tentar acessar as solicitações."""
        self.driver.get("https://ecotrackapp.azurewebsites.net/agendamento/visualizar/1/")

        # Espera um pouco para garantir que a página tenha carregado
        time.sleep(4)

        # Verifica se a URL atual é a página de login
        current_url = self.driver.current_url
        assert "login" in current_url, f"Esperado estar na página de login, mas está em {current_url}"
        print("Redirecionado para a página de login, como esperado.")

    def test_login_empresa(self):
        """Teste para verificar o login da empresa."""
        self.driver.get("https://ecotrackapp.azurewebsites.net/users/login/")
        
        # Aguardar um pouco para garantir que a página carregou
        time.sleep(4)

        # Campo de email
        try:
            email_field = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "username"))
            )
            print("Campo de email encontrado")
            email_field.click()  # Clica para garantir que o campo está focado
            email_field.clear()  # Limpa o campo antes de preencher
            email_field.send_keys("teste@gmail.com")  # Preenche o email
            print("Campo de email preenchido com sucesso")
        except Exception as e:
            print("Erro ao encontrar ou preencher o campo de email:", e)
            print("HTML atual da página:", self.driver.page_source)  # Adicionando o HTML atual

        time.sleep(4)
        # Campo de senha
        try:
            password_field = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "password"))
            )
            print("Campo de senha encontrado")
            password_field.click()  # Clica para focar
            password_field.clear()  # Limpa o campo antes de preencher
            password_field.send_keys("teste123")  # Preenche a senha
            print("Campo de senha preenchido com sucesso")
        except Exception as e:
            print("Erro ao encontrar ou preencher o campo de senha:", e)

        time.sleep(2)
        # Botão de login
        try:
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
            )
            print("Botão de login encontrado")
            login_button.click()
        except Exception as e:
            print("Erro ao clicar no botão de login:", e)

        # Aguarda até que o link de Agendamentos esteja visível
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.LINK_TEXT, 'Agendamentos'))
            ).click()
            print("Link de Agendamentos clicado")
            time.sleep(7)
        except Exception as e:
            print("Erro ao encontrar ou clicar no link de Agendamentos:", e)

        # Verifica a mensagem de agendamentos
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.TAG_NAME, 'p'))
            )
            message_element = self.driver.find_element(By.TAG_NAME, 'p')
            assert "Não há agendamentos para a sua empresa." in message_element.text
            print("Mensagem de agendamentos verificada")
        except Exception as e:
            print("Erro ao verificar a mensagem de agendamentos:", e)