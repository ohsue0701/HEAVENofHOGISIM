import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

st.markdown("# DC인사이드 🚫")
st.sidebar.markdown("# DC인사이드 🚫")

# st.set_page_config(
#     page_title="호기심 천국",
#     page_icon="👋",
#     layout="wide"
# )

st.sidebar.success("Select a demo above.")

file_path1 = r'C:\Users\lg\Desktop\졸작\호기심천국\호기심천국 WEB\WEB_DATA\origin_DC.csv'
origin = pd.read_csv(file_path1, encoding='utf8')

file_path2 = r'C:\Users\lg\Desktop\졸작\호기심천국\호기심천국 WEB\WEB_DATA\datalab_DC.csv'
datalab = pd.read_csv(file_path2, encoding='utf8')

ranking = pd.merge(origin, datalab, left_on='단어', right_on=datalab.iloc[:, 0], how='left')
ratio = ranking.iloc[:, 3:]
ranking = ranking.iloc[:, 0:2]

file_path3 = r'C:\Users\lg\Desktop\졸작\호기심천국\호기심천국 WEB\WEB_DATA\sentences_DC.csv'
sentences = pd.read_csv(file_path3, encoding="utf8")

# 각 단어에 대한 포함된 문장의 길이를 계산하여 새로운 열 생성
sentences['문장 길이'] = sentences['포함된 문장'].apply(len)

# 단어별로 그룹화하여 문장 길이를 정렬하고 두 번째로 작은 행 선택
sentences = sentences.groupby('단어').apply(lambda group: group.nlargest(2, '문장 길이').tail(1)).reset_index(drop=True)
sentences = sentences.drop_duplicates(subset='단어', keep='first')

ranking = pd.merge(ranking, sentences, left_on='단어', right_on=sentences.iloc[:, 0], how='left')
ranking.drop(columns=['단어_x'], inplace=True)
ranking.drop(columns=['단어_y'], inplace=True)
ranking.drop(columns=['문장 길이'], inplace=True)

for_ratio = pd.merge(origin, datalab, left_on='단어', right_on=datalab.iloc[:, 0], how='left')
for_ratio.drop(columns=['빈도'], inplace=True)
for_ratio.drop(columns=['Unnamed: 0'], inplace=True)

# 데이터프레임을 딕셔너리 리스트로 변환
result_dict = {}
for _, row in for_ratio.iterrows():
    result_dict[row[0]] = row[1:].tolist()

df_ratio = pd.DataFrame(list(result_dict.items()), columns=['단어', 'ratio'])

ranking = pd.merge(ranking, df_ratio, left_on='단어', right_on=df_ratio.iloc[:, 0], how='left')
ranking.drop(columns=['단어_x'], inplace=True)
ranking.drop(columns=['단어_y'], inplace=True)

ranking = ranking[['단어', '빈도', 'ratio', '포함된 문장']]


stdf = st.dataframe(data = ranking[:],
                    width=4000,
                    height=2000,
                    column_config={
                        '단어': '신조어',
                        '포함된 문장' : '예문',
                        "ratio": st.column_config.LineChartColumn(
                            "검색 추이 그래프", y_min=5000, y_max=50000
                        ),
                        '빈도': st.column_config.NumberColumn(
                            '출현 빈도',
                            format='%d  👄',
                        ),
                     },
                     
                     hide_index=True,
                    )