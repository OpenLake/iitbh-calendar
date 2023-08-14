import streamlit as st
from backend import show_pdf, generate_pdf

st.title("Time-Table Generator : ")

place=st.text_input("Code:",help="Type the course code")

if place:
    generate_pdf(place)
    st.info("pdf generated successfully")


    with st.expander("Generate PDF"):
        show_pdf('TT.pdf')