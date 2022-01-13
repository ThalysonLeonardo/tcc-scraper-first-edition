import xlsxwriter
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from scrapper import Scrapper

#Url com os códigos das ações na bovespa
url_stocks_raw_br = 'https://raw.githubusercontent.com/ThalysonLeonardo/BOT-Financial-Scraper/main/a%C3%A7%C3%B5es-c%C3%B3digos2.csv'
stocks = pd.read_csv(url_stocks_raw_br,error_bad_lines=False)

#Url base para consulta no "Status Invest"
base_url_br = 'https://statusinvest.com.br/acoes/'

#Iniciando as colunas do frame
frame_columns = ['Código', 'Dividend Yield(%)', 'P/L', 'P/VPA', 'M. Liquida(%)', 'DB/PL', 'ROE(%)', 'EV/EBIT']

#Inciando o frame com as colunas pré-setadas
final_dataFrame = pd.DataFrame(columns=frame_columns)

#Gerando o Frame Final com os indicadores ainda vazios
for stock in stocks['Ticker']:
    target_url = base_url_br + stock

    #valuation_list,debt_indicators_list,efficiency_list,profiability_list,growth_indicators_list = Scrapper.extracao(target_url)
    indicators_list = Scrapper.extracao(target_url)
    #Scrapper.cria_frame(indicators_list,'Indicators')

    final_dataFrame = final_dataFrame.append(
        pd.Series(
            [
                stock,
                indicators_list[0],
                indicators_list[1],
                indicators_list[3],
                indicators_list[23],
                indicators_list[14],
                indicators_list[24],
                indicators_list[4]
            ],
            index = frame_columns
        ),
        ignore_index = True
    )

print(final_dataFrame)
final_dataFrame.to_json('test.json')