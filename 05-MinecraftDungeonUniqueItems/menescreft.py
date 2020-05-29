from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import csv

linhas = []
columns = []

driver = webdriver.Chrome("../chromedriver")
driver.get('https://www.rockpapershotgun.com/2020/05/26/minecraft-dungeons-unique-items-guide-how-to-get-the-best-gear-2/')
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.close()

for table in soup.find_all('table'):
    if table.has_attr('class') and ' '.join(
            table['class']) == 'tablepress tablepress-id-927 dataTable no-footer':
        trs = table.find_all('thead')[0].find_all('tr')
        columns = [th.text for th in trs[0].find_all('th')]
        print(columns)

for table in soup.find_all('table'):
    if table.has_attr('class') and ' '.join(
            table['class']) == 'tablepress tablepress-id-927 dataTable no-footer':
        linhas = [[td.text.replace('\n', '').replace('\xa0', '') for td in tr.find_all('td') if td.text] for tr in
                  table.find_all('tbody')[0].find_all('tr')]
        print(linhas)
df = pd.DataFrame(linhas, columns=columns)
df.to_csv('dados.csv', encoding='iso8859-1', sep=';', index=False, quoting=csv.QUOTE_NONNUMERIC)
