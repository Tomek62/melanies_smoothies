# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom ***Smoothie***
    """
)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

name_on_order = st.text_input('Name on Smoothie:')

st.text('The name on your Smoothie will be:'+ name_on_order)

# st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect('Choose up to 5 ingredients:',my_dataframe,max_selections=5)

if ingredients_list:
    ingredients_string = ''
    for fruit in ingredients_list:
        ingredients_string+=fruit+' '
    st.text(ingredients_string[:-2])

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order) values ('"""+ingredients_string+"""','"""+name_on_order+"""')"""
    submit =st.button('Submit')
    
    if submit:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
