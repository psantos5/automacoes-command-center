
import logging
import os
import time

from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,ElementNotVisibleException,InvalidSelectorException,ElementNotInteractableException,NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


nome_arquivo_py = os.path.splitext(os.path.basename(__file__))[0]
pasta_prints_erros = 'erros_screenshot'
data_hora_atual = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
screenshot_filename = f"{nome_arquivo_py}_{data_hora_atual}_erro.png"


script_directory = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(script_directory, 'logs')
if not os.path.exists(log_file_path):
    os.makedirs(log_file_path)

log_filename = f"{log_file_path}/{nome_arquivo_py}.log"
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def wait_and_log_clickable_element(driver, by, value):
    element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((by, value)))
    return element

def log_execution_time(start_time, end_time, action_name):
    duration = end_time - start_time
    if duration < 1:
        formatted_duration = f"{duration * 1000:.2f} milissegundos"
    else:
        formatted_duration = f"{duration:.2f} segundos"
    logging.info(f"{action_name} executado em {formatted_duration}")

def print_erro(driver, pasta_prints_erros, screenshot_filename):
    screenshot_path = os.path.join(pasta_prints_erros, screenshot_filename)

    try:
        if not os.path.exists(pasta_prints_erros):
            os.makedirs(pasta_prints_erros)
            logging.warning(f"O diretório {pasta_prints_erros} não existe, será criado agora..")
            driver.save_screenshot(screenshot_path)
            logging.info(f"Screenshot salvo em: {screenshot_path}")
            return True  
        else:
            driver.save_screenshot(screenshot_path)
            logging.info(f"Screenshot salvo em: {screenshot_path}")
            return True  
    except Exception as e:
        logging.error(f"Erro ao criar o diretório: {str(e)}")
        driver.save_screenshot(screenshot_path)
        return False  


xpath_element = '//*[@id="seu_elemento"]'



driver = webdriver.Chrome()
wait = WebDriverWait(driver, 8) 


