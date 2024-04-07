import streamlit as st
import pandas as pd

DATA = 'data/books.csv'
DATA_URL = 'https://www.kaggle.com/datasets/sootersaalu/amazon-top-50-bestselling-books-2009-2019'

@st.cache_data
def load_data():
    return pd.read_csv(DATA)

def get_stat(df, col_name, rnd_dgt=None):
    return df[col_name].min(), df[col_name].max(), round(df[col_name].mean(), rnd_dgt)

def add_slider(df, col_name, rnd_dgt=None, step=None):
    min, max, mean = get_stat(df, col_name, rnd_dgt)
    selected = st.sidebar.slider(col_name, min_value=min, max_value=max, value=(mean, max), step=step)
    return (df[col_name] >= selected[0]) & (df[col_name] <= selected[1])

st.title('Amazon Top 50 Bestselling Books 2009-2019')
st.markdown('Dataset is from [here](%s)' % DATA_URL)
st.write("What's the most bestselling books in 2009-2019 on Amazon?")
st.sidebar.title('Some filters')

df = load_data()

user_rating_filter = add_slider(df, 'User Rating', 1, 0.1)
reviews_filter = add_slider(df, 'Reviews')
price_filter = add_slider(df, 'Price', None, 1)
year_filter = add_slider(df, 'Year', None, 1)

df = df[user_rating_filter]
df = df[reviews_filter]
df = df[price_filter]
df = df[year_filter]

show_filter = st.sidebar.checkbox("Show one more filter")
if show_filter:
    option = st.sidebar.selectbox('If any books were bestsellers for more than one year?', ('one year bestsellers', 'multi year bestsellers'))
    if option == 'one year bestsellers':
        df = df.groupby(['Name', 'Author']).filter(lambda x: x['Year'].nunique() == 1)
    else:
        df = df.groupby(['Name', 'Author']).filter(lambda x: x['Year'].nunique() > 1)

g = st.sidebar.radio('Genre', ('Fiction', 'Non Fiction', 'Both'), index=2)
if g == 'Fiction':
    df = df[df['Genre'] == 'Fiction']
elif g == 'Non Fiction':
    df = df[df['Genre'] == 'Non Fiction']
else:
    df = df[df['Genre'].isin(['Fiction', 'Non Fiction', 'Both'])]

#genres = df['Genre'].unique()
#selected_genres = st.sidebar.multiselect('Genre', genres, default=genres)
#df = df[df['Genre'].isin(selected_genres)]

show_authors = st.sidebar.checkbox('Show authors')
if show_authors:
    authors = df['Author'].unique()
    selected_authors = st.sidebar.multiselect('Author', authors, default='George R. R. Martin')
    df = df[df['Author'].isin(selected_authors)]

st.markdown(f'There are **{df.shape[0]}** books that match chosen filters.')
st.markdown('**Enjoy!**')
st.table(df)
