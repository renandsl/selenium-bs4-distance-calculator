from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd
from bs4 import BeautifulSoup

df_rs = pd.read_csv(r'coloque_um_arquiv_aqui.csv', encoding='utf8', sep=',')

service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
driver.maximize_window()

url = 'https://www.google.com.br/maps/'

driver.get(url)

df_rs['Km calculado'] = ""

for index, row in df_rs.iterrows():
    valor1 = row['Coordenada Vara Municipio']
    valor2 = row['Coordenada Cidade Estabelecimento']

    if pd.notna(valor2):
        sleep(3)

        try:
            campo_pesquisa = driver.find_element('xpath', '//*[@id="searchboxinput"]')
            campo_pesquisa.clear()
            campo_pesquisa.send_keys(valor1)
            campo_pesquisa.send_keys(Keys.RETURN)
            sleep(2)

            botao = driver.find_element('xpath', '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/button/span').click()
            sleep(2)

            campo_pesquisa2 = driver.find_element('xpath', '//*[@id="sb_ifc50"]/input')
            campo_pesquisa2.clear()
            campo_pesquisa2.send_keys(valor2)
            campo_pesquisa2.send_keys(Keys.RETURN)
            sleep(2)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            km = soup.find('div', class_='ivN21e tUEI8e fontBodyMedium')

            df_rs.at[index, 'km calculado'] = km.text if km else "km não encontrado"

            print(f"Distância entre {valor1} e {valor2}: {km.text}")

        except Exception as e:
            print(f"Erro ao obter distância para {valor1} e {valor2}: {e}")

        finally:
            driver.get(url)
            sleep(3)

df_rs.to_csv(r'seu_arquivo_retornado.csv', index=False, encoding='utf8')
driver.quit()