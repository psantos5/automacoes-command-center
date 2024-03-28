from selenium import webdriver
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchWindowException, WebDriverException
from cartao import  cartaoCPF, cartaoNome, cartaoNum, cartaoCVV, cartaoVal
import traceback
import requests





def scrollUP ():
    actions = ActionChains(driver)
    actions.send_keys(Keys.PAGE_UP).perform()


def scrollDown ():
    actions = ActionChains(driver)
    actions.send_keys(Keys.PAGE_DOWN).perform()


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
    

script_directory = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(script_directory, 'logs')
if not os.path.exists(log_file_path):
    os.makedirs(log_file_path)


def configurarLogger(nome_arquivo='conversaoWeb.log'):

    nome_arquivo = os.path.join(log_file_path, nome_arquivo)
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S',  
                        filename=nome_arquivo,  
                        filemode='a')

    logger = logging.getLogger()

    
    if not logger.handlers:

        file_handler = logging.FileHandler(nome_arquivo, mode='a')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))


        logger.addHandler(file_handler)

    return logger




def configurarLoggerDebug(nome_arquivo='conversaoWeb.log'):

    nome_arquivo = os.path.join(log_file_path, nome_arquivo)
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s', 
                        datefmt='%d/%m/%Y %H:%M:%S', 
                        filename=nome_arquivo,  
                        filemode='a')

    logger = logging.getLogger()

    
    if not logger.handlers:

        file_handler = logging.FileHandler(nome_arquivo, mode='a')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))


        logger.addHandler(file_handler)

    return logger






loggerConversao = configurarLogger()
loggerDebug = configurarLoggerDebug()



teams_webhook_url = "https://uolinc.webhook.office.com/webhookb2/cbbababe-5ee6-40e7-b78b-fd01ab37edf4@7575b092-fc5f-4f6c-b7a5-9e9ef7aca80d/IncomingWebhook/1b5bdebb7b324a69ba9bd17d203350f6/5e25d5d6-c12d-4329-9ea4-63ea811be36b"

def enviar_mensagem_para_teams_error(mensagem):

    horario_teste = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "0076D7",
        "summary": "Erros, automação",
        "sections": [{
            "activityTitle": "Erro durante o teste: JORNADA DE CONVERSÃO - WEB",
            "activitySubtitle": f"Horario: {horario_teste}",
            "activityImage": "https://adaptivecards.io/content/cats/3.png",  # URL da imagem que você deseja exibir
            "facts": [
                {
                    "name": "Detalhes do erro:",
                    "value": mensagem
                }
            ]
        }],
        "potentialAction": [{
            "@type": "ActionCard",
            "name": "Abrir chamado",
            "actions": [{
                "@type": "OpenUri",
                "name": "Abrir chamado",
                "targets": [{
                    "os": "default",
                    "uri": "https://jiraps.atlassian.net/servicedesk/customer/portal/5/group/2422/create/5327"
                }]
            }]
        }]
    }

    try:
        # Envia mensagem para o Teams
        requests.post(teams_webhook_url, json=payload)
    except Exception as e:
        # Registra erro no log se houver problema no envio para o Teams
        loggerDebug.error(f"Erro ao enviar mensagem para o Teams: {e}")


