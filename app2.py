import streamlit as st
import pandas as pd

st.title('人口推移')

# csv読み込み
df = pd.read_csv(
    'FEH_00200524_260125230712.csv',
    encoding='utf-8',
    skiprows=7
)

df.columns = df.columns.str.strip()
df['表章項目'] = df['表章項目'].str.strip()

df['年月'] = (
    df['時間軸（年月日現在）']
    .astype(str)
    .str.replace('年', '-', regex=False)
    .str.replace('月', '', regex=False)
    .str.replace('日', '', regex=False)
)
df['年月'] = pd.to_datetime(df['年月'], errors='coerce')
df['年'] = df['年月'].dt.year
df['月'] = df['年月'].dt.month

# 人口列を数値化
for col in ['男', '女']:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(',', '', regex=False)
        .astype(float)
    )

df['男女計'] = df['男女計'].astype(str).str.replace(',', '', regex=False)
df['男女計'] = pd.to_numeric(df['男女計'], errors='coerce')
df['男女計'] = df['男女計'].fillna(df['男'] + df['女'])

# サイドバー
with st.sidebar:
    st.subheader("抽出条件")

    # 性別選択(一つずつ)
    sex = st.selectbox(
        '性別を選択してください',
        ['男女計', '男', '女']
    )

    # 年齢選択(複数選択)
    age = st.multiselect(
        '年齢を選択してください',
        df['年齢5歳階級'].unique()
    )

if not age:
    age = df['年齢5歳階級'].unique()

# データ抽出
df_show = df[(df['表章項目'].str.contains('人口', na=False)) &
             (df['年齢5歳階級'].isin(age))
             ]

if df_show.empty:
    st.warning('条件に合うデータがありません')
    st.stop()

# 集計
df_plot = (
    df_show
    .groupby(['年月', '年齢5歳階級'])[sex]
    .sum()
    .reset_index()
    .sort_values('年月')
)

st.subheader('抽出結果')
st.dataframe(df_plot)

st.subheader('グラフ')
st.line_chart(
    df_plot,
    x='年月',
    y=sex,
    color='年齢5歳階級'
)
