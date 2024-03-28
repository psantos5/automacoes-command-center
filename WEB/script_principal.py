import time
from script_conversao import conversao, loggerDebug, loggerConversao
from script_reset import reset
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import requests


options = webdriver.ChromeOptions()

driver = webdriver.Chrome(options=options)




def run_automacao():
    
    try:
        conversao()
        
        reset()
    
    except Exception as ex:
        pass

    finally:
        pass


def laguardia_automacao():
    while True:
        run_automacao()
        loggerConversao.info("Próximo teste daqui 2 horas.")
        time.sleep(1800)


if __name__ == "__main__": 
    laguardia_automacao()
