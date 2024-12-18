from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
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
    
    
    
    def test_access_recompensas_without_authentication(self):
        """Se a empresa tentar acessar um ciclo de vida sem estar autenticada, o sistema deve exibir uma mensagem de erro."""
        self.driver.get("https://ecotrackapp.azurewebsites.net/agendamento/editar_etapa/11/")
        
        time.sleep(8)        
        
        
    def test_insufficient_points_recompensas(self):
        """Se a empresa tentar acessar um ciclo de vida inexistente, o sistema deve exibir uma mensagem de erro."""
        self.driver.get("https://ecotrackapp.azurewebsites.net/users/login/")
        
        time.sleep(2)

        # Campo de email
        try:
            email_field = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "username"))
            )
            email_field.click()
            email_field.clear()
            email_field.send_keys("teste@gmail.com")
        except Exception as e:
            print("Erro ao preencher o campo de email:", e)

        time.sleep(1)

        # Campo de senha
        try:
            password_field = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "password"))
            )
            password_field.click()
            password_field.clear()
            password_field.send_keys("teste123")
        except Exception as e:
            print("Erro ao preencher o campo de senha:", e)

        time.sleep(2)

        # Botão de login
        try:
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
            )
            login_button.click()
        except Exception as e:
            print("Erro ao clicar no botão de login:", e)
            
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.LINK_TEXT, 'Agendamentos'))
            ).click()
            time.sleep(3)
        except Exception as e:
            print("Erro ao clicar no link de Agendamentos:", e)
            
        self.driver.get("https://ecotrackapp.azurewebsites.net/agendamento/editar_etapa/999/")
        
        time.sleep(2)


        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.LINK_TEXT, 'Editar Etapa'))
            ).click()
            time.sleep(3)
        except Exception as e:
            print("Erro ao clicar no link de Editar Etapa:", e)        
            


# Usando XPath para selecionar o botão pelo texto
        try:
            save_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Salvar Alterações")]'))
    )
            save_button.click()
            time.sleep(3)
        except Exception as e:
            print("Erro ao clicar no botão de Salvar Alterações:", e)
        
        
            
        

