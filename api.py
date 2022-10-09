import pandas as pd
pd.options.mode.chained_assignment = None


def get_all_seconds(year: int, month: int, day: int, secs: int) -> int:
  return (year*12*30*24*60*60 + month*30*24*60*60 + day*60*60 + secs)


def recommend_news(df: pd.DataFrame, role: str) -> list:
    df['jesos_seconds'] = 0
    for i in range(len(df)):
        year = df['year'].iloc[[i]]
        month = df['month'].iloc[[i]]
        day = df['day'].iloc[[i]]
        secs = df['seconds'].iloc[[i]]
        df['jesos_seconds'].iloc[[i]] = get_all_seconds(year, month, day, secs)    
    mean_jesos_seconds = df['jesos_seconds'].mean()
    mean_views = df['views'].mean()
    df['recom_coof'] = 0
    for i in range(len(df)):
        df['recom_coof'].iloc[[i]] = (df['views'].iloc[[i]]/mean_views)/(df['jesos_seconds'].iloc[[i]]/mean_jesos_seconds)    
    df = df.sort_values(by=['recom_coof'], ascending=False)
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