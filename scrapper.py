from os import replace
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class Scrapper:
    
    def __init__(self):
        return
    
    @staticmethod
    def extracao(url):
        #valuation_list = []
        #debt_indicators_list = []
        #efficiency_list = []
        #profiability_list = []
        #growth_indicators_list = []
        indicators_list = []

        # instala o drive do chrome evita incompatibilidade
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)
        time.sleep(10)

        # Verifica se existe pop up na página, se sim ele fecha
        popup = driver.find_element_by_xpath(
            "//button[@class='btn-close']")
        if popup:
            popup.click()

        # Captura o html da tabela dos indicadores no site, facilitando a raspagem dos dados
        element_indicators = driver.find_element_by_xpath(
            "//div[@id='indicators-section']//div[@class='indicator-today-container']")

        indicators_table = element_indicators.get_attribute('outerHTML')

        # Captura o html da tabela da cotação atual do ativo
        element_price = driver.find_element_by_xpath(
            "//div[@class='top-info has-special d-flex justify-between flex-wrap']//div[@class='info special w-100 w-md-33 w-lg-20']")

        cotacao_table = element_price.get_attribute('outerHTML')

        # Parseando conteúdo HTML da página
        soup = BeautifulSoup(indicators_table, 'html.parser')
        soup_2 = BeautifulSoup(cotacao_table, 'html.parser')
        print(soup_2)

        # Capturando conteúdo da cotação atual da ação
        price_table = soup_2.find("div", attrs={"class": "d-md-inline-block"})
        price_value = price_table.find("strong", attrs={"class": "value"})
        price_value = price_value.text

        indicators_list.append(price_value)

        # Capturando conteúdo dos indicadores de valuation
        valuation_table = soup.find("div", attrs={"data-group": "0"})
        valuation_itens = valuation_table.findAll("div", attrs={"class": "item"})

        # Capturando conteúdo dos indicadores de endividamento
        debt_table = soup.find("div", attrs={"data-group": "2"})
        debt_itens = debt_table.findAll("div", attrs={"class": "item"})

        # Capturando conteúdo dos indicadores de eficiência
        efficiency_table = soup.find("div", attrs={"data-group": "1"})
        efficiency_itens = efficiency_table.findAll("div", attrs={"class": "item"})

        # Capturando conteúdo dos indicadores de rentabilidade
        profiability_table = soup.find("div", attrs={"data-group": "3"})
        profiability_itens = profiability_table.findAll(
            "div", attrs={"class": "item"})

        # Capturando conteúdo dos indicadores de crescimento
        growth_table = soup.find("div", attrs={"data-group": "4"})
        growth_itens = growth_table.findAll("div", attrs={"class": "item"})

        # Cria uma lista com os indicadores de valuation capturados
        for valuation_item in valuation_itens:
            #title_vi = valuation_item.find("h3", attrs={"class": "title"})
            value_vi = valuation_item.find("strong", attrs={"class": "value"})

            #valuation_list.append([title_vi.text, value_vi.text])
            value = value_vi.text 
            indicators_list.append(value.replace('%',''))    

        # Cria uma lista com os indicadores de endividamento
        for debt_item in debt_itens:
            #title_di = debt_item.find("h3", attrs={"class": "title"})
            value_di = debt_item.find("strong", attrs={"class": "value"})

            #debt_indicators_list.append([title_di.text, value_di.text])
            
            value = value_di.text 
            indicators_list.append(value.replace('%',''))  

        # Cria uma lista com os indicadores de eficiência
        for efficiency_item in efficiency_itens:
            #title_ei = efficiency_item.find("h3", attrs={"class": "title"})
            value_ei = efficiency_item.find("strong", attrs={"class": "value"})

            #efficiency_list.append([title_ei.text, value_ei.text])

            value = value_ei.text 
            indicators_list.append(value.replace('%',''))  

        # Cria uma lista com os indicadores de rentabilidade
        for profiability_item in profiability_itens:
            #title_pi = profiability_item.find("h3", attrs={"class": "title"})
            value_pi = profiability_item.find("strong", attrs={"class": "value"})

            #profiability_list.append([title_pi.text, value_pi.text])

            value = value_pi.text 
            indicators_list.append(value.replace('%',''))  

        # Cria uma lista com os indicadores de crescimento
        for growth_item in growth_itens:
            #title_gi = growth_item.find("h3", attrs={"class": "title"})
            value_gi = growth_item.find("strong", attrs={"class": "value"})

            #growth_indicators_list.append([title_gi.text, value_gi.text])
            
            value = value_gi.text 
            indicators_list.append(value.replace('%',''))      

        driver.quit()
        
        #return valuation_list, debt_indicators_list, efficiency_list, profiability_list, growth_indicators_list
        #print(indicators_list)
        return indicators_list
        
    @staticmethod
    def cria_frame(lista,nome):
        frame = pd.DataFrame(lista)
        frame.to_json(nome+'.json')
        print(frame)

