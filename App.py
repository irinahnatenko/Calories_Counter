import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(page_title='Calories Counter')
st.header('Calories Counter')

excel_file = 'sampledatafoodinfo.xlsx'
sheet_name = 'FoodList'

df = pd.read_excel(excel_file,
                   sheet_name=sheet_name,
                   usecols='A:D',
                   header=0)


categories = df['Category'].unique().tolist()
calories = df['Calories'].unique().tolist()

calories_selection = st.slider('Calories:',
                                 min_value=min(calories),
                                 max_value=max(calories),
                                 value=(min(calories),max(calories)))

categories_selection = st.multiselect('Category',
                                      categories,
                                      default=categories)

mask = (df['Calories'].between(*calories_selection)) & (df['Category'].isin(categories_selection))
number_of_results = df[mask].shape[0]
st.markdown(f'*Available Results: {number_of_results}*')

df_grouped = df[mask].groupby(by=['Category']).count()[['Calories']]
df_grouped = df_grouped.reset_index()

bar_chart = px.bar(df_grouped,
                  x = 'Category',
                  y = 'Calories',
                  color_discrete_sequence = (['#8F94EF'])*len(df_grouped), template = 'plotly_white')

st.plotly_chart(bar_chart)

pie_chart = px.pie(df,
                   title = 'Calories by Category',
                   values = 'Calories',
                   names = 'Category')


st.plotly_chart(pie_chart)



