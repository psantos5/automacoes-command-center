import logging
import os
import time

from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchWindowException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
import requests



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



def configurarLoggerSenha(nome_arquivo='resetSenha.log'):

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



def configurarLoggerDebugSenha(nome_arquivo='resetSenha.log'):

    nome_arquivo = os.path.join(log_file_path, nome_arquivo)
    logging.basicConfig(level=logging.DEBUG, 
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

loggerSenha = configurarLoggerSenha()
loggerDebug = configurarLoggerDebugSenha()



def logExecutionTime(startTime, endTime, actionName):
    duration = endTime - startTime
    if duration < 1:
        formatted_duration = f"{duration * 1000:.2f} milissegundos"
    else:
        formatted_duration = f"{duration:.2f} segundos"
    loggerSenha.info(f"{actionName} executado em {formatted_duration}")



options = webdriver.ChromeOptions()
"""options.add_argument("--window-size=1920,1080")
options.add_argument('--headless')"""


driver = webdriver.Chrome(options=options)
urlAtualErro = driver.current_url

pastaPrintsErros = 'erros_screenshot'
dataHoraAtual = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
screenshot_filename = f"reset_{dataHoraAtual}_erro.png"
acesso = ''
senha = ''


teams_webhook_url = "https://uolinc.webhook.office.com/webhookb2/cbbababe-5ee6-40e7-b78b-fd01ab37edf4@7575b092-fc5f-4f6c-b7a5-9e9ef7aca80d/IncomingWebhook/1b5bdebb7b324a69ba9bd17d203350f6/5e25d5d6-c12d-4329-9ea4-63ea811be36b"

def enviar_mensagem_para_teams_sucesso(mensagem):

    horario_teste = datetime.now().strftime("%d/%m/%Y %H:%M:%S")


    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "0076D7",
        "summary": "Teste realizado com sucesso!",
        "sections": [{
            "activityTitle": "Teste de Reset Senha - WEB realizado com sucesso!",
            "activitySubtitle": f"Horario: {horario_teste}",
            "activityImage": "https://static.vecteezy.com/system/resources/thumbnails/010/956/188/small/check-mark-3d-icon-button-green-success-illustration-simple-element-with-transparent-background-png.png",  # URL da imagem que você deseja exibir
            "facts": [
                {
                    "name": "Detalhes:",
                    "value": mensagem
                },

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


def enviar_mensagem_para_teams_error(mensagem):

    horario_teste = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "0076D7",
        "summary": "Erros, automação",
        "sections": [{
            "activityTitle": "Erro durante o teste: RESET DE SENHA - WEB",
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

def reset():
    
    try:

        
        driver.get("https://pagseguro.uol.com.br/banco-completo-para-empreendedor")
        url = driver.current_url

        driver.maximize_window()
        startTimelog = time.time()
        startTime = time.time()

        loggerSenha.info(f"CENARIO: INICIANDO teste, pagina aberta:{url}")

        endTime = time.time()
        duration = endTime - startTime
        if duration > 3:
            loggerSenha.warning("ATENÇÃO: Pagina demorou mais de 3 segundos para carregar")
        else:
            logExecutionTime(startTime, endTime, "TEMPO de carregamento da pagina:")


        loggerSenha.info("CENARIO: ACESSANDO conta")
        element_Entrar = driver.find_element(By.XPATH, '//*[@id="__next"]/header/div/div[2]/div/div/a[1]')
        element_Entrar.click()


        time.sleep(2)

        element_Acesso =  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/main/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/form/div/div/label')))
        element_Acesso.click()
        element_AcessoInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="user"]')))
        element_AcessoInput.send_keys(acesso)

        element_Continuar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="continue"]')))
        element_Continuar.click()


        startTime = time.time()
        element_EsqueciSenha = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="forgotPassword"]')))
        endTime= time.time()
        logExecutionTime(startTime, endTime, "LOCALIZAÇÃO da conta:")
        tempolocalizarConta = endTime - startTime
        if tempolocalizarConta > 5:
            loggerSenha.warning("ATENÇÃO: Pagina demorou mais de 5 segundos para localizar sua conta")
            driver.quit()
        else:
            element_EsqueciSenha.click()



        loggerSenha.info("CENARIO: RECUPERAÇÃO de senha:")

        time.sleep(1)

        loggerSenha.info("SMS")
        element_SMS = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sms-factor"]/div[2]/span[1]')))
        element_SMS.click()


        time.sleep(8)

        element_Voltar = driver.find_element(By.XPATH, '//*[@id="back-button"]')
        element_Voltar.click()

        time.sleep(1)
        element_AcessoSenha = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div[2]/div/div[1]/div/div/div/form/div/div/label')))
        element_AcessoSenha.click()
        element_AcessoSenhaInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="credential-input"]')))
        element_AcessoSenhaInput.send_keys(acesso)
        element_EsqueciSenhaContinuar = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div[2]/div/div[1]/div/div/div/form/button')
        element_EsqueciSenhaContinuar.click()


        loggerSenha.info("E-MAIL")
        element_EMAIL = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="email-factor"]/div[2]/span[2]')))
        element_EMAIL.click()
        endTimelog = time.time()
        timeLog = endTimelog - startTime
        enviar_mensagem_para_teams_sucesso(mensagem=f"Duração do teste: {timeLog:.2f} segundos")

    except NoSuchElementException as ex:
        urlAtualErro = driver.current_url

        loggerDebug.error(f"Elemento não encontrado com o XPath: {str(ex)} - {urlAtualErro}")
        print_erro(driver, pastaPrintsErros, screenshot_filename)
        enviar_mensagem_para_teams_error(mensagem=f" - Elemento não encontrado com o XPath: {str(ex)} - {urlAtualErro}")

    except TimeoutException as e:
        urlAtualErro = driver.current_url
        
        loggerDebug.error("TimeoutException durante a execução: %s\n%s\nURL: %s", str(e), traceback.format_exc(), urlAtualErro)
        enviar_mensagem_para_teams_error(mensagem=f" - TimeoutException durante a execução: {str(e)},\n - {traceback.format_exc()}\n - URL: {urlAtualErro}")
        print_erro(driver, pastaPrintsErros, screenshot_filename)

    except NoSuchWindowException as e:
        urlAtualErro = driver.current_url
        
        loggerDebug.error("Navegador encerrado durante execução do teste: %s\n%s\nURL: %s", str(e), traceback.format_exc() - urlAtualErro)
        enviar_mensagem_para_teams_error(mensagem=f" - Navegador encerrado durante execução do teste: {str(e)} - {urlAtualErro}")
        print_erro(driver, pastaPrintsErros, screenshot_filename)
        
    except WebDriverException as e:
        urlAtualErro = driver.current_url
        
        loggerDebug.error("Houve mudanças repentinamente na pagina que ocasionou erro: %s\n%s\nURL: %s", str(e), traceback.format_exc(), urlAtualErro)
        enviar_mensagem_para_teams_error(mensagem=f" - Houve mudanças repentinamente na pagina que ocasionou erro: {str(e)} - {urlAtualErro}")
        print_erro(driver, pastaPrintsErros, screenshot_filename)



    finally:
        endTime = time.time()
        logExecutionTime(startTime, endTime, "DURAÇÃO do teste:")
        logging.shutdown()

if __name__ == "__main__": 
    reset()

