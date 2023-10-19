import streamlit as st

st.title("Student Schedule Builder - KUDC")
"---"
"Welcome to the Student Schedule Builder! Use the \
planner below to keep your busy schedule organized \
and do things on time!"
"---"
col1, col2, col3 = st.columns(3 )

col1.text_area("Hello World!")
col2.title("Hello World!")