import streamlit as st
import pandas as pd
import plotly.express as px

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

# 円グラフ
latest_month = df_plot['年月'].max()
df_pie = df_plot[df_plot['年月'] == latest_month]

st.subheader('円グラフ')

fig_pie = px.pie(df_pie,
                 names='年齢5歳階級',
                 values=sex,
                 title=f'{latest_month.date()} の人口構成 ({sex})'
                 )

st.plotly_chart(fig_pie, use_container_width=True)

st.subheader('折れ線グラフ')
st.line_chart(
    df_plot,
    x='年月',
    y=sex,
    color='年齢5歳階級'
)

# アプリの説明
st.subheader('アプリの概要・目的・使い方')

st.markdown("""
##### アプリの概要
本アプリは、e-Statで公開されている人口統計データを用いて、  
年齢および性別ごとの人口推移を可視化するWebアプリです。  
政府統計データを操作しながら確かめることで、  
人口の変化を直感的に理解することを目的としています。

##### アプリの目的
- 年齢階級別・性別ごとの人口推移を視覚的に理解できる
- 年齢構成や人口割合をグラフから読み取ることができる
- 統計データを用いたWebアプリの基本構成を学ぶことができる

##### 使い方
1. 画面左にあるサイドバーから性別(男女計/男/女)を選択する  
2. 表示したい年齢階級を選択(複数)する（未選択の場合はすべての年齢階級が選択される）  
3. 選択した条件に応じて、人口推移のグラフが更新される  
4. 最新年月の年齢構成は円グラフで確認できる
""")


# 可視化からの解釈・説明
st.subheader('解釈・説明')

st.markdown("""
##### 折れ線グラフからわかること
どの年齢層が多い傾向にあるかがこのグラフから読み取ることができる。
若年層が減少傾向にあるのに反して、高齢層では人口が増加傾向にあることが確認できる。
これにより、少子高齢化が進んでいることが考えられる。
            
##### 円グラフからわかること
調べたい年齢層を選択することでその年齢層動詞を比較することができる。
このグラフからも若年層より高齢層の方が人口が多い傾向にあることが分かる。
こちらでも、少子高齢化であることが分かりそれらの割合を可視化することができる。
            
##### まとめ
以上のことから、本アプリの可視化により
年齢階級別及び性別ごとの人口構造や変化を直感的に把握することができるとわかった。
""")