def enviar_mensagem_para_teams_sucesso(mensagem):

    horario_teste = datetime.now().strftime("%d/%m/%Y %H:%M:%S")


    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "0076D7",
        "summary": "Teste realizado com sucesso!",
        "sections": [{
            "activityTitle": "Teste de Conversão realizado com sucesso!",
            "activitySubtitle": f"Horario: {horario_teste}",
            "activityImage": "https://static.vecteezy.com/system/resources/thumbnails/010/956/188/small/check-mark-3d-icon-button-green-success-illustration-simple-element-with-transparent-background-png.png",  # URL da imagem que você deseja exibir
            "facts": [
                {
                    "name": "Detalhes:",
                    "value": mensagem
                }

            ]
        }],
        "potentialAction": [{
            "@type": "ActionCard",
            "name": "Abrir chamado",
            "actions": [{
                "@type": "OpenUri",
                "name": "Preencher Planilha",
                "targets": [{
                    "os": "default",
                    "uri": "https://uolinc.sharepoint.com/:x:/r/sites/Laguardia-Comunicaointerna/_layouts/15/Doc.aspx?sourcedoc=%7B4A2CC996-8410-4D47-9245-F4B48792ACC5%7D&file=teste_de_automacao.xlsm&action=default&mobileredirect=true&isSPOFile=1&clickparams=eyJBcHBOYW1lIjoiVGVhbXMtRGVza3RvcCIsIkFwcFZlcnNpb24iOiIxNDE1LzIzMTEzMDI2MjAyIiwiSGFzRmVkZXJhdGVkVXNlciI6ZmFsc2V9"
                }]
            }]
        }]
    }

    try:
        # Envia mensagem para o Teams
        requests.post(teams_webhook_url, json=payload)
    except Exception as e:
        # Registra erro no log se houver problema no envio para o Teams
        loggerDebug.error(f"Erro ao enviar mensagem para o Teams: {e}")







def finalizarCompra():
    XPath = '//*[@id="step-payment"]/div/div[2]/div/div/form/div[2]'

    element_FinalizarCompra = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, XPath)))
    if element_FinalizarCompra.is_displayed() and element_FinalizarCompra.is_enabled():
        loggerConversao.info("Botão de 'FInalizar Compra' aparecendo corretamente para o cliente")
        time.sleep(1)
    else:
        loggerConversao.error("Botão de finalizar compra não estã clicavel para o usuario, validar informações do cartão")
        driver.quit()

def logExecutionTime(startTime, endTime, actionName):
    duration = endTime - startTime
    if duration < 1:
        formattedDuration = f"{duration * 1000:.2f} milissegundos"
    else:
        formattedDuration = f"{duration:.2f} segundos"
    loggerConversao .info(f"{actionName} executado em {formattedDuration}")


options = webdriver.ChromeOptions()



driver = webdriver.Chrome(options=options)





pasta_prints_erros = 'erros_screenshot'
data_hora_atual = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
screenshot_filename = f"conversao_{data_hora_atual}_erro.png"
acesso = ''
senha = ''




