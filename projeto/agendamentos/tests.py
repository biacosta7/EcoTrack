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

    def test_access_agendamentos_without_authentication(self):
        time.sleep(5)
        """Se o usuário tentar agendar uma coleta sem estar autenticado, o sistema deve solicitar autenticação antes de permitir o agendamento."""
        self.driver.get("https://ecotrackapp.azurewebsites.net/agendamento/")

        time.sleep(3)

        current_url = self.driver.current_url
        assert "login" in current_url, f"Esperado estar na página de login, mas está em {current_url}"
        print("Redirecionado para a página de login, como esperado.")
    
    def test_access_solicitacoes_without_authentication(self):
        """Se a empresa tentar acessar as solicitações sem estar autenticada, o sistema deve solicitar autenticação antes de permitir o acesso às solicitações."""
        self.driver.get("https://ecotrackapp.azurewebsites.net/agendamento/visualizar/1/")

        time.sleep(4)

        current_url = self.driver.current_url
        assert "login" in current_url, f"Esperado estar na página de login, mas está em {current_url}"
        print("Redirecionado para a página de login, como esperado.")        
   
    def test_agendamento_empresa(self):
        """Se a empresa tentar visualizar solicitações de agendamento, mas não houver nenhuma solicitação disponível no momento, o sistema deve exibir uma mensagem informando que não há solicitações pendentes"""
        
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

        time.sleep(2)

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

        # Aguarda até que o link de Agendamentos esteja visível
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.LINK_TEXT, 'Agendamentos'))
            ).click()
            time.sleep(3)
        except Exception as e:
            print("Erro ao clicar no link de Agendamentos:", e)

        # Verifica a mensagem de agendamentos
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.TAG_NAME, 'p'))
            )
            message_element = self.driver.find_element(By.TAG_NAME, 'p')
            assert "Não há agendamentos para a sua empresa." in message_element.text
        except Exception as e:
            print("Erro ao verificar a mensagem de agendamentos:", e)
            
    def test_agendamento_duplicado(self):
        """Se o usuário tentar agendar uma coleta para uma data ou horário indisponível, o sistema deve exibir uma mensagem de erro."""
        self.driver.get("https://ecotrackapp.azurewebsites.net/users/login/")
        
        time.sleep(2)

        # Campo de email
        try:
            email_field = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "username"))
            )
            email_field.click()
            email_field.clear()
            email_field.send_keys("testeruser@gmail.com")
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
            password_field.send_keys("testeruser")
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

        # Aguarda até que o link de Agendamentos esteja visível
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.LINK_TEXT, 'Agendar'))
            ).click()
            time.sleep(3)
        except Exception as e:
            print("Erro ao clicar no link de Agendamentos:", e)

        # Preenche o formulário
        nome_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "name"))
        )
        nome_field.send_keys("Teste Usuário 1")
        time.sleep(1)
        data_field = self.driver.find_element(By.ID, "date")
        data_field.clear()  # Limpa o campo de data antes de preenchê-lo
        self.driver.execute_script("document.getElementById('date').value = '2024-11-01';")
        time.sleep(1)
        
        # Preencher o campo "Hora" (Seleção por valor)
        # Forçar a seleção do horário usando JavaScript
        self.driver.execute_script("document.getElementById('time').value = '09:00';")
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

        time.sleep(3)

        # Tenta agendar novamente com os mesmos dados
        self.driver.get("https://ecotrackapp.azurewebsites.net/users/usuario/dashboard/")

        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.LINK_TEXT, 'Agendar'))
            ).click()
            time.sleep(3)
        except Exception as e:
            print("Erro ao clicar no link de Agendamentos:", e)

        # Preenche o formulário
        nome_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "name"))
        )
        nome_field.send_keys("Teste Usuário 2")
        time.sleep(1)
        data_field = self.driver.find_element(By.ID, "date")
        data_field.clear()  # Limpa o campo de data antes de preenchê-lo
        self.driver.execute_script("document.getElementById('date').value = '2024-11-01';")
        time.sleep(1)
        
        # Preencher o campo "Hora" (Seleção por valor)
        # Forçar a seleção do horário usando JavaScript
        self.driver.execute_script("document.getElementById('time').value = '09:00';")
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

        time.sleep(3)

        
    def test_login_empresa(self):
        """Teste para verificar o login da empresa e exclusão de um agendamento."""
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

        time.sleep(2)

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


    #-------Júlio e Thiago--------
    def test_delete_agendamento(self):
        """ exclusão de um agendamento."""
        time.sleep(2)
        # Passo 1: Clicar no link de "Agendamentos"
        try:
            agendamentos_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Agendamentos"))
            )
            agendamentos_link.click()
            print("Link de 'Agendamentos' clicado com sucesso.")
            time.sleep(2)  # Espera para garantir que a página de agendamentos carregue corretamente
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
        """Se a empresa tentar gerenciar um pedido de coleta que não existe ou que foi cancelado, o sistema deve exibir uma mensagem de erro informando que o pedido não está disponível para gerenciamento."""
        self.driver.get("https://ecotrackapp.azurewebsites.net/users/empresa/dashboard/")
        time.sleep(2)
        # Clicar no link de "Agendamentos"
        agendamentos_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Agendamentos"))
        )
        agendamentos_link.click()
        time.sleep(2)

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