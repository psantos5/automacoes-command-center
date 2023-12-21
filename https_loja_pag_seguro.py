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


log_filename = f"{log_file_path}/{nome_arquivo_py}_{data_hora_atual}.log"
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

def add_more_products(element, logging):
    xpath = '/html/body/div[1]/form/div[3]/a'

    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    logging.info('Clicando em "Adicionar mais produtos"')
    element.click()

def check_purchase_limit_alert(element, driver, pasta_prints_erros, screenshot_filename):
    element = wait_and_log_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div/div/div/div[3]/div[1]/div/div[1]/button[2]')
    element.click()
    logging.info("Clicando no botão de '+'")
    element = wait_and_log_clickable_element(driver, By.XPATH, '//*[@id="cart-item__limit__alert-message"]')
    if element.is_displayed() and element.is_enabled():
        logging.info("Alerta de limite de compra está aparecendo com sucesso")
    else:
        logging.error("Alerta de limite de compra não está aparecendo")
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()

    
def remove_one_card_machine(element, driver, pasta_prints_erros, screenshot_filename):
    element = wait_and_log_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div/div/div/div[3]/div[1]/div/div[1]/button[1]')
    if element.is_displayed() and element.is_enabled():
        element.click()
        logging.info("Clicando no botão de '-'")
    else:
        logging.error('Não foi possivel clicar no botão '-'')
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()

xpath_element = '//*[@id="seu_elemento"]'


driver = webdriver.Chrome()

