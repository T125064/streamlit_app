import streamlit as st
import pandas as pd

st.title('人口推移')

df = pd.read_csv('FEH_00200524_260125230712.csv',
    encoding='utf=8',
    skiprows=7
    )

df.columns = df.columns.str.strip()
# df = df.rename(columns={'男女別': '性別'})
df['年'] = pd.to_datetime(
    df['時間軸（年月日現在）'],
    errors='coerce'
).dt.year
# df['性別'] = (
#     df['性別']
#     .astype('string')   # ← ここが重要
#     .str.strip()
# )
df['男女別'] = (
    df['男女別']
    .astype('string')
    .str.strip()
    .replace('', pd.NA)
)

st.write("columns:", list(df.columns))


with st.sidebar:
    st.subheader("抽出条件")

    sex_list = df['男女別'].dropna().unique()
    if len(sex_list) == 0:
        st.error('性別が取得できません')
        st.stop()

    sex = st.selectbox('性別を選択してください',sex_list)
    
    age = st.multiselect('年齢を選択してください',
                       df['年齢5歳階級'].dropna().unique(),
                       # default=['総数'] if '総数' in df['年齢5歳階級'].unique() else None
                       )
    
df_show = df[
    (df['表章項目'] == '人口') &
    (df['性別'] == sex) &
    (df['年齢5歳階級'].isin(age))
]

st.subheader('抽出結果')

st.dataframe(df_show)

st.write(df.columns)
st.dataframe(df.head())

st.subheader('グラフ')
df_plot = (df_show
           .groupby('年')['人口']
           .sum()
           .reset_index())
st.line_chart(df_plot.set_index('年'))
