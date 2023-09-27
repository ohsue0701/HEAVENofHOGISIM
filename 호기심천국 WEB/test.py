# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

# origin_path = r'C:\Users\lg\Desktop\졸작\호기심천국\호기심천국 DATA\origin.csv'
# origin = pd.read_csv(origin_path, encoding='utf8')
# print(origin.iloc[:, 0])

# datalab_path = r'C:\Users\lg\Desktop\졸작\호기심천국\호기심천국 DATA\신조어추출\데이터랩\데이터랩_onlyNew_CSV.csv'
# datalab = pd.read_csv(datalab_path, encoding='utf8')

# # print(datalab_raw.iloc[0])

# file_path3 = 'C:/Users/lg\Desktop/졸작/호기심천국 WEB/exSentences.csv'
# sentences = pd.read_csv(file_path3, encoding="utf8")

# # 각 단어에 대한 포함된 문장의 길이를 계산하여 새로운 열 생성
# sentences['문장 길이'] = sentences['포함된 문장'].apply(len)

# # 단어별로 그룹화하여 문장 길이를 정렬하고 두 번째로 작은 행 선택
# sentences = sentences.groupby('단어').apply(lambda group: group.nlargest(2, '문장 길이').tail(1)).reset_index(drop=True)
# result_df = sentences.drop_duplicates(subset='단어', keep='first')

# df = pd.DataFrame(
#     {
#         "단어": [],
#         "빈도": [],
#         "예문": []
#     }
# )

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# print(len(origin))
# print()
# print()
# print(len(sentences))

# df = pd.DataFrame({'단어': origin['단어'],
#                    '예문': sentences.loc[sentences['단어'].isin(origin['단어']), '포함된 문장'].values})



# for i in range (len(origin['단어'])):

#     index = sentences['단어'][origin['단어'][i]].index
#     print(index)
#     df.loc[i] = [origin['단어'][i], origin['빈도'][i], sentences['포함된 문장'][index]]

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# print(df)





import random
import pandas as pd
import streamlit as st

df = pd.DataFrame(
    {
        "name": ["Roadmap", "Extras", "Issues"],
        "url": ["https://roadmap.streamlit.app", "https://extras.streamlit.app", "https://issues.streamlit.app"],
        "stars": [random.randint(0, 1000) for _ in range(3)],
        "views_history": [[random.randint(0, 5000) for _ in range(30)] for _ in range(3)],
    }
)

print(df["views_history"])

st.dataframe(
    df,
    column_config={
        "name": "App name",
        "stars": st.column_config.NumberColumn(
            "Github Stars",
            help="Number of stars on GitHub",
            format="%d ⭐",
        ),
        "url": st.column_config.LinkColumn("App URL"),
        "views_history": st.column_config.LineChartColumn(
            "Views (past 30 days)", y_min=0, y_max=5000
        ),
    },
    hide_index=True,
)