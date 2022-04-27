# %%
import pandas as pd
import streamlit as st
from collections import Counter
from PIL import Image
import numpy as np

# %%
# im = Image.open("./logo_ugry.png")
# st.set_page_config(page_title="Количество созданных задач", page_icon=im)

# %%
st.title("Промокоды")
st.write("Количество созданных задач для каждого просокода, время между созданием")


uploaded_file = st.file_uploader("Выбирете файл")

use_example_file = st.checkbox(
    "Use example file", False, help="Use in-built example file to demo the app"
)

ab_default = None
result_default = None

if uploaded_file is not None:
     df = pd.read_csv(uploaded_file, sep='|')
     df.columns = [
        'refferal_code',
        'id',
        'created_at'
        ]

     # изменение типов
     df['created_at'] = pd.to_datetime(df['created_at'], format='%Y-%m-%d %H:%M:%S')
     df['id'] = df['id'].fillna(0).astype('int32')
     df['refferal_code'] = df['refferal_code'].str.strip()



     # удаление пропусков, которые появляются из за особенностей выгрузки
     df = df.dropna()
     file_container = st.expander("Check your uploaded .csv")   
     st.write(df.head(5))
else:
    st.info(
        f"""
             👆 Загрузите файл с расширением csv. В файле должны стого содержаться следующие столбцы:
             - реферальный код
             - id задачи
             - время создания задачи
             """
    )    


if use_example_file:
    uploaded_file = "offers_referral_codes_2021_09_15__2022_03_15.csv"
    ab_default = ["variant"]
    result_default = ["converted"]


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
df['diff'] = df.groupby('refferal_code')['created_at'].diff(1)
df['diff'] = df['diff'] / np.timedelta64(1, 'm')

# %%
df.head(20)

# %%
df = df.dropna()

# %%
col_multi, col_em = st.columns([2, 3])

selected_sn = col_multi.selectbox(
    "Выберите промокод",
    options=df['refferal_code'].unique().tolist(),
    index=0,
)

# %%
def creation_day(difference_in_hours):
    if difference_in_hours < 0.25:
        return 'Менее 15 минут'
    elif 0.25 <= difference_in_hours <= 0.5:
        return 'От 15 до 30 минут'
    elif 0.5 <= difference_in_hours <= 1:
        return 'От 30 до 60 минут'
    elif 1 <= difference_in_hours <= 3:
        return 'От 1 до 3 часов'
    elif 3 <= difference_in_hours <= 5:
        return 'От 3 до 5 часов'
    elif 5 <= difference_in_hours <= 10:
        return 'От 5 до 10 часов'
    elif 10 <= difference_in_hours <= 20:
        return 'От 10 до 20 часов'
    else:
        return 'Более 20 часов'
#MOF000['diff'].apply(creation_day).value_counts()

# %%
df['duration'] = df['diff'].apply(creation_day)
df_ref_code = df[df['refferal_code']== selected_sn].duration.value_counts().to_frame()
st.dataframe(df_ref_code)


