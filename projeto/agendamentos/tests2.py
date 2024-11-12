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
        """Se o usuário acessar as recompensas sem estar autenticado, o sistema deve solicitar autenticação antes de permitir o acesso às recompensas."""
        self.driver.get("https://ecotrackapp.azurewebsites.net/users/recompensas/")

        time.sleep(4)

        current_url = self.driver.current_url
        assert "login" in current_url, f"Esperado estar na página de login, mas está em {current_url}"
        print("Redirecionado para a página de login, como esperado.")        
        
    def test_insufficient_points_recompensas(self):
        """Se o usuário acessar as recompensas e não tiver realizado ações de reciclagem suficientes, o sistema deve exibir uma mensagem informando que ele ainda não possui pontos suficientes."""
        self.driver.get("https://ecotrackapp.azurewebsites.net/users/login/")
        
        time.sleep(2)

        # Campo de email
        try:
            email_field = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "username"))
            )
            email_field.click()
            email_field.clear()
            email_field.send_keys("testerecompensa2@gmail.com")
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
            password_field.send_keys("123")
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
                EC.visibility_of_element_located((By.LINK_TEXT, 'Perfil'))
            ).click()
            time.sleep(3)
        except Exception as e:
            print("Erro ao clicar no link de Perfil:", e)
            
        time.sleep(2)
        
    
    def test_recompensas(self):
        """Quando o usuário tiver pontos de recompensa, o sistema deve permitir que ele entre na página de resgatar recompensas"""
        self.driver.get("https://ecotrackapp.azurewebsites.net/agendamento/")
        
                # Preenche o formulário para ganhar pontos
        nome_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "name"))
        )
        nome_field.send_keys("Teste Usuário 1")
        time.sleep(1)
        data_field = self.driver.find_element(By.ID, "date")
        data_field.clear()  # Limpa o campo de data antes de preenchê-lo
        self.driver.execute_script("document.getElementById('date').value = '2024-11-26';")
        time.sleep(1)
        
        # Preencher o campo "Hora" (Seleção por valor)
        # Forçar a seleção do horário usando JavaScript
        self.driver.execute_script("document.getElementById('time').value = '10:00';")
        time.sleep(1)

        # empresa
        empresa_dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "empresa"))
        )
        empresa_dropdown.click()
        time.sleep(1)

        # Seleciona a primeira opção diretamente usando JavaScript
        self.driver.execute_script("document.querySelector('#empresa option:nth-child(2)').selected = true;")
        time.sleep(1)

        # Alternativa: clicar na primeira opção
        first_option = self.driver.find_element(By.XPATH, "//select[@id='empresa']/option[2]")  # Mudamos para 2, pois o primeiro é o valor padrão
        first_option.click()
        time.sleep(1)
       
        endereco_field = self.driver.find_element(By.ID, "endereco")
        endereco_field.clear()  # Limpa o campo de data antes de preenchê-lo
        self.driver.execute_script("document.getElementById('endereco').value = 'Rua do Brum, 77';")
        time.sleep(1)
        
        # tipo de material
        metal_checkbox = self.driver.find_element(By.XPATH, "//input[@value='Metal']")
        metal_checkbox.click()
        time.sleep(2)
        submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
            )
        submit_button.click()

        time.sleep(2)
        
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.LINK_TEXT, 'Voltar ao Dashboard'))
            ).click()
            time.sleep(3)
        except Exception as e:
            print("Erro ao clicar no link de Dashboard:", e)
            
            
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.LINK_TEXT, 'Perfil'))
            ).click()
            time.sleep(3)
        except Exception as e:
            print("Erro ao clicar no link de Perfil:", e)
            
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.LINK_TEXT, 'Acessar Recompensas'))
            ).click()
            time.sleep(3)
        except Exception as e:
            print("Erro ao clicar no link de Recompensas:", e)
    
                    
        