try:

    driver.maximize_window()
    start_time = time.time()

    logging.info("Abrindo pagina")
    driver.get("https://loja.pagseguro.uol.com.br/")
    logging.info(f"URL Aberta: {driver.current_url}")

    end_time = time.time()
    log_execution_time(start_time, end_time, "Tempo de carregamento da pagina")
    
    duration = end_time - start_time
    if duration > 2:
        logging.warning(f"Atenção, pagina demorou mais de 1 segundo para carregar: {driver.current_url}")      
    else:
        pass


    element = wait_and_log_clickable_element(driver, By.XPATH, '//*[@id="ps"]/div[1]/div/div[1]/div[3]/a')
    if element.is_displayed() and element.is_enabled():
        element.click()
        logging.info(f"Moderninha Pro 2 do header está visivel, clicavel e sendo direcionado para: {driver.current_url}")
        check_purchase_limit_alert(element, driver, pasta_prints_erros, screenshot_filename)
        remove_one_card_machine(element, driver, pasta_prints_erros, screenshot_filename)
        add_more_products(element, logging)
    else:
        logging.error("Não foi possivel localizar a Moderninha Pro 2 no header")
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit() 



    element = wait_and_log_clickable_element(driver, By.XPATH, '//*[@id="ps"]/div[1]/div/div[2]/div[3]/a')
    if element.is_displayed() and element.is_enabled():
        element.click()
        logging.info(f"Moderninha Plus 2 do header está visivel, clicavel e sendo direcionado para: {driver.current_url}")
        check_purchase_limit_alert(element, driver, pasta_prints_erros, screenshot_filename)
        remove_one_card_machine(element, driver, pasta_prints_erros, screenshot_filename)
    else:
        logging.error("Não foi possivel localizar a Moderninha Plus 2 no header")
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit() 

    element = wait_and_log_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div[1]/div/div/div[3]/div[2]/div/p[3]/a')
    if element.is_displayed() and element.is_enabled():
        element.click()
        logging.info('Removendo a Moderninha Pro 2 do carrinho')
        
    else:
        logging.error('Não foi possivel remover a Moderninha Pro 2 do carrinho')
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()

    time.sleep(1)

    element = wait_and_log_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div[1]/div/div[1]/p/a')
    if element.is_displayed() and element.is_enabled():
        element.click()
        logging.info('Adicionando novamente as Moderninha Pro 2')
    else:
        logging.error('Não foi possivel adicionar a Moderninha Pro 2 no carrinho novamente')
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()

    element = wait_and_log_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div[2]/div/div/div[3]/div[2]/div/p[3]/a')
    if element.is_displayed() and element.is_enabled():
        element.click()
        logging.info('Removendo a Moderninha Plus 2 do carrinho')
    else:
        logging.error('Não foi possivel remover a Moderninha Plus 2 do carrinho')
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()



    element = wait_and_log_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div[2]/div/div[1]/p/a')
    if element.is_displayed() and element.is_enabled():
        element.click()
        logging.info('Adicionando novamente a Moderninha Plus 2')
    else:
        logging.error('Não foi possivel adicionar a Moderninha Plus 2 no carrinho novamente')
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()

    element = wait_and_log_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div[1]/div/div/div[3]/div[2]/div/p[3]/a')
    if element.is_displayed() and element.is_enabled():
        element.click()
        time.sleep(1)
    else: 
        logging.error("Ocorreu um erro ao remover a Moderninha Pro 2")
        print_erro(driver, pasta_prints_erros, screenshot_filename)
    

    element = wait_and_log_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div[2]/div/div/div[3]/div[2]/div/p[3]/a')
    if element.is_displayed() and element.is_enabled():
        element.click()
    else: 
        logging.error("Ocorreu um erro ao remover a Moderninha Plus 2")
        print_erro(driver, pasta_prints_erros, screenshot_filename)
    

    expected_text = "Seu carrinho está vazio"
    element_cart_empty = WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '/html/body/div[1]/form/div[5]/section/div[2]/h2'), expected_text))
    if element_cart_empty:
        logging.info("Devido a trava de limite de compras de maquininhas, removido as maquininhas do carrinho e o mesmo está vazio, seguindo com o teste com as demais maquininhas")
    else:
        logging.error("Não foi possivel deixar o carrinho vazio, é ncessario que o carrinho esteja vazio para seguir com o teste")   
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()
    
    logging.info('Validando se a grade de maquininhas mais vendidas do carrinho está habilitada e redirecionando corretamente')
    element = wait_and_log_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[6]/div/div/div[2]/div/div[1]/div[3]/a[1]')
    if element.is_displayed() and element.is_displayed():
        logging.info("Moderninha Smart redirecionando corretamente")
    else:
        logging.error("Ocorreu um erro ao validar o redirecionamento da Moderninha Smart na grade de maquininhas mais vendidas")
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()
    
    element = wait_and_log_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[6]/div/div/div[2]/div/div[2]/div[3]/a[1]')
    if element.is_displayed() and element.is_displayed():
        logging.info("Minizinha NFC 2 redirecionando corretamente")
    else:
        logging.error("Ocorreu um erro ao validar o redirecionamento da Minizinha NFC 2 na grade de maquininhas mais vendidas")
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()

    element = wait_and_log_clickable_element(driver, By.XPATH, '//html/body/div[1]/form/div[6]/div/div/div[2]/div/div[3]/div[3]/a[1]')
    if element.is_displayed() and element.is_displayed():
        logging.info("Moderninha Plus 2 redirecionando corretamente")
    else:
        logging.error("Ocorreu um erro ao validar o redirecionamento da Moderninha Plus 2 na grade de maquininhas mais vendidas")
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()
  
    element = wait_and_log_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[6]/div/div/div[2]/div/div[4]/div[3]/a[1]')
    if element.is_displayed() and element.is_displayed():
        logging.info("Moderninha Pro 2 redirecionando corretamente")
    else:
        logging.error("Ocorreu um erro ao validar o redirecionamento da Moderninha Pro 2 na grade de maquininhas mais vendidas")
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()
        
    element = wait_and_log_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[6]/div/div/div[3]/div')
    if element.is_displayed() and element.is_displayed():
        logging.info("Seta para o lado da grade funcionando corretamente")
    else:
        logging.error("Ocorreu um erro ao validar a seta para o lado na grade")    
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()

    element = wait_and_log_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[6]/div/div/div[2]/div/div[5]/div[3]/a[1]')
    if element.is_displayed() and element.is_displayed():
        logging.info("Minizinha Chip 3 redirecionando corretamente")
    else:
        logging.error("Ocorreu um erro ao validar o redirecionamento da Minizinha Chip 3 na grade de maquininhas mais vendidas")
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()
    

    element = wait_and_log_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[5]/section/div[2]/div/a[1]')
    if element.is_displayed() and element.is_displayed():
        element.click()
        logging.info("Clicando em 'Ver Maquininhas'")
        time.sleep(2)
        logging.info(f"{driver.current_url}")
        
    else:
        logging.error("Não foi possivel clicar em 'Ver maquininhas'")
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()



    logging.info('Validando Moderninha Smart 2 da grade')
    element = wait_and_log_clickable_element(driver, By.XPATH, '//*[@id="ps"]/div[1]/div/div[3]')
    element.click()
    element = wait_and_log_clickable_element(driver, By.XPATH, '//*[@id="e2e_product_tile_moderninha_smart_2"]/div/div/div[2]/a[1]')
    if element.is_displayed() and element.is_displayed():
        logging.info("Moderninha Smart 2 do grade redirecionando corretamente")
    else:
        logging.error("Ocorreu um erro ao validar o redirecionamento da Moderninha Smart 2 na grade")
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()


    element = wait_and_log_clickable_element(driver, By.XPATH, '//*[@id="ps"]/div[1]/div/div[3]/div[3]/a')
    if element.is_displayed() and element.is_enabled():
        element.click()
        logging.info(f"Moderninha Smart 2 está visivel, clicavel e sendo direcionado para: {driver.current_url}")
        check_purchase_limit_alert(element, driver, pasta_prints_erros, screenshot_filename)
        remove_one_card_machine(element, driver, pasta_prints_erros, screenshot_filename)
        add_more_products(element, logging)
    else:
        logging.error("Não foi possivel localizar a Moderninha Smart no 2 no header")
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit() 


    element = wait_and_log_clickable_element(driver, By.XPATH, '//*[@id="e2e_product_tile_minizinha_nfc_2"]/div/div/div[2]/a[1]')
    if element.is_displayed() and element.is_enabled():
        element.click()
        logging.info(f"Minizinha NFC 2 do header está visivel, clicavel e sendo direcionado para: {driver.current_url}")
        check_purchase_limit_alert(element, driver, pasta_prints_erros, screenshot_filename)
        remove_one_card_machine(element, driver, pasta_prints_erros, screenshot_filename)
    else:
        logging.error("Não foi possivel localizar a Minizinha NFC 2 no header")
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit() 




    element = wait_and_log_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div[1]/div/div/div[3]/div[2]/div/p[3]/a')
    if element.is_displayed() and element.is_enabled():
        element.click()
        logging.info('Removendo a Minizinha NFC 2 do carrinho')
        
    else:
        logging.error('Não foi possivel remover a Minizinha NFC 2 do carrinho')
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()

    time.sleep(1)














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