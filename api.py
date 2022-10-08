import pandas as pd

def generate_link(sourse: str, id: int) -> str:
    if sourse == 'habr':
        link = 'https://habr.com/ru/post/' + str(id)
    return link


def recommend_news(df: pd.DataFrame, role: str) -> list:
    df = df.sort_values(by=['views'], ascending=False)
    if role == 'develop': 
        best_news = df.loc[df['rubrics'] == 'develop'].iloc[:3]
    else:
        best_news = df.loc[df['rubrics'] == 'business'].iloc[:3]
    recomendations = []
    ids = list(best_news['id'])
    sourses = list(best_news['sourse'])   
    for i in range(3):
        recomendations.append(generate_link(sourses[i], ids[i]))
    return recomendations


habr_df = pd.read_csv("C:\\Users\\sasha\\PycharmProjects\\vtb_hack2\\data\\habr.csv", index_col=0)
role = input("Input the business role: ")
print(recommend_news(habr_df, role))