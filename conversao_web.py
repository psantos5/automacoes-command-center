import logging
import os
import time

from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,ElementNotVisibleException,InvalidSelectorException,ElementNotInteractableException,NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


nome_arquivo_py = os.path.splitext(os.path.basename(__file__))[0]
pasta_prints_erros = 'erros_screenshot'
data_hora_atual = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
screenshot_filename = f"{nome_arquivo_py}_{data_hora_atual}_erro.png"


script_directory = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(script_directory, 'logs')
if not os.path.exists(log_file_path):
    os.makedirs(log_file_path)

log_filename = f"{log_file_path}/{nome_arquivo_py}_.log"
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def wait_and_log_visible_and_clickable_element(driver, by, value):
    element = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((by, value)) and
        EC.element_to_be_clickable((by, value))
    )
    return element

def add_more_products(element, logging):
    xpath = '/html/body/div[1]/form/div[3]/a'

    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    element.click()

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


def check_purchase_limit_alert(element, driver, pasta_prints_erros, screenshot_filename):
    element_more = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div/div/div/div[3]/div[1]/div/div[1]/button[2]')
    element_more.click()
    element_alert_limit = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '//*[@id="cart-item__limit__alert-message"]')
    if element_alert_limit.is_displayed() and element_alert_limit.is_enabled():
        pass
        #logging.info("Alerta de limite de compra está aparecendo com sucesso")
    else:
        logging.error("Alerta de limite de compra não está aparecendo")
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()

    
def remove_one_card_machine_cart(element, driver, pasta_prints_erros, screenshot_filename):
    element_remove_one_card_machine_cart = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div/div/div/div[3]/div[1]/div/div[1]/button[1]')
    if element_remove_one_card_machine_cart.is_displayed() and element_remove_one_card_machine_cart.is_enabled():
        element_remove_one_card_machine_cart.click()
    else:
        logging.error('Não foi possivel clicar no botão '-'')
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()

def log_execution_time(start_time, end_time, action_name):
    duration = end_time - start_time
    if duration < 1:
        formatted_duration = f"{duration * 1000:.2f} milissegundos"
    else:
        formatted_duration = f"{duration:.2f} segundos"
    logging.info(f"{action_name} executado em {formatted_duration}")

def verificar_texto(driver, id, expected_text, mensagem_erro, pasta_prints_erros, screenshot_filename):

    elemento = WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.ID, id), expected_text))
    if elemento:
        logging.info("sucesso")

    logging.error(mensagem_erro)
    print_erro(driver, pasta_prints_erros, screenshot_filename)
    return False


