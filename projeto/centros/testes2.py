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

    def test_endereco_invalido(self):
        """Teste para verificar endereco inválido."""
        # Acessa a página de login
        self.driver.get("https://ecotrackapp.azurewebsites.net/users/login/")

        # Faz login como user
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "username"))
        ).send_keys("testeuser@gmail.com")
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "password"))
        ).send_keys("testeuser")
        self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()

         # Aguarda até que o link de Agendamentos esteja visível
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.LINK_TEXT, 'Localizar'))
            ).click()
            print("Link de Localizar clicado")
            time.sleep(7)
        except Exception as e:
            print("Erro ao encontrar ou clicar no link de Localizar:", e)

        # Aguarda o redirecionamento e acessa a página de cadastro de pontos de coleta
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.NAME, "user_address"))
        ).click()

        # Preenche o formulário com dados incompletos
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.NAME, "user_address"))
        ).send_keys("aaaaaaa")
        time.sleep(2)
        
        # Submete o formulário
        self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()

        # Verifica se uma mensagem de erro é exibida
        try:
            error_message = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "alert alert-danger"))
            )
            assert "Endereço não encontrado" in error_message.text
            print("Teste passou: Mensagem de erro foi exibida corretamente.")
        except Exception as e:
            print(f"Teste falhou: {e}")

        time.sleep(2)
    def test_localizar_centro(self):
        self.driver.get("https://ecotrackapp.azurewebsites.net/users/login/")
        time.sleep(2)

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "username"))
        ).send_keys("testeuser@gmail.com")
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "password"))
        ).send_keys("testeuser")
        self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()

         # Aguarda até que o link de Agendamentos esteja visível
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.LINK_TEXT, 'Localizar'))
            ).click()
            print("Link de Localizar clicado")
            time.sleep(7)
        except Exception as e:
            print("Erro ao encontrar ou clicar no link de Localizar:", e)

        # Aguarda o redirecionamento e acessa a página de cadastro de pontos de coleta
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.NAME, "user_address"))
        ).click()
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.NAME, "user_address"))
        ).send_keys("Rua do Brum, 77")

        time.sleep(1)
        self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(2)
        try:
            centro_items = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "centro-item"))
            )
            assert len(centro_items) > 0, "Nenhum centro de coleta foi encontrado."
            print(f"Teste passou: {len(centro_items)} centros de coleta encontrados.")
        except Exception as e:
            print(f"Teste falhou: {e}")
    