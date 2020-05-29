from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import csv

linhas = []
columns = []

driver = webdriver.Chrome("../chromedriver")
driver.get('https://liquipedia.net/leagueoflegends/Player_Transfers')
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.close()

for div in soup.find_all('div'):
    if div.has_attr('class') and ' '.join(
            div['class']) == 'divTable mainpage-transfer Ref':
        for subdiv in div.find_all('div'):
            if subdiv.has_attr('class') and ' '.join(
                    subdiv['class']) == 'divHeaderRow':
                columns = [subdiv2.text for subdiv2 in subdiv.find_all('div') if subdiv2.text]
            elif subdiv.has_attr('class') and 'divRow' in ' '.join(subdiv['class']):
                dados = {}
                for subdiv2 in subdiv.find_all('div'):
                    if subdiv2.has_attr('class'):
                        classejoin = ' '.join(subdiv2['class'])
                        if classejoin == 'divCell Date':
                            dados['Date'] = subdiv2.text
                        if classejoin == 'divCell Name':
                            names = subdiv2.find_all('a')
                            dados['Name'] = []
                            for name in names:
                                if name.text:
                                    dados['Name'].append(name.text)
                        if classejoin == 'divCell Team OldTeam':
                            if subdiv2.text == 'None':
                                dados['Old'] = subdiv2.text
                            elif not subdiv2.text:
                                dados['Old'] = subdiv2.find_all('span')[0]['data-highlightingclass']
                            else:
                                dados['Old'] = subdiv2.find_all('span')[0]['data-highlightingclass'] + " " + subdiv2.text
                        if classejoin == 'divCell Team NewTeam':
                            if subdiv2.text == 'None':
                                dados['New'] = subdiv2.text
                            elif not subdiv2.text:
                                dados['New'] = subdiv2.find_all('span')[0]['data-highlightingclass']
                            else:
                                dados['New'] = subdiv2.find_all('span')[0]['data-highlightingclass'] + " " + subdiv2.text
                for name in dados['Name']:
                    linhas.append([dados['Date'], name, dados['Old'], dados['New']])

df = pd.DataFrame(linhas, columns=columns)
df.to_csv('Dados.csv', encoding='iso8859-1', sep=';', index=False, quoting=csv.QUOTE_NONNUMERIC)
