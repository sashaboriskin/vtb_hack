import pandas as pd


def recommend_news(df: pd.DataFrame, role: str) -> list:
    df = df.sort_values(by=['views'], ascending=False)
    if role == 'it': 
        best_news = df.loc[df['rubrics'] == 1].iloc[:3]
    else:
        best_news = df.loc[df['rubrics'] == 0].iloc[:3]
    recomendations = []
    for i in range(3):
        recomendations.append(best_news['link'].iloc[[i]].values[0])
    return recomendations 
          

habr_df = pd.read_csv("C:\\Users\\sasha\\PycharmProjects\\vtb_hack2\\data\\habr_recomendations.csv", index_col=0)
role = input("Input the business role: ")
print(recommend_news(habr_df, role))