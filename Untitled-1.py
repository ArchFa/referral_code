# %%
import pandas as pd
import streamlit as st
from collections import Counter
from PIL import Image

# %%
# im = Image.open("./logo_ugry.png")
# st.set_page_config(page_title="Количество созданных задач", page_icon=im)

# %%
st.title("Промокоды")
st.write("Количество созданных задач для каждого просокода, время между созданием")


uploaded_file = st.file_uploader("Выбирете файл")


if uploaded_file is not None:
     df = pd.read_csv(uploaded_file, sep='|')
     df.columns = [
        'refferal_code',
        'id',
        'created_at'
        ]

     # изменение типов
     df['created_at'] = pd.to_datetime(df['created_at'], format='%Y-%m-%d %H:%M:%S')

     # удаление пропусков, которые появляются из за особенностей выгрузки
     df = df.dropna()
     file_container = st.expander("Check your uploaded .csv")   
     st.write(df)
else:
    st.info(
        f"""
             👆 Загрузите файл с расширением csv. В файле должны стого содержаться следующие столбцы:
             - реферальный код
             - id задачи
             - время создания задачи
             """
    )
    st.stop()

# %%
# df = pd.read_csv('/Users/arturfattahov/Desktop/offers_referral_codes_2021_09_15__2022_03_15.csv', sep='|')

# %%
df.columns = ['refferal_code', 'id', 'created_at']
df = df.dropna()
df['refferal_code'] = df['refferal_code'].str.strip()
df['created_at'] = pd.to_datetime(df['created_at'], format='%Y-%m-%d %H:%M:%S')

# %%
df = df.sort_values(by=['refferal_code', 'created_at'])

# %%
st.write("# Количество созданных задач по промокоду")

# %%
display_all_task = st.checkbox(
    "Отобразить количество задач по каждому промокоду", False, help="Отобразится количество созданных задач по каждому промокоду"
)

# %%
if display_all_task:
    st.write(df['refferal_code'].value_counts())

# %%