def conversao():
    urlAtualErro = driver.current_url

    try:
        

        loggerConversao .info("TESTE - CONVERSÃO WEB")


        driver.get("https://pagseguro.uol.com.br/para-seu-negocio/")
        startTimelog = time.time()
        startTime = time.time()
        url = driver.current_url

        driver.maximize_window()

        loggerConversao .info(f"CENARIO: INICIANDO teste, pagina aberta:{url}")
        endTime = time.time()
        
        
        duration = endTime - startTime
        if duration > 2:
            loggerConversao .warning("Atenção, pagina demorou mais de 2 segundos para carregar")
        else:
            logExecutionTime(startTime, endTime, "TEMPO de carregamento da pagina:")

        loggerConversao .info("CENARIO: COMPRA de maquininha")

        element_pecaja = driver.find_element(By.XPATH, '//*[@id="__next"]/section[1]/div/div/div/a')
        element_pecaja.click()

        scrollDown()
        time.sleep(3)


        

        element_moderninhaPlus2 = driver.find_element(By.XPATH, '//*[@id="plans"]/div[6]/div[1]/div[1]/div/div[4]/a')
        element_moderninhaPlus2.click()

        element_mais = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div/div/div/div[3]/div[1]/div/div[1]/button[2]')))
        element_mais.click()
        time.sleep(2)
        element_menos= WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/form/div[3]/div[1]/div/div/div/div[3]/div[1]/div/div[1]/button[1]')))
        element_menos.click()
        time.sleep(2)

        element_addMaisProdutos = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[3]/a')
        element_addMaisProdutos.click()

        time.sleep(2)
        element_moderninhaPro2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ps"]/div[1]/div[2]/div/div[2]/div/div[2]/div[3]/a[1]')))
        element_moderninhaPro2.click()
        
        time.sleep(1)

        scrollDown()

        time.sleep(1)
        element_carrinhoContinuar = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[4]/div[2]/div/div[3]/button')
        element_carrinhoContinuar.click()

        loggerConversao .info("CENARIO: LOGIN")

        time.sleep(3)

        element_loginEmail = driver.find_element(By.XPATH, '//*[@id="email"]')
        element_loginEmail.send_keys(acesso)

        time.sleep(1)
        element_continuarLogin = driver.find_element(By.XPATH, '//*[@id="continue-button"]')
        element_continuarLogin.click()

        element_senha = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
        element_senha.send_keys(senha)

        time.sleep(1)
        element_continuarLoginSenha = driver.find_element(By.XPATH, '//*[@id="continue-button"]')
        element_continuarLoginSenha.click()

        loggerConversao .info("CENARIO: ENTREGA, editando endereço")

        element_editarEndereco = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="form-button-freight-edit"]')))
        element_editarEndereco.click()

        element_inserirCep = driver.find_element(By.XPATH, '//*[@id="step-shipping"]/form/div[1]/div[2]/div/div[1]/div/div/div/div/input')
        element_inserirCep.clear()
        
        time.sleep(1)

        cep = '18652132'
        element_inserirCep.send_keys(cep)

        time.sleep(1)

        element_inserirNumero = driver.find_element(By.XPATH, '//*[@id="shipping-street-number"]/div/div/div[1]/input')
        numero = '173'
        element_inserirNumero.send_keys(numero)

        time.sleep(1)

        element_continuarEndereco = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="form-button-shipping-continue"]')))
        element_continuarEndereco.click()

        time.sleep(1)


        loggerConversao.info("CENARIO: CHECKOUT {Sem Efetivar}")

        loggerConversao.info("FORMA DE PAGAMENTO: Cartão de Crédto")
        
        element_cartaoCreditoNum = driver.find_element(By.XPATH, '//*[@id="credit-card-number"]/div/div/div[1]/input')
        element_cartaoCreditoNum.send_keys(cartaoNum)
        
        element_bandeiraCartaoCredito = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="credit-cart-brand-container"]/span/span')))
        if element_bandeiraCartaoCredito:
            time.sleep(1)
        else:
            loggerConversao.error("Bandeira do cartão não está aparecendo")    
            driver.quit()                                         
        
        element_cartaoCreditoVal = driver.find_element(By.XPATH, '//*[@id="expiration-date"]/div/div/div[1]/input') 
        element_cartaoCreditoVal.send_keys(cartaoVal)

        time.sleep(1)

        element_cartaoCreditoCVV = driver.find_element(By.XPATH, '//*[@id="cvv-number"]/div/div/div[1]/input')
        element_cartaoCreditoCVV.send_keys(cartaoCVV)

        time.sleep(1)

        element_cartaoCreditoNome = driver.find_element(By.XPATH, '//*[@id="credit-card-full-name"]/div/div/div[1]/input')
        element_cartaoCreditoNome.send_keys(cartaoNome)

        time.sleep(1)

        element_cartaoCreditoCPF = driver.find_element(By.XPATH, '//*[@id="credit_card_cpf"]/div/div/div[1]/input')
        element_cartaoCreditoCPF.send_keys(cartaoCPF)
        finalizarCompra()

        loggerConversao.info("FORMA DE PAGAMENTO: Cartão de Débito")

        element_CartaoDebito = driver.find_element(By.XPATH, '//*[@id="tab-button-DEBIT_CARD"]')
        element_CartaoDebito.click()

        time.sleep(1)

        element_CartaoDebitoNum = driver.find_element(By.XPATH, '//*[@id="debit-card-number"]/div/div/div[1]/input')
        element_CartaoDebitoNum.send_keys(cartaoNum)

        element_bandeiraCartaoDebito = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="credit-cart-brand-container"]/span/span')))
        if element_bandeiraCartaoDebito:
            time.sleep(1)
        else:
            loggerConversao.error("Bandeira do cartão não está aparecendo") 
            driver.quit()

        element_CartaoDebitoVal = driver.find_element(By.XPATH, '//*[@id="expiration-date"]/div/div/div[1]/input')
        element_CartaoDebitoVal.send_keys(cartaoVal)

        time.sleep(1)

        element_CartaoDebitoNome = driver.find_element(By.XPATH, '//*[@id="debit-card-full-name"]/div/div/div[1]/input')
        element_CartaoDebitoNome.send_keys(cartaoNome)

        time.sleep(1)

        element_CartaoDebitoCVV = driver.find_element(By.XPATH, '//*[@id="cvv"]/div/div/div[1]/input')
        element_CartaoDebitoCVV.send_keys(cartaoCVV)
        finalizarCompra()
        


        loggerConversao.info("FORMA DE PAGAMENTO: PIX")


        element_pagamentoPix = driver.find_element(By.XPATH, '//*[@id="tab-button-PIX"]')
        element_pagamentoPix.click()

        time.sleep(1)

        loggerConversao.info("FORMA DE PAGAMENTO: PagBank")

        element_pagbank = driver.find_element(By.XPATH, '//*[@id="tab-button-PAGBANK"]')
        element_pagbank.click()


        time.sleep(1)

        loggerConversao.info("FORMA DE PAGAMENTO: Boleto Bancário")

        element_pagbank = driver.find_element(By.XPATH, '//*[@id="tab-button-BOLETO"]')
        element_pagbank.click()
        endTimelog = time.time()
        timeLog = endTimelog - startTime
        enviar_mensagem_para_teams_sucesso(mensagem=f"Duração do teste: {timeLog:.2f} segundos")




    except NoSuchElementException as ex:
        urlAtualErro = driver.current_url


        loggerDebug.error("Elemento não encontrado com o XPath:", {str(ex)}, urlAtualErro)
        enviar_mensagem_para_teams_error(mensagem=f" - Elemento não encontrado com o XPath:: {str(ex)} - {urlAtualErro}")
        print_erro(driver, pasta_prints_erros, screenshot_filename)

    except TimeoutException as e:
        urlAtualErro = driver.current_url

        loggerDebug.error("TimeoutException durante a execução: %s\n%s\n%s", str(e), traceback.format_exc(), urlAtualErro)
        enviar_mensagem_para_teams_error(mensagem=f" - TimeoutException durante a execução: {str(e)},\n - {traceback.format_exc()}\n - URL: {urlAtualErro}")
        print_erro(driver, pasta_prints_erros, screenshot_filename)

    except NoSuchWindowException as e:
        urlAtualErro = driver.current_url

        loggerDebug.error("Navegador encerrado durante execução do teste: %s", str(e), traceback.format_exc(), urlAtualErro)
        enviar_mensagem_para_teams_error(mensagem=f" - Navegador encerrado durante execução do teste: {str(e)} - {urlAtualErro}")

        print_erro(driver, pasta_prints_erros, screenshot_filename)
        
    except WebDriverException as e:
        urlAtualErro = driver.current_url
        
        loggerDebug.error("Houve mudanças repentinamente na pagina que ocasionou erro:", str(e), traceback.format_exc(), urlAtualErro)
        enviar_mensagem_para_teams_error(mensagem=f" - Houve mudanças repentinamente na pagina que ocasionou erro: {str(e)} - {urlAtualErro}")
        print_erro(driver, pasta_prints_erros, screenshot_filename)



    finally:
        endTime = time.time()
        logExecutionTime(startTime, endTime, "DURAÇÃO do teste:")
        logging.shutdown()





if __name__ == "__main__": 
    conversao()