try:
    

    driver.maximize_window()
    start_time = time.time()

    logging.info("Abrindo pagina")
    driver.get("https://pagseguro.uol.com.br/")
    logging.info(f"URL Aberta: {driver.current_url}")

    end_time = time.time()
    log_execution_time(start_time, end_time, "Tempo de carregamento da página:")
    duration = end_time - start_time
    if duration > 1:
        logging.warning(f"Atenção, pagina demorou mais de 1 segundo para carregar: {driver.current_url}")
       
    else:
        pass
  
    if "https://pagseguro.uol.com.br/home/escolha-melhor-solucao" in driver.current_url:
        logging.info("A página foi redirecionada para a pagina nova do pags.")
        element = wait_and_log_clickable_element(driver, By.XPATH, '//*[@id="__next"]/header/div/div/div/div/a[1]')
        if element.is_displayed() and element.is_enabled():
            logging.info("Elemento 'Entrar' está visível e habilitado.")
        else:
            logging.error("Não foi possivel localizar ou clicar no elemento 'Entrar'")
    else:
        element = wait_and_log_clickable_element(driver, By.XPATH, '//*[@id="entrar"]')
        if element.is_displayed() and element.is_enabled():
           logging.info("Elemento 'Entrar' está visível e habilitado.")
        else:
            logging.error("Não foi possivel localizar ou clicar no elemento 'Entrar'")
    element.click()
    
      
   
    url_esperada = "https://acesso.pagseguro.uol.com.br/"
    if url_esperada == driver.current_url:
        logging.info(f"Clique no 'Entrar' foi bem-sucedido. URL atual: {driver.current_url}")
    else:
        logging.error(f"Url invalida {driver.current_url}")



    


 
    element = wait_and_log_clickable_element(driver, By.XPATH, '//*[@id="user"]')
    acesso = '' #Inserir aqui seu login de acesso aqui (E-mail, CPF ou Telefone)
    element.send_keys(acesso)
    value_acesso = element.get_attribute("value")
    if acesso == value_acesso:
           logging.info(f"Inserindo dados de acesso: {value_acesso}")
    else:
        logging.error(f"Erro ao inserir dados de acesso: {value_acesso}")
        

    element = wait_and_log_clickable_element(driver, By.XPATH, '//*[@id="continue"]')
    element.click()

 
    start_time = time.time()
    element = wait_and_log_clickable_element(driver, By.XPATH, '//*[@id="password"]')
    end_time = time.time()
    log_execution_time(start_time, end_time, "Localização da conta:")
    time_loading_account = end_time - start_time
    if time_loading_account > 5:
        logging.warning("Atenção, o site demorou mais de 5 segundos para localizar a pagina")
    else:
        pass
                
  
    element = wait_and_log_clickable_element(driver, By.XPATH, '//*[@id="forgotPassword"]')
    element.click()

    logging.info("Envio de sms")
    element = wait_and_log_clickable_element(driver, By.XPATH, '//*[@id="sms-factor"]')
    element.click()

    time.sleep(8)

 
    element = wait_and_log_clickable_element(driver, By.XPATH, '//*[@id="back-button"]')
    element.click()


    logging.info(f"Url atual: {driver.current_url}")
    element = wait_and_log_clickable_element(driver, By.XPATH, '//*[@id="credential-input"]')
    element.send_keys('') #Inserir seu login de acesso aqui (E-mail, CPF ou Telefone)
    element_value = element.get_attribute("value")
    logging.info(f"Inserindo dados de acesso: {element_value}")

  
    element = wait_and_log_clickable_element(driver, By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div[2]/div/div[1]/div/div/div/form/button')
    element.click()
    time.sleep(4)

    logging.info("Envio de e-mail")
    element = wait_and_log_clickable_element(driver, By.XPATH, '//*[@id="email-factor"]/div[2]/span[1]')
    element.click()
    time.sleep(4)


except TimeoutException as e:
    

    try:
        element = driver.find_element(By.XPATH, xpath_element)
        if not element.is_displayed():
            raise ElementNotVisibleException("Elemento não está visível.")
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        
        
    except NoSuchElementException as ex:
        logging.error(f"Elemento não encontrado com o XPath '{str(ex)}")
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        
    except ElementNotVisibleException as inner_exception:
        logging.error(f"Erro ElementNotVisibleException: {type(inner_exception).__name__} - {str(inner_exception)}")
        logging.info("Elemento não está visível.")
        print_erro(driver, pasta_prints_erros, screenshot_filename)

    except Exception as inner_exception:
        logging.error(f"Erro inesperado:: {type(inner_exception).__name__} - {str(inner_exception)}")
        print_erro(driver, pasta_prints_erros, screenshot_filename)
    else:
        logging.error(f"Erro TimeoutException: {type(e).__name__} - {str(e)}")
        logging.info("Tempo de espera excedido para encontrar o elemento.")
        print_erro(driver, pasta_prints_erros, screenshot_filename)

except InvalidSelectorException as e:
    logging.error(f"Erro InvalidSelectorException: {type(e).__name__} - {str(e)}")
    logging.info("Elemento inválido.")
    print_erro(driver, pasta_prints_erros, screenshot_filename)

except ElementNotInteractableException as e:
    logging.error(f"Erro ElementNotInteractableException: {type(e).__name__} - {str(e)}")
    logging.info("Elemento não é interagível.")
    print_erro(driver, pasta_prints_erros, screenshot_filename)

except Exception as e:
    logging.error(f"Ocorreu um erro: {type(e).__name__} - {str(e)}")
    print_erro(driver, pasta_prints_erros, screenshot_filename)

    
    
finally:

    end_time = time.time()
    log_execution_time(start_time, end_time, "Duração do teste:")
    driver.quit()
    logging.shutdown()
    


