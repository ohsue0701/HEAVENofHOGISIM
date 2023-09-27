import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from PIL import Image
import os
plt.rcParams['font.family'] = 'sans-serif'

st.set_page_config(
    page_title="호기심 천국",
    page_icon="💡",
    layout="wide"
)

st.write("# 💡 :rainbow[호기심 천국이란?]")
st.write("### 📈 '네이버 데이터랩' :red[**검색 빈도 데이터**]를 기반으로,")
st.write("### 🆕 각 커뮤니티별 :blue[**신조어**]를 분석하여 제공하는 서비스입니다.")
st.caption("숙명여자대학교 소프트웨어학부 컴퓨터과학전공 김민정, 김현수")

def load_image(img_file):
    img = Image.open(img_file)
    return img

wordCloud = load_image(r'WEB_DATA/호기심천국_워드클라우드.png')
st.image(wordCloud)           

sample_path = r'WEB_DATA/sample.csv'
sample_datalab = pd.read_csv(sample_path, encoding='utf8')

temp = 0
# 각 단어의 검색 빈도를 날짜별로 그리는 라인 차트
for index, row in sample_datalab.iterrows():
    word = row['Unnamed: 0']
    chart_data = row[1:]  # 날짜 열을 제외한 데이터 가져오기
    word_name = row[0] 
    if temp == 0:
        st.divider()
        st.write("### 📌 일반어 검색 빈도 그래프 예시")
    elif temp == 3:
        st.divider()
        st.write("### 📌 신조어 검색 빈도 그래프 예시")
    elif temp == 6:
        st.divider()
        st.write("### 📌 이슈어 검색 빈도 그래프 예시")
    st.write('**EX) '+word_name+'**')
    st.line_chart(chart_data,
                  )
    temp += 1
