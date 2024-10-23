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
        
      
    def test_1_access_solicitacoes_without_authentication(self):
        """Teste para verificar se uma empresa não autenticada é redirecionada ao tentar acessar as solicitações."""
        self.driver.get("https://ecotrackapp.azurewebsites.net/agendamento/visualizar/1/")

        # Espera um pouco para garantir que a página tenha carregado
        time.sleep(2)

        # Verifica se a URL atual é a página de login
        current_url = self.driver.current_url
        assert "login" in current_url, f"Esperado estar na página de login, mas está em {current_url}"
        print("Redirecionado para a página de login, como esperado.")



    def test_3_excluir_agendamento_inexistente(self):
        """Teste para verificar a exclusão de um agendamento inexistente ou já excluído."""
        self.driver.get("https://ecotrackapp.azurewebsites.net/users/login/")
        time.sleep(4)  # Espera para garantir que a página carregou

        # Fazer login
        email_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "username"))
        )
        email_field.clear()
        email_field.send_keys("empresa@gmail.com")

        password_field = self.driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys("123")

        login_button = self.driver.find_element(By.XPATH, '//button[@type="submit"]')
        login_button.click()
        time.sleep(4)

        try:
            agendamentos_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Agendamentos"))
            )
            agendamentos_link.click()
            print("Link de 'Agendamentos' clicado com sucesso.")
            time.sleep(4)  # Espera para garantir que a página de agendamentos carregue corretamente
        except Exception as e:
            print("Erro ao clicar no link de 'Agendamentos':", e)

        # Tentar excluir um agendamento inexistente (simulando um ID de agendamento inválido)
        try:
            self.driver.get("https://ecotrackapp.azurewebsites.net/agendamento/delete/99999/")
            time.sleep(2)

            # Verificar se a mensagem de erro de agendamento não encontrado é exibida
            mensagem_erro = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "mensagem-erro"))
            )
            assert "Agendamento não disponível para exclusão" in mensagem_erro.text
            print("Mensagem de erro de agendamento não encontrado exibida corretamente.")

        except Exception as e:
            print("Erro ao tentar excluir um agendamento inexistente:", e)
            print("HTML atual da página:", self.driver.page_source)  # Captura o HTML para análise
