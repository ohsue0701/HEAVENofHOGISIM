import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from dateutil.relativedelta import relativedelta
import math

st.markdown("# DC인사이드 🚫")
st.sidebar.markdown("# DC인사이드 🚫")

file_path1 = r'WEB_DATA/origin_DC.csv'
file_path2 = r'WEB_DATA/datalab_DC.csv'
file_path3 = r'WEB_DATA/sentences_DC.csv'

file_path1 = r'WEB_DATA/origin_DC_발표샘플.csv'
file_path2 = r'WEB_DATA/datalab_DC_발표샘플.csv'
file_path3 = r'WEB_DATA/sentences_DC_발표샘플.csv'

origin = pd.read_csv(file_path1, encoding='utf8')
datalab = pd.read_csv(file_path2, encoding='utf8')
sentences = pd.read_csv(file_path3, encoding="utf8") 
# print("origin 길이 :" + str(len(origin)))
# print("datalab 길이 :" + str(len(datalab)))
# print("sentences 길이 :" + str(len(sentences)))


# 새로운 열에 가장 먼저 0보다 큰 값이 나온 날짜 추가
first_non_zero_date = []
for index, row in datalab.iterrows():
    word = row['Unnamed: 0']
    values = row[1:]
    first_non_zero_idx = np.where(values > 0)[0]
    # first_non_zero_idx[0] 가, 단어마다 처음 나온 날짜의 인덱스
    idx = first_non_zero_idx[0]
    date_list = datalab.columns.tolist()
    date_list.remove("Unnamed: 0")
    date = date_list[idx]
    first_non_zero_date.append(date)
# print(len(first_non_zero_date))

datalab['최초 등장 달'] = first_non_zero_date
first_appear = datalab[['Unnamed: 0', '최초 등장 달']]
first_appear = first_appear.rename(columns={'Unnamed: 0': '단어'})
# print(first_appear)
datalab.drop(columns=['최초 등장 달'], inplace=True)


# 'ranking' 생성
ranking = pd.merge(origin, datalab, left_on='단어', right_on=datalab.iloc[:, 0], how='left')
ratio = ranking.iloc[:, 3:]
ranking = ranking.iloc[:, 0:2]
# print("ranking 길이 :" + str(len(ranking)))

# 'sentences'를 두 번째로 짧은 문장 하나씩으로만 구성되도록 재구성
sentences['문장 길이'] = sentences['포함된 문장'].apply(len)
sentences = sentences.groupby('단어').apply(lambda group: group.nlargest(2, '문장 길이').tail(1)).reset_index(drop=True)
sentences = sentences.drop_duplicates(subset='단어', keep='first')
# print("sentences 길이 :" + str(len(sentences)))

# Function to truncate text around a keyword
def truncate_text_around_keyword(text, keyword, max_length=10):
    keyword_index = text.find(keyword)
    if keyword_index == -1:
        return text
    start_index = max(0, keyword_index - max_length)
    end_index = min(len(text), keyword_index + max_length + len(keyword))
    truncated_text = '…' + text[start_index:end_index] + '…'
    return truncated_text
sentences['포함된 문장'] = sentences.apply(lambda row: truncate_text_around_keyword(row['포함된 문장'], row['단어']), axis=1)
# print("sentences 길이 :" + str(len(sentences)))

# 'ranking' 생성
ranking = pd.merge(ranking, sentences, left_on='단어', right_on=sentences.iloc[:, 0], how='left')
ranking.drop(columns=['단어_x'], inplace=True)
ranking.drop(columns=['단어_y'], inplace=True)
ranking.drop(columns=['문장 길이'], inplace=True)
# print("ranking 길이 :" + str(len(ranking)))

# 'for_ratio' 생성 (단어+빈도+그래프)
for_ratio = pd.merge(origin, datalab, left_on='단어', right_on=datalab.iloc[:, 0], how='left')
for_ratio.drop(columns=['빈도'], inplace=True)
for_ratio.drop(columns=['Unnamed: 0'], inplace=True)
# print("for_ratio 길이 :" + str(len(for_ratio)))

# 'for_ratio'를 딕셔너리 리스트로 변환
result_dict = {}
for _, row in for_ratio.iterrows():
    result_dict[row[0]] = row[1:].tolist()

# 한 단어의 빈도값들을 하나의 리스트로 만들고, 그 리스트를 하나의 셀에 넣기
df_ratio = pd.DataFrame(list(result_dict.items()), columns=['단어', 'ratio'])
# print("df_ratio 길이 :" + str(len(df_ratio)))

ranking = pd.merge(ranking, df_ratio, left_on='단어', right_on=df_ratio.iloc[:, 0], how='left')
ranking.drop(columns=['단어_x'], inplace=True)
ranking.drop(columns=['단어_y'], inplace=True)
# print("ranking 길이 :" + str(len(ranking)))

# Add a '순위' column to the DataFrame
ranking.insert(0, '순위', range(1, 1 + len(ranking)))
# print("ranking 길이 :" + str(len(ranking)))

ranking = pd.merge(ranking, first_appear, left_on='단어', right_on=first_appear.iloc[:, 0], how='left')
ranking.drop(columns=['단어_x'], inplace=True)
ranking.drop(columns=['단어_y'], inplace=True)
# print("ranking 길이 :" + str(len(ranking)))
# print(ranking)
# print(type(ranking['최초 등장 달'][0]))


