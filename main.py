import streamlit as st
from backend import show_pdf, generate_pdf , fetch_csv_data, fetch_db_data, fetch_course_info_db



st.title("Time-Table Generator : ")


course=st.text_input("Codes:",help="Type the course codes in a single line separated by commas "
                                   "( please note that course codes should be exact as the code in list of courses pdf "
                                   ", Example : writing cs266 instead of cs266/csl200 wont work )")


user_input=course.upper().split(",")
print(user_input)
if user_input !=['']:
    for c in user_input:
        try:
            data=fetch_course_info_db("db.sqlite3",c)
            st.text(f"{data[0]} - {data[1]}")
        except IndexError:
            st.info("Please enter a valid course code")
            user_input.pop()




if st.button(label="Submit") and user_input:
    try:
        index=fetch_db_data(db_filepath="db.sqlite3",user_input=user_input)
        generate_pdf(index)
        st.info("Pdf generated successfully")

        user_input = []
        with st.expander("Show PDF"):
            show_pdf('TT.pdf')

    except KeyError:
        st.info("One of your chosen courses appears to have no proper slot defined")
