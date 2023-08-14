import streamlit as st
import base64
from fpdf import FPDF


def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)



def generate_pdf(input):
    """
     31 = 3rd weekday (wednesday) ka 1st slot

     IF DATA == INDEX[99] , INDEXX[99]=DATA
     """

    index = {11: "A1", 12: "B1", 13: "C1", 14: "E1", 15: "G1", 16: "K1", 17: "L1", 18: "I1",
             21: "B2", 22: "D1", 23: "C2", 24: input, 25: "H1", 26: "L2", 27: "J1", 28: "M1",
             31: "E2", 32: "A2", 33: "D2", 34: "F1", 35: "G2", 36: "K2", 37: "M2", 38: "I2",
             41: "F2", 42: "B3", 43: "C3", 44: "E3", 45: "H2", 46: "L3", 47: "M3", 48: "J2",
             51: "G3", 52: "A3", 53: "D3", 54: "F3", 55: "H3", 56: "K3", 57: "J3", 58: "I3",

             1: "N", 2: "O", 3: "V", 4: "W", 5: "P", 6: "Q", 7: "R", 8: "S", 9: "T", 10: "U"}

    Day = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thrusday", 5: "Friday"}

    

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()

    # TITLE ROW
    pdf.set_font(family="Times", size=8, style="B")
    pdf.set_text_color(80, 80, 80)
    pdf.cell(w=20, h=8, txt="Day", border=1)

    pdf.cell(w=20, h=8, txt="8:20-9:20", border=1)
    pdf.cell(w=20, h=8, txt="9:20-20:20", border=1)
    pdf.cell(w=20, h=8, txt="20:20-11:20", border=1)
    pdf.cell(w=20, h=8, txt="11:20-12:20", border=1)
    pdf.cell(w=20, h=8, txt="12:20-1:20", border=1)
    pdf.cell(w=20, h=8, txt="2:20-3:20", border=1)
    pdf.cell(w=20, h=8, txt="3:20-4:20", border=1)
    pdf.cell(w=20, h=8, txt="4:20-5:20", border=1, ln=1)

    # Adding content
    for i in range(1, 6, 1):
        pdf.cell(w=20, h=8, txt=Day[i], border=1)
        for j in range(1, 9, 1):
            if j != 8:
                pdf.cell(w=20, h=8, txt=index[(i * 10 + j)], border=1)
            else:
                pdf.cell(w=20, h=8, txt=index[(i * 10 + j)], border=1, ln=1)

    pdf.output(f"TT.pdf")