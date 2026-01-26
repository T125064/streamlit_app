import streamlit as st
import pandas as pd

st.title('人口推移')

df = pd.read_csv(
    'FEH_00200524_260125230712.csv',
    encoding='utf-8-sig',
    skiprows=7,
    # on_bad_lines='skip',
    header=None
)

st.write(df.columns)

with st.sidebar:
    st.subheader("抽出条件")
    a = st.multiselect('性別を選択してください',
                       df['a'].unique())

st.write(df.columns)
st.dataframe(df.head())



st.write