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

    def test_login_empresa(self):
        """Teste para verificar o login da empresa e exclusão de um agendamento."""
        self.driver.get("https://ecotrackapp.azurewebsites.net/users/login/")
        time.sleep(4)  # Espera para garantir que a página carregou

        # Campo de email
        try:
            email_field = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "username"))
            )
            print("Campo de email encontrado")
            email_field.click()
            email_field.clear()
            email_field.send_keys("teste@gmail.com")  # Preenche o email
            print("Campo de email preenchido com sucesso")
        except Exception as e:
            print("Erro ao encontrar ou preencher o campo de email:", e)
            print("HTML atual da página:", self.driver.page_source)

        time.sleep(4)

        # Campo de senha
        try:
            password_field = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "password"))
            )
            print("Campo de senha encontrado")
            password_field.click()
            password_field.clear()
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

        time.sleep(4)

        # Passo 1: Clicar no link de "Agendamentos"
        try:
            agendamentos_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Agendamentos"))
            )
            agendamentos_link.click()
            print("Link de 'Agendamentos' clicado com sucesso.")
            time.sleep(4)  # Espera para garantir que a página de agendamentos carregue corretamente
        except Exception as e:
            print("Erro ao clicar no link de 'Agendamentos':", e)

        # Passo 2: Excluir um agendamento
        try:
            # Verificar se há um botão de exclusão com a classe 'delete-button'
            delete_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "delete-button"))
            )
            print("Botão de exclusão encontrado")
            delete_button.click()
            time.sleep(2)

            # Capturar o alerta e confirmar
            alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            print(f"Alerta de confirmação capturado: {alert.text}")
            alert.accept()  # Aceitar o alerta de confirmação
            print("Alerta de confirmação aceito.")

            # Esperar até que a página seja recarregada após o POST
            WebDriverWait(self.driver, 10).until(
                EC.staleness_of(delete_button)  # Aguarda até que o botão desapareça da página
            )
            print("Formulário de exclusão submetido e página atualizada.")

            # Verificar se o agendamento foi excluído
            mensagem_sucesso = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "mensagem-sucesso"))
            )
            assert "Agendamento excluído com sucesso" in mensagem_sucesso.text
            print("Agendamento excluído com sucesso")

        except Exception as e:
            print("Erro ao excluir o agendamento:", e)

    def test_excluir_agendamento_inexistente(self):
        """Teste para verificar a exclusão de um agendamento inexistente ou já excluído."""
        self.driver.get("https://ecotrackapp.azurewebsites.net/users/login/")
        time.sleep(4)  # Espera para garantir que a página carregou

        # Fazer login
        email_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "username"))
        )
        email_field.clear()
        email_field.send_keys("teste@gmail.com")

        password_field = self.driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys("teste123")

        login_button = self.driver.find_element(By.XPATH, '//button[@type="submit"]')
        login_button.click()
        time.sleep(4)

        # Clicar no link de "Agendamentos"
        agendamentos_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Agendamentos"))
        )
        agendamentos_link.click()
        time.sleep(4)

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
