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

def get_id_from_link(url: str) -> int:
    id = ''
    for i in range(len(url)):
        if url[i].isdigit():
            id+=url[i]
    return int(id)


def add_new_row_to_df(url: str, rubric: str) -> dict:
    test_responce = requests.get(url)
    soup = BeautifulSoup(test_responce.text, 'lxml')
    try:
    	views = int(soup.find('span', class_='tm-icon-counter__value').get_text())
    except ValueError:
        if 'K' in soup.find('span', class_='tm-icon-counter__value').get_text(): 
            views = float(soup.find('span', class_='tm-icon-counter__value').get_text()[:-1])*1000
        elif 'M' in soup.find('span', class_='tm-icon-counter__value').get_text():
            views = float(soup.find('span', class_='tm-icon-counter__value').get_text()[:-1])*1000000 
    id = get_id_from_link(url)
    link = url
    date = get_date(soup.find('span', class_='tm-article-snippet__datetime-published'))
    text = [string.get_text() for string in soup.find_all('p')]
    title = soup.find('h1', class_='tm-article-snippet__title tm-article-snippet__title_h1').find('span').get_text()
    #rubric = clear_rubric([string.get_text() for string in soup.find_all('span', 'tm-article-snippet__hubs-item')])
    new_row = {'id': id,
               'link': link,
	       'sourse': 'habr', 
               'views': views,
               'title': title, 
               'date': date[0],
               'time': date[1],
               'rubrics': rubric,
               'text': text}
    return new_row


def add_link_to_df(df: pd.DataFrame, url: str, role: str) -> pd.DataFrame:
    all_pages = requests.get(url)
    soup = BeautifulSoup(all_pages.text, 'lxml')
    links = []
    for link in soup.find_all('a', class_='tm-article-snippet__title-link'):
        if 'post' in link.get('href'):
            links.append('https://habr.com' + link.get('href')) 

    for link in links:
        df = df.append(add_new_row_to_df(link, role), ignore_index=True)
    return df

def normalize_date(date: str) -> list:
    new_list = date.split('-')
    return new_list


def normalize_time(time: str) -> int:
    new_list = time.split(':')
    return int(new_list[0]) * 60 * 60 + int(new_list[1]) * 60


habr_df = pd.DataFrame(columns=['id', 'link','sourse', 'views', 'title', 'date', 'time', 'rubrics', 'text'])
develop_url = 'https://habr.com/ru/flows/develop/'
business_url = 'https://habr.com/ru/flows/marketing/'
habr_df = add_link_to_df(habr_df, develop_url, 'develop')
habr_df = add_link_to_df(habr_df, business_url, 'business')

for i in range(2, 151):
    print(i)
    print(habr_df.shape)
    next_page_develop_url = develop_url + 'page' + str(i)
    next_page_business_url = business_url + 'page' + str(i)
    habr_df = add_link_to_df(habr_df, next_page_develop_url, 'develop')
    habr_df = add_link_to_df(habr_df, next_page_business_url, 'business')

#habr_df.to_csv("C:\\Users\\sasha\\PycharmProjects\\vtb_hack2\\data\\habr.csv")  
dates_series = habr_df['date']
list_of_secs = []
for i in range(len(habr_df)):
    list_of_secs.append(normalize_time(str(habr_df['time'][i])))


habr_df['year'] = pd.Series(normalize_date(str(habr_df['date']))[0][1:], index=habr_df.index)
habr_df['month'] = pd.Series(normalize_date(str(habr_df['date']))[1], index=habr_df.index)
habr_df['day'] = pd.Series(normalize_date(str(habr_df['date']))[2][:2], index=habr_df.index)
habr_df['seconds'] = pd.Series(list_of_secs, index=habr_df.index)
del habr_df['date']
del habr_df['time']
habr_df['rubrics'] = habr_df['rubrics'].map({'develop': 1, 'business': 0})
for i in range(len(habr_df)):
    habr_df['text'][i] = habr_df['text'][i][2:-2]
habr_df.to_csv('C:\\Users\\sasha\\PycharmProjects\\vtb_hack2\\data\\habr_preprocessed.csv')

