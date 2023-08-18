import streamlit as st
from backend import show_pdf, generate_pdf , fetch_csv_data, fetch_db_data

st.title("Time-Table Generator : ")

#user_input=[]
course=st.text_input("Codes:",help="Type the course codes in a single line separated by commas "
                                   "( please note that course codes should be exact as the code in list of courses pdf "
                                   ", Example : writing cs266 instead of cs266/csl200 wont work )")
#user_input.append(course.upper())
user_input=course.upper().split(",")
if course:
    print(user_input)
    index=fetch_db_data(db_filepath="db.sqlite3",user_input=user_input)
    generate_pdf(index)
    st.info("pdf generated successfully")


    with st.expander("Generate PDF"):
        show_pdf('TT.pdf')