################################# TF IDF test ##################################
data_path = r'crawling_result/NEWS_크롤링결과_발표샘플.csv'
data = pd.read_csv(data_path)
df = pd.DataFrame(data)

noun_list = ranking.loc[:, '단어'].tolist()
# print("단어 수 :" + str(len(noun_list)))

idf_df = pd.DataFrame({'단어': noun_list})
idf_df['DF'] = idf_df['단어'].apply(lambda x: sum(df['문장'].apply(lambda y: y.count(x))))
total_documents = len(df['글번호'].unique())
idf_df['IDF'] = idf_df['DF'].apply(lambda x: math.log(total_documents / (x + 1)))  # +1을 더해 0으로 나누는 경우를 방지
# print(ranking)
# print(idf_df)
# print("idf df 리스트 수 :" + str(len(idf_df)))
ranking = pd.merge(ranking, idf_df, on='단어', how='left')

################################# TF IDF test ##################################


# 최종 'ranking'
ranking = ranking[['순위', '단어', 'DF', 'IDF', '최초 등장 달', 'ratio', '포함된 문장']]


# 요약 랭킹, 전체 랭킹 tab
show_small_df, show_expanded_df = st.tabs(["요약 랭킹 (1-10위)", "전체 랭킹"])

# with show_small_df:
#     date = date_list[-1]
#     st.caption("📆검색 날짜 : " + str(date))
#     st.data_editor(ranking.iloc[:10, :4],
#                    num_rows="dynamic",
#                    key="data_editor_small",
#                  width=400,
#                  height=390,
#                  column_config={
#                      '순위' : st.column_config.NumberColumn(
#                          '순위👑',
#                          format='%d위',
#                      ),

#                      '단어': '신조어🆕',
#                      'DF': st.column_config.NumberColumn(
#                          '출현 빈도(DF)👄',
#                          format='%d',
#                      ),
#                      'IDF': st.column_config.NumberColumn(
#                          '출현 빈도(IDF)👄',
#                          format='%.2f',
#                      ),

#                  },
#                  hide_index=True)
#     removed_words_small = []
#     for i in range(len(st.session_state["data_editor_small"]["deleted_rows"])):
#         removed_words_small.append(ranking.iloc[st.session_state["data_editor_small"]["deleted_rows"][i], 1])
#     st.write(removed_words_small)

# with show_expanded_df:
#     date = date_list[-1]
#     st.caption("📆검색 날짜 : " + str(date))
#     st.data_editor(ranking,
#                    num_rows="dynamic",
#                    key="data_editor_expended",
#                  width=6000,
#                  height=2000,
#                  column_config={
#                      '순위' : st.column_config.NumberColumn(
#                          '순위👑',
#                          format='%d위',
#                      ),
#                      '단어': '신조어🆕',
#                      '포함된 문장': '출처 문장✍️',
#                      "ratio": st.column_config.LineChartColumn(
#                          "검색 빈도 📈", y_min=5000, y_max=50000
#                      ),
#                      'DF': st.column_config.NumberColumn(
#                          '출현 빈도(DF)👄',
#                          format='%d',
#                      ),
#                      'IDF': st.column_config.NumberColumn(
#                          '출현 빈도(IDF)👄',
#                          format='%.2f',
#                      ),
#                  },
#                  hide_index=True
#                  )
#     removed_words_expended = []
#     for i in range(len(st.session_state["data_editor_expended"]["deleted_rows"])):
#         removed_words_expended.append(ranking.iloc[st.session_state["data_editor_expended"]["deleted_rows"][i], 1])
        
#     st.write(removed_words_expended)

with show_small_df:
    date = date_list[-1]
    st.caption("📆검색 날짜 : " + str(date))
    st.dataframe(ranking.iloc[:10, :4],
                 width=400,
                 height=390,
                 column_config={
                     '순위' : st.column_config.NumberColumn(
                         '순위👑',
                         format='%d위',
                     ),

                     '단어': '신조어🆕',
                     'DF': st.column_config.NumberColumn(
                         '출현 빈도(DF)👄',
                         format='%d',
                     ),
                     'IDF': st.column_config.NumberColumn(
                         '출현 빈도(IDF)👄',
                         format='%.2f',
                     ),

                 },
                 hide_index=True)

with show_expanded_df:
    date = date_list[-1]
    st.caption("📆검색 날짜 : " + str(date))
    st.dataframe(ranking,
                 width=6000,
                 height=2000,
                 column_config={
                     '순위' : st.column_config.NumberColumn(
                         '순위👑',
                         format='%d위',
                     ),
                     '단어': '신조어🆕',
                     '포함된 문장': '출처 문장✍️',
                     "ratio": st.column_config.LineChartColumn(
                         "검색 빈도 📈", y_min=5000, y_max=50000
                     ),
                     'DF': st.column_config.NumberColumn(
                         '출현 빈도(DF)👄',
                         format='%d',
                     ),
                     'IDF': st.column_config.NumberColumn(
                         '출현 빈도(IDF)👄',
                         format='%.2f',
                     ),
                 },
                 hide_index=True
                 )


