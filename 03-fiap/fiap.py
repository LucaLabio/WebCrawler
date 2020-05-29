from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import csv

driver = webdriver.Chrome("../chromedriver")
driver.get('https://www.fiap.com.br/graduacao/')
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.close()

column = ''
df_dict = {}

for div in soup.find_all('div'):
    if div.has_attr('class') and ' '.join(
            div['class']) == 'graduacao-cursos-column':
        for subtitle in div.find_all('div'):
            if subtitle.has_attr('class') and ' '.join(
                    subtitle['class']) == 'graduacao-cursos-subtitle-columns' and subtitle.find_all('span')[0].text:
                column = subtitle.find_all('span')[0].text
        df_dict[column] = [li.find_all('a')[0].text.replace('\n', '').strip().split('   ')[0] for li in
                           div.find_all('ul')[0].find_all('li')]

pd.DataFrame({'Bacharelado': df_dict['Bacharelados']}).to_csv('bacharel.csv', encoding='iso8859-1', sep=',',
                                                              index=False)
pd.DataFrame({'Tecnologo': df_dict['Tecnólogos']}).to_csv('tecnologo.csv', encoding='iso8859-1', sep=',', index=False)

df1 = pd.read_csv('bacharel.csv', encoding='iso8859-1', sep=',')
df2 = pd.read_csv('tecnologo.csv', encoding='iso8859-1', sep=',')
df3 = pd.concat([df1, df2], ignore_index=False, axis=1)
df3.to_csv('completo.csv', encoding='iso8859-1', sep=';')
