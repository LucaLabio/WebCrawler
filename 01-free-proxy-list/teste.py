from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import csv
driver = webdriver.Chrome("../chromedriver.exe")
driver.get('https://free-proxy-list.net/')
soup = BeautifulSoup(driver.page_source, 'html.parser')
linhas = [[td.text.replace('\n', '') for td in tr.find_all('td')] for tr in soup.find_all('tbody')[0].find_all('tr')]

columns = [th.text for th in soup.find_all('table')[0].find_all('tr')[0].find_all('th')]
df = pd.DataFrame(linhas, columns=columns)
df.to_csv('dados.csv', sep=',', index=False, encoding='utf8', quoting=csv.QUOTE_NONNUMERIC)
driver.close()
