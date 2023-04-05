import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healty Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinash & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruit_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruit_selected]
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
#fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
#streamlit.write('The user entered ', fruit_choice)
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
##streamlit.text(fruityvice_response.json())
#normalized_list=pandas.json_normalize(fruityvice_response.json())
#streamlit.dataframe(normalized_list)

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.write('please select a fruit to get information')
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    normalized_list=pandas.json_normalize(fruityvice_response.json())
    streamlit.dataframe(normalized_list)
except URLError as e:
  streamlit.error()
  

#normalized_list=pandas.json_normalize(fruityvice_response.json())
#streamlit.dataframe(normalized_list)
streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_row = my_cur.fetchone()
my_data_rows = my_cur.fetchall()
streamlit.text("Fruit List:")
streamlit.dataframe(my_data_row)
streamlit.dataframe(my_data_rows)

fruit_choice = streamlit.text_input('which fruit would you like to add?','Kiwi')
streamlit.write('Thanks for adding ', fruit_choice)

my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from streamlit')")
