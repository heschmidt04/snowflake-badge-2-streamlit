import streamlit

streamlit.title("Breakfast Favorites")

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmean')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie') 
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')

import pandas 
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# Set the index for the fruit list instead of the number it was imported as 
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so folks can pick the fruit they want to include
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

# Display the table on the page 
streamlit.dataframe(my_fruit_list) 

