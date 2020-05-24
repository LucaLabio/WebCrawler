from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import csv

liga = input("Digite a sigla de uma liga profissional de LOL: ").upper()

driver = webdriver.Chrome("../chromedriver")
driver.get('https://lol.gamepedia.com/' + liga + '/2020_Season/Spring_Season/Champion_Statistics')
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.close()

linhas = []
columns = []
titulo = ''

for table in soup.find_all('table'):
    if table.has_attr('class') and ' '.join(
            table['class']) == 'wikitable sortable spstats plainlinks hoverable-rows jquery-tablesorter':
        linhas = [[td.text.replace('\n', '').replace('\xa0', '') for td in tr.find_all('td') if td.text] for tr in
                  table.find_all('tbody')[1].find_all('tr')]

for table in soup.find_all('table'):
    if table.has_attr('class') and ' '.join(
            table['class']) == 'wikitable sortable spstats plainlinks hoverable-rows jquery-tablesorter':
        trs = table.find_all('thead')[0].find_all('tr')
        titulo = trs[0].find_all('th')[0].text.replace(' - Open As Query', '')
        columns = [th.text for th in trs[4].find_all('th')]

df = pd.DataFrame(linhas, columns=columns)
print(df.head())
df.to_csv(liga + '.csv', sep=';', index=False, encoding='utf8', quoting=csv.QUOTE_NONNUMERIC)
