import streamlit as st
import base64
from fpdf import FPDF
import pandas as pd
import re
import sqlite3
import csv



def fetch_csv_data(user_input):
    df = pd.read_csv("course_list/List_of_courses.csv")

    """
     31 = 3rd weekday (wednesday) ka 1st slot

     IF DATA == INDEX[99] , INDEXX[99]=DATA
     """

    index = {11: "A1", 12: "B1", 13: "C1", 14: "E1", 15: "G1", 16: "K1", 17: "L1", 18: "I1",
             21: "B2", 22: "D1", 23: "C2", 24: "  ", 25: "H1", 26: "L2", 27: "J1", 28: "M1",
             31: "E2", 32: "A2", 33: "D2", 34: "F1", 35: "G2", 36: "K2", 37: "M2", 38: "I2",
             41: "F2", 42: "B3", 43: "C3", 44: "E3", 45: "H2", 46: "L3", 47: "M3", 48: "J2",
             51: "G3", 52: "A3", 53: "D3", 54: "F3", 55: "H3", 56: "K3", 57: "J3", 58: "I3",

             1: "N", 2: "O", 3: "V", 4: "W", 5: "P", 6: "Q", 7: "R", 8: "S", 9: "T", 10: "U"}



    Slot_key = {"A1": 11, "B1": 12, "C1": 13, "E1": 14, "G1": 15, "K1": 16, "L1": 17, "I1": 18,
                "B2": 21, "D1": 22, "C2": 23, "H1": 25, "L2": 26, "J1": 27, "M1": 28,
                "E2": 31, "A2": 32, "D2": 33, "F1": 34, "G2": 35, "K2": 36, "M2": 37, "I2": 38,
                "F2": 41, "B3": 42, "C3": 43, "E3": 44, "H2": 45, "L3": 46, "M3": 47, "J2": 48,
                "G3": 51, "A3": 52, "D3": 53, "F3": 54, "H3": 55, "K3": 56, "J3": 57, "I3": 58,
                "N": 1, "O": 2, "V": 3, "W": 4, "P": 5, "Q": 6, "R": 7, "S": 8, "T": 9, "U": 10}

    # data frame me input = course code then output = A1 ...
    # uss output ko dalenge slot dictionary me to get a number
    # index[number] = course code
    # modifying index dictionary wont matter but slot dictionary must be permanently hard coded

    # agar ajeeb slot aaya for example E23 then usko hum slot dictionary use karke interpret karenge
    # E23 => slot[E2] and slot[E3]

    # current idea is to store all slot[] outputs in a list as the code input will prolly be a list

    keys = []
    slots = []

    pattern1 = re.compile("[A-Z][0-9]{2}")  # for D12 vaghera
    pattern2 = re.compile("[A-Z][0-9]{1}")  # for D1

    for course in user_input:
        slots.append((df.loc[df['Code (New/Old)'] == f"{course}"]['Slot new'].squeeze()).strip().split(","))

    for course_slot in slots:

        add = []

        for slot in course_slot:
            slot = slot.strip()

            if re.findall(pattern1, slot) == []:
                if re.findall(pattern2, slot) == []:  # single alphabet
                    alphabet = slot[0]
                    add.append(Slot_key[f"{alphabet}1"])
                    add.append(Slot_key[f"{alphabet}2"])
                    add.append(Slot_key[f"{alphabet}3"])
                else:
                    add.append(Slot_key[slot])
            else:
                alphabet = slot[0]
                dig_1 = slot[1]
                dig_2 = slot[2]

                add.append(Slot_key[f"{alphabet}{dig_1}"])
                add.append(Slot_key[f"{alphabet}{dig_2}"])
        keys.append(add)

    i = 0
    for list in keys:
        for key in list:
            #print(key)
            index[key] = user_input[i]
        #print(user_input[i])
        i = i + 1

    return index


