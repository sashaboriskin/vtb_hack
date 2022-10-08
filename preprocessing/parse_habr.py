import pandas as pd
import requests
from bs4 import BeautifulSoup


def clear_rubric(rubrics: list) -> list:
    bad_symbols = ['*']
    clear_rubric = rubrics[:] 
    for word in range(len(rubrics)):   
        for i in range(len(rubrics[word])):
            if rubrics[word][i] in bad_symbols:
                clear_rubric[word] = clear_rubric[word].replace(rubrics[word][i], '')   #clear bad words in rubrics
    clear_rubric = [word[:-1] for word in clear_rubric]    #delete last spaces
    return clear_rubric


def get_date(date_soup: str) -> list:
    date_str = str(date_soup)
    date = str(date_str[102:112])
    time = str(date_str[114:119])
    return [date, time]


def add_new_row_to_df(url: str, rubric:str) -> dict:
    test_responce = requests.get(url)
    soup = BeautifulSoup(test_responce.text, 'lxml')
    views = int(soup.find('span', class_='tm-icon-counter__value').get_text())
    id = int(url[25:-1])
    date = get_date(soup.find('span', class_='tm-article-snippet__datetime-published'))
    text = [string.get_text() for string in soup.find_all('p')]
    title = soup.find('h1', class_='tm-article-snippet__title tm-article-snippet__title_h1').find('span').get_text()
    #rubric = clear_rubric([string.get_text() for string in soup.find_all('span', 'tm-article-snippet__hubs-item')])
    new_row = {'id': id,
               'views': views,
               'title': title, 
               'date': date[0],
               'time': date[1],
               #'rubrics': rubric,
               'text': text}
    return new_row



habr_df = pd.DataFrame(columns=['id', 'views', 'title', 'date', 'time', 'rubrics', 'text'])

url = 'https://habr.com/develop/'
all_pages = requests.get(url)
soup = BeautifulSoup(all_pages.text, 'lxml')
#links = []
# for link in soup.find_all('a', class_='tm-article-snippet__title-link'):
#     print(link.get('href'))
links = soup.find_all('div', class_='tm-article-snippet')
print(links)