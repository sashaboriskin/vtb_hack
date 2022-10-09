from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from catboost import CatBoostClassifier
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''make model'''												
whole_data = pd.read_csv("C:\\Users\\sasha\\PycharmProjects\\vtb_hack2\\data\\habr_preprocessed.csv", index_col=0)
X = whole_data[['text', 'title', 'views', 'year', 'month', 'day', 'seconds']]
y = whole_data['rubrics']   #business - 0, #IT - 1
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
model = CatBoostClassifier(iterations=300, task_type="CPU")#, ignored_features=['id', 'link', 'seconds', 'year', 'day', 'month', 'views'])
model.fit(X_train, y_train, text_features=['text', 'title'])
preds = model.predict(X_val)
X_val['rubrics'] = preds
#score = roc_auc_score(y_val, preds)
#print(score)

'''recover the link'''
list_of_titles = X_val['title'].to_list()
new_list_of_links = []
for i in range(len(X_val)):
  row = whole_data.loc[whole_data['title'] == list_of_titles[i]]
  new_list_of_links.append(row['link'])
print(len(new_list_of_links))
X_val['link'] = new_list_of_links


for i in range(len(X_val)):
  X_val['link'].iloc[[i]] = X_val['link'].iloc[[i]].to_string().split()[2]

X_val.to_csv("C:\\Users\\sasha\\PycharmProjects\\vtb_hack2\\data\\habr_recomendations.csv")
'''
feature_importance = model.feature_importances_
sorted_idx = np.argsort(feature_importance)
fig = plt.figure(figsize=(12, 6))
plt.barh(range(len(sorted_idx)), feature_importance[sorted_idx], align='center')
plt.yticks(range(len(sorted_idx)), np.array(X_val.columns)[sorted_idx])
plt.title('Feature Importance')
'''
X_val.to_csv("C:\\Users\\sasha\\PycharmProjects\\vtb_hack2\\data\\habr_recomendations.csv")