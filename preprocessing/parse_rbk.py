import pandas as pd
import requests
from bs4 import BeautifulSoup

"""
Our features: 1)id 2)num of views 3) title 4) text 5) date of publication 6) rubrics
1 table for product m
2 table for project m
"""
features = 'id num_of_views title text date_of_publication rubrics'
columns = features.split(' ')

url_product_manager = 'https://www.rbc.ru/search2/?query=ИТ&project=rbcnews&category=business'
url_project_manager = 'https://www.rbc.ru/search2/?query=ИТ&project=rbcnews&category=technology_and_media'
url_one_example = 'https://www.rbc.ru/technology_and_media/06/10/2022/633dbf9e9a7947269f66e7f1'
df_product = pd.DataFrame(columns=columns)
df_product = df_product.fillna(0) # With 0s rather than NaNs

#response_product = requests.get(url_product_manager)
#response_project = requests.get(url_project_manager)
test_responce = requests.get(url_one_example)
print(test_responce)
soup = BeautifulSoup(test_responce.text, 'lxml')
quotes = soup.find('span', class_='article__header__counter js-insert-views-count')

text = soup.get_text()
print(text)
#print(quotes)