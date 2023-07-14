import streamlit
import pandas 
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Mom\'s New Healthy Diner')

streamlit.header("Breakfast Favorites")

streamlit.text('🥣 Omega 3 & Blueberry Oatmean')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie') 
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# import pandas 
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# Set the index for the fruit list instead of the number it was imported as 
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so folks can pick the fruit they want to include
# streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page 
streamlit.dataframe(fruits_to_show) 

# create the repeatable code block - python function 
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized


# New Section to display fruitvice API response 
streamlit.header("Fruityvice Fruit Advice!")
try: 
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  # Replacing write to screen with a try catch block 
  # streamlit.write('The user entered ', fruit_choice)
  if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
  else:
      # import requests
      # fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
      # fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      back_from_function = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()

# For testing to get text output 
# streamlit.text(fruityvice_response.json())

## Using Pandas read the JSON into a dataframe table using streamlit
# fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
## Format the data into a table with columns 
# streamlit.dataframe(fruityvice_normalized)

# Add a processing break here 
# streamlit.stop()

# import snowflake.connector

# Execute the cursor
## my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_cur.execute("SELECT * FROM fruit_load_list")
# my_data_rows = my_cur.fetchall()

# streamlit.text("Hello from Snowflake:")
streamlit.header("The fruit load list contains:")
# Snowflake related functions 
def get_fruit_load_list():
  with my_cnx_cursor() as my_cur:
    # with statement replaces my_cur = my_cnx.cursor()
    my_cur.execute("SELECT * FROM fruit_load_list")
    return my_cur.fetchall()
    
# Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
  # Set up Snowflake connection 
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)

# Add a processing break here 
streamlit.stop()

# Add a fruit from text input 
add_my_fruit = streamlit.text_input('What fruit would you like to add?', key = "add_my_fruit")

streamlit.write('Thanks for adding ', add_my_fruit)
my_cur.execute("INSERT into FRUIT_LOAD_LIST values ('from streamlit')") 