try:

    driver = webdriver.Chrome()
    driver.get("https://loja.pagseguro.uol.com.br/")
    start_time = time.time()
    driver.maximize_window()
    logging.info("Abrindo pagina")
    logging.info(f"URL Aberta: {driver.current_url}")
    end_time = time.time()
    log_execution_time(start_time, end_time, "Tempo de carregamento da pagina:")
    
    duration = end_time - start_time
    if duration > 2:
        logging.warning(f"Atenção, pagina demorou mais de 1 segundo para carregar: {driver.current_url}")      
    else:
        pass

    logging.info("CENARIO: Iniciando teste de adição e remoção das maquininhas no carrinho")

    element_moderninha_pro_2_header = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '//*[@id="ps"]/div[1]/div/div[1]/div[3]/a')
    if element_moderninha_pro_2_header.is_displayed() and element_moderninha_pro_2_header.is_enabled():
        element_moderninha_pro_2_header.click()
        check_purchase_limit_alert(element_moderninha_pro_2_header, driver, pasta_prints_erros, screenshot_filename)
        remove_one_card_machine_cart(element_moderninha_pro_2_header, driver, pasta_prints_erros, screenshot_filename)
        add_more_products(element_moderninha_pro_2_header, logging)
    else:
        logging.error("Não foi possivel localizar a Moderninha Pro 2 no header")
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit() 

    element_moderninha_plus_2_header = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '//*[@id="ps"]/div[1]/div/div[2]/div[3]/a')
    if element_moderninha_plus_2_header.is_displayed() and element_moderninha_plus_2_header.is_enabled():
        element_moderninha_plus_2_header.click()
        check_purchase_limit_alert(element_moderninha_plus_2_header, driver, pasta_prints_erros, screenshot_filename)
        remove_one_card_machine_cart(element_moderninha_plus_2_header, driver, pasta_prints_erros, screenshot_filename)
    else:
        logging.error("Não foi possivel localizar a Moderninha Plus 2 no header")
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()


    element_remove_cart_moderninha_pro_2 = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div[1]/div/div/div[3]/div[2]/div/p[3]/a')
    if element_remove_cart_moderninha_pro_2.is_displayed() and element_remove_cart_moderninha_pro_2.is_enabled():
        element_remove_cart_moderninha_pro_2.click()
    else:
        logging.error('Não foi possivel remover a Moderninha Pro 2 do carrinho')
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()

    time.sleep(1)


    element_moderninha_pro_2_cart = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div[1]/div/div[1]/p/a')
    if element_moderninha_pro_2_cart.is_displayed() and element_moderninha_pro_2_cart.is_enabled():
        element_moderninha_pro_2_cart.click()
    else:
        logging.error('Não foi possivel adicionar a Moderninha Pro 2 no carrinho novamente')
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()

    element_remove_cart_moderninha_plus_2 = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div[2]/div/div/div[3]/div[2]/div/p[3]/a')
    if element_remove_cart_moderninha_plus_2.is_displayed() and element_remove_cart_moderninha_plus_2.is_enabled():
        element_remove_cart_moderninha_plus_2.click()
    else:
        logging.error('Não foi possivel remover a Moderninha Plus 2 do carrinho')
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()

    element_moderninha_plus_2_cart = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div[2]/div/div[1]/p/a')
    if element_moderninha_plus_2_cart.is_displayed() and element_moderninha_plus_2_cart.is_enabled():
        element_moderninha_plus_2_cart.click()
    else:
        logging.error('Não foi possivel adicionar a Moderninha Plus 2 no carrinho novamente')
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()


    element_clean_cart_moderninha_pro_2 = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div[1]/div/div/div[3]/div[2]/div/p[3]/a')
    if element_clean_cart_moderninha_pro_2.is_displayed() and element_clean_cart_moderninha_pro_2.is_enabled():
        element_clean_cart_moderninha_pro_2.click()
        time.sleep(1)
    else: 
        logging.error("Ocorreu um erro ao remover a Moderninha Pro 2")
        print_erro(driver, pasta_prints_erros, screenshot_filename)

    element_clean_cart_moderninha_plus_2 = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div[2]/div/div/div[3]/div[2]/div/p[3]/a')
    if element_clean_cart_moderninha_plus_2.is_displayed() and element_clean_cart_moderninha_plus_2.is_enabled():
        element_clean_cart_moderninha_plus_2.click()
        time.sleep(1)
    else: 
        logging.error("Ocorreu um erro ao remover a Moderninha Plus 2")
        print_erro(driver, pasta_prints_erros, screenshot_filename)

    expected_text = "Seu carrinho está vazio"
    element_cart_empty = WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '/html/body/div[1]/form/div[5]/section/div[2]/h2'), expected_text))
    if element_cart_empty:
        pass
    else:
        logging.error("Não foi possivel deixar o carrinho vazio, é ncessario que o carrinho esteja vazio para seguir com o teste")   
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()

    
    logging.info('CENARIO: Grade de maquininhas mais vendidas (ainda no carrinho)')
    
    element_maquininha_1_grade_mais_vendidas = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[6]/div/div/div[2]/div/div[1]/div[3]/a[1]')
    element_maquininha_1_grade_mais_vendidas.click()
    element_maquininha_1_grade_mais_vendidas = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div/div/div/div[2]/h3/img')))
    if element_maquininha_1_grade_mais_vendidas:
        remove_maquininha_1_carrinho = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div/div/div/div[3]/div[2]/div/p[3]/a')
        remove_maquininha_1_carrinho.click()
    else:
        logging.error("Ocorreu um erro ao validar a maquininha da grade")   
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()

    element_maquininha_2_grade_mais_vendidas = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[6]/div/div/div[2]/div/div[2]/div[3]/a[1]')
    element_maquininha_2_grade_mais_vendidas.click()
    element_maquininha_2_grade_mais_vendidas = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div/div/div/div[2]/h3/img')))
    if element_maquininha_2_grade_mais_vendidas:
        remove_maquininha_2_carrinho = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div/div/div/div[3]/div[2]/div/p[3]/a')
        remove_maquininha_2_carrinho.click()
    else:
        logging.error("Ocorreu um erro ao validar a maquininha da grade")   
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()

    element_maquininha_3_grade_mais_vendidas = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[6]/div/div/div[2]/div/div[3]/div[3]/a[1]')
    element_maquininha_3_grade_mais_vendidas.click()
    element_maquininha_3_grade_mais_vendidas = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div/div/div/div[2]/h3/img')))
    if element_maquininha_3_grade_mais_vendidas:
        remove_maquininha_3_carrinho = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div/div/div/div[3]/div[2]/div/p[3]/a')
        remove_maquininha_3_carrinho.click()
    else:
        logging.error("Ocorreu um erro ao validar a maquininha da grade")   
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()

    element_maquininha_3_grade_mais_vendidas = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[6]/div/div/div[2]/div/div[4]/div[3]/a[1]')
    element_maquininha_3_grade_mais_vendidas.click()
    element_maquininha_3_grade_mais_vendidas = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div/div/div/div[2]/h3/img')))
    if element_maquininha_3_grade_mais_vendidas:
        remove_maquininha_3_carrinho = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div/div/div/div[3]/div[2]/div/p[3]/a')
        remove_maquininha_3_carrinho.click()
    else:
        logging.error("Ocorreu um erro ao validar a maquininha da grade")   
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()

    element_maquininha_3_grade_mais_vendidas = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[6]/div/div/div[2]/div/div[5]/div[3]/a[1]')
    element_maquininha_3_grade_mais_vendidas.click()
    element_maquininha_3_grade_mais_vendidas = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div/div/div/div[2]/h3/img')))
    if element_maquininha_3_grade_mais_vendidas:
        remove_maquininha_3_carrinho = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div/div/div/div[3]/div[2]/div/p[3]/a')
        remove_maquininha_3_carrinho.click()
    else:
        logging.error("Ocorreu um erro ao validar a maquininha da grade")   
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()

    element_ver_maquininhas = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[5]/section/div[2]/div/a[1]')
    element_ver_maquininhas.click()
    time.sleep(4)

    url_atual = driver.current_url

    if 'https://pagseguro.uol.com.br/para-seu-negocio/maquininhas' in url_atual:
        logging.info(f'CENARIO: Continuando teste de adição e remoção de maquininha, redirecionado para:{url_atual}')

        element_minizinha_nfc2 = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '//*[@id="ps"]/div[1]/div[2]/div/div[2]/div/div[1]/div[3]/a[1]')
        if element_minizinha_nfc2.is_displayed() and element_minizinha_nfc2.is_enabled():
            element_minizinha_nfc2.click()
            check_purchase_limit_alert(element_minizinha_nfc2, driver, pasta_prints_erros, screenshot_filename)
            remove_one_card_machine_cart(element_minizinha_nfc2, driver, pasta_prints_erros, screenshot_filename)
            add_more_products(element_minizinha_nfc2, logging)     
        else:
            logging.info("Ocorreu um erro durante o redirecionamento da Minizinha NFC 2")


        element_moderninha_pro2 = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '//*[@id="ps"]/div[1]/div[2]/div/div[2]/div/div[2]/div[3]/a[1]')
        if element_moderninha_pro2.is_displayed() and element_moderninha_pro2.is_enabled():
            element_moderninha_pro2.click()
            check_purchase_limit_alert(element_moderninha_pro2, driver, pasta_prints_erros, screenshot_filename)
            remove_one_card_machine_cart(element_moderninha_pro2, driver, pasta_prints_erros, screenshot_filename)
            element_remove = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div[1]/div/div/div[3]/div[2]/div/p[3]/a')
            element_remove.click()
            element_remove2 = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div[2]/div/div/div[3]/div[2]/div/p[3]/a')
            element_remove2.click() 
            add_more_products(element_moderninha_pro2, logging)
        else:
            logging.info("Ocorreu um erro durante o redirecionamento da Moderninha Pro 2")

        element_minizinha_chip3 = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '//*[@id="ps"]/div[1]/div[2]/div/div[2]/div/div[3]/div[3]/a[1]')
        if element_minizinha_chip3.is_displayed() and element_minizinha_chip3.is_enabled():
            element_minizinha_chip3.click()
            check_purchase_limit_alert(element_minizinha_chip3, driver, pasta_prints_erros, screenshot_filename)
            remove_one_card_machine_cart(element_minizinha_chip3, driver, pasta_prints_erros, screenshot_filename)
            add_more_products(element_minizinha_chip3, logging)
        else:
            logging.info("Ocorreu um erro durante o redirecionamento da Minizinha Chip 3")


        element_moderninha_plus2 = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '//*[@id="ps"]/div[1]/div[2]/div/div[2]/div/div[4]/div[3]/a[1]')
        if  element_moderninha_plus2.is_displayed() and element_moderninha_plus2.is_enabled():
            element_moderninha_plus2.click()
            check_purchase_limit_alert(element_moderninha_plus2, driver, pasta_prints_erros, screenshot_filename)
            remove_one_card_machine_cart(element_moderninha_plus2, driver, pasta_prints_erros, screenshot_filename)
            element_remove = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div[1]/div/div/div[3]/div[2]/div/p[3]/a')
            element_remove.click()
            element_remove2 = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div[2]/div/div/div[3]/div[2]/div/p[3]/a')
            element_remove2.click() 
            add_more_products(element_moderninha_plus2, logging)
        else:
            logging.info("Ocorreu um erro durante o redirecionamento da Moderninha Plus 2")

        
        element_moderninha_smart2 = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '//*[@id="ps"]/div[1]/div[2]/div/div[2]/div/div[5]/div[3]/a[1]')
        if  element_moderninha_smart2.is_displayed() and element_moderninha_smart2.is_enabled():
            element_moderninha_smart2.click()
            check_purchase_limit_alert(element_moderninha_smart2, driver, pasta_prints_erros, screenshot_filename)
            element_cartao_gratis = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[3]/div[2]/div[2]/div[3]/div/div[1]/label/input')
            element_cartao_gratis.click()

            logging.info("CENARIO: Validando se opções de cartão da conta gratis e cadastrar chave pix estão funcionais")
            expected_text_cartao_gratis = "Cartão da Conta"
            element_cart_cartao_gratis = WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '/html/body/div[1]/form/div[4]/div[2]/div/dl/dt[3]'), expected_text_cartao_gratis))
            if element_cartao_gratis:
                pass
            else:
                logging.error("Mensagem de cartão da conta gratis não esta aparecendo")

            element_cadastrar_pix = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[4]/div[1]/div/div/label/input[1]')
            element_cadastrar_pix.click()

            element_continuar_carrinho = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '/html/body/div[1]/form/div[4]/div[2]/div/div[3]/button')
            element_continuar_carrinho.click()
        else:
            logging.info("Ocorreu um erro durante o redirecionamento da Moderninha Smart 2")


    elif 'https://loja.pagseguro.uol.com.br/' in url_atual:
        logging.info(f'Redirecionado para: {url_atual}')

    logging.info("CENARIO: Realizando login na conta após carrinho")
    element_login_email = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '//*[@id="email"]')
    element_login_email.click()
    acesso = '' #Inserir aqui seu login de acesso aqui (E-mail, CPF ou Telefone)
    element_login_email.send_keys(acesso)
    value_acesso = element_login_email.get_attribute("value")
    if acesso == value_acesso:

           element_continuar_login = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '//*[@id="continue-button"]')
           element_continuar_login.click()

           element_outro_email = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div[2]/div/div/form/div[1]/p/a')
           element_outro_email.click()
           expected_text_outro_email = "Insira um e-mail para começar"
           element_login_outro_email = WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div[2]/div/div/form/div[1]/label'), expected_text_outro_email))
           if element_login_outro_email:
                element_login_email_outro = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '//*[@id="email"]')
                element_login_email_outro.click()
                acesso = '' #Inserir aqui seu login de acesso aqui (E-mail, CPF ou Telefone)
                element_login_email_outro.send_keys(acesso)
                element_continuar_login_outro_email = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '//*[@id="continue-button"]')
                element_continuar_login_outro_email.click()
                element_login_senha = wait_and_log_visible_and_clickable_element(driver, By. XPATH, '//*[@id="password"]')
                element_login_senha.click()
                senha = '' #Inserir a senha da sua conta aqui
                element_login_senha.send_keys(senha)
                element_senha = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '//*[@id="continue-button"]')
                element_senha.click()
                time.sleep(20)
           else:
               logging.error('Não foi possivel localizar o conteudo da variavel "expected_text_outro_email"')
                     
    else:
        logging.error(f"Erro ao inserir dados de acesso")

    logging.info("CENARIO: Checkout, endereço de entrega") 

    expected_text_endereco_entrega_rua = "" #Inserir aqui o endereço da rua que aparece, copiar e colar do jeito que está
    element_endereco_rua = WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="step-shipping"]/form/div[1]/div[2]/div/div/p[1]'), expected_text_endereco_entrega_rua))
    if element_cart_empty:
        pass
    else:
        logging.error("Nome da rua não esta aparecendo corretamente")   
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()

    expected_text_endereco_entrega_cidade = "" #Inserir aqui o endereço da cidade que aparece, copiar e colar do jeito que está
    element_endereco_cidade = WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="step-shipping"]/form/div[1]/div[2]/div/div/p[2]'), expected_text_endereco_entrega_cidade))
    if element_cart_empty:
        pass
    else:
        logging.error("Nome da cidade não esta aparecendo corretamente")   
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()

    expected_text_endereco_entrega_cep = "" #Inserir aqui o CEP  que aparece, copiar e colar do jeito que está, até mesmo o texto CEP
    element_endereco_cidade = WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="step-shipping"]/form/div[1]/div[2]/div/div/p[3]'), expected_text_endereco_entrega_cep))
    if element_cart_empty:
        pass
    else:
        logging.error("Nome da cidade não esta aparecendo corretamente")   
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        driver.quit()

    logging.info("CENARIO: Editando o endereço de entrega")
    element_editar_endereco = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '//*[@id="form-button-freight-edit"]')
    element_editar_endereco.click()
    element_inserir_cep = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '//*[@id="step-shipping"]/form/div[1]/div[2]/div/div[1]/div/div/div/div/input')
    element_inserir_cep.clear()
    cep = "18652132" 
    element_inserir_cep.send_keys(cep)

    element_inserir_numero = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '//*[@id="shipping-street-number"]/div/div/div[1]/input')
    numero = "173"
    element_inserir_numero.send_keys(numero)

    element_continuar_endereco = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '//*[@id="form-button-shipping-continue"]')
    if element_continuar_endereco:

        element_inserir_cep = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '//*[@id="step-shipping"]/form/div[1]/div[2]/div/div[1]/div/div/div/div/input')
        element_inserir_cep.clear()
        cep2 = "05653070" 
        element_inserir_cep.send_keys(cep2)
        element_inserir_numero = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '//*[@id="shipping-street-number"]/div/div/div[1]/input')
        numero2 = "173"
        element_inserir_numero.send_keys(numero2)
        element_continuar_endereco = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '//*[@id="form-button-shipping-continue"]')
        element_continuar_endereco.click()
        time.sleep(10)

    else:
        logging.error("Endereço não retornou corretamente ou botão de continuar esta indisponivel")

    logging.info("CENARIO: Forma de Pagamento (PIX)")
    element_pagamento_pix = wait_and_log_visible_and_clickable_element(driver, By.XPATH, '//*[@id="tab-button-PIX"]/span')
    element_pagamento_pix.click()















except TimeoutException as e:
    

    try:
        element = driver.find_element(By.XPATH, 'xpath_element')
        if not element.is_displayed():
            raise ElementNotVisibleException("Elemento não está visível.")
        print_erro(driver, pasta_prints_erros, screenshot_filename)
        
        
    except NoSuchElementException as ex:
        logging.error(f"Elemento não encontrado  '{str(ex)}")
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