def fetch_db_data(db_filepath, user_input):
    index = {11: "A1", 12: "B1", 13: "C1", 14: "E1", 15: "G1", 16: "K1", 17: "L1", 18: "I1",
             21: "B2", 22: "D1", 23: "C2", 24: "  ", 25: "H1", 26: "L2", 27: "J1", 28: "M1",
             31: "E2", 32: "A2", 33: "D2", 34: "F1", 35: "G2", 36: "K2", 37: "M2", 38: "I2",
             41: "F2", 42: "B3", 43: "C3", 44: "E3", 45: "H2", 46: "L3", 47: "M3", 48: "J2",
             51: "G3", 52: "A3", 53: "D3", 54: "F3", 55: "H3", 56: "K3", 57: "J3", 58: "I3",

             1: "N", 2: "O", 3: "V", 4: "W", 5: "P", 6: "Q", 7: "R", 8: "S", 9: "T", 10: "U"}

    Day = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thrusday", 5: "Friday"}

    Slot_key = {"A1": 11, "B1": 12, "C1": 13, "E1": 14, "G1": 15, "K1": 16, "L1": 17, "I1": 18,
                "B2": 21, "D1": 22, "C2": 23, "H1": 25, "L2": 26, "J1": 27, "M1": 28,
                "E2": 31, "A2": 32, "D2": 33, "F1": 34, "G2": 35, "K2": 36, "M2": 37, "I2": 38,
                "F2": 41, "B3": 42, "C3": 43, "E3": 44, "H2": 45, "L3": 46, "M3": 47, "J2": 48,
                "G3": 51, "A3": 52, "D3": 53, "F3": 54, "H3": 55, "K3": 56, "J3": 57, "I3": 58,
                "N": 1, "O": 2, "V": 3, "W": 4, "P": 5, "Q": 6, "R": 7, "S": 8, "T": 9, "U": 10}
    connection = sqlite3.connect(db_filepath)
    cursor = connection.cursor()
    keys = []
    slots = []
    # Query certain columns
    for course in user_input:
        cursor.execute(f"SELECT slot FROM TimeTable_Generator_coursedata WHERE course_code='{course}'")
        rows = cursor.fetchall()
        # rows is a list of tuples
        # list(rows[0]) is a list ( typecasted tuples to convert them to a list)
        # list(rows[0])[0] is a string
        slots.append((list(rows[0])[0]).split(","))

    connection.close()

    pattern1 = re.compile("[A-Z][0-9]{2}")  # for D12 vaghera
    pattern2 = re.compile("[A-Z][0-9]{1}")  # for D1

    for course_slot in slots:

        add = []

        for slot in course_slot:
            slot = slot.strip()

            if re.findall(pattern1, slot) == []:
                if re.findall(pattern2, slot) == []:  # single alphabet
                    alphabet = slot[0]
                    add.append(Slot_key[f"{alphabet}1"])
                    add.append(Slot_key[f"{alphabet}2"])
                    add.append(Slot_key[f"{alphabet}3"])
                else:
                    add.append(Slot_key[slot])
            else:
                alphabet = slot[0]
                dig_1 = slot[1]
                dig_2 = slot[2]

                add.append(Slot_key[f"{alphabet}{dig_1}"])
                add.append(Slot_key[f"{alphabet}{dig_2}"])
        keys.append(add)

    i = 0
    for lst in keys:
        for key in lst:
            # print(key)
            index[key] = user_input[i]
        # print(user_input[i])
        i = i + 1

    return index

def generate_pdf(index):
    Day = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thrusday", 5: "Friday"}
    """ LOADING DATA IN PDF """

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

def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


if __name__ == "__main__":
    courses=[]
    while True:
        course_code=input(" Enter course code . (break to stop) :").upper()
        if(course_code=="BREAK"):
            break
        else:
            courses.append(course_code)

    print(courses)

    index=fetch_db_data(db_filepath="db.sqlite3",user_input=courses)
    generate_pdf(index=index)