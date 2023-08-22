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

            index[key] = user_input[i]

        i = i + 1

    return index


def fetch_db_data(db_filepath, user_input):

    index = {11: "A1", 12: "B1", 13: "C1", 14: "E1", 15: "G1", 16: "K1", 17: "L1", 18: "I1",
             21: "B2", 22: "D1", 23: "C2", 24: "  ", 25: "H1", 26: "L2", 27: "J1", 28: "M1",
             31: "E2", 32: "A2", 33: "D2", 34: "F1", 35: "G2", 36: "K2", 37: "M2", 38: "I2",
             41: "F2", 42: "B3", 43: "C3", 44: "E3", 45: "H2", 46: "L3", 47: "M3", 48: "J2",
             51: "G3", 52: "A3", 53: "D3", 54: "F3", 55: "H3", 56: "K3", 57: "J3", 58: "I3",

             1: "N", 2: "O", 3: "V", 4: "W", 5: "P", 6: "Q", 7: "R", 8: "S", 9: "T", 10: "U"}
    # Value of index dictionary changes every time program is run

    permanent_index = {11: "A1", 12: "B1", 13: "C1", 14: "E1", 15: "G1", 16: "K1", 17: "L1", 18: "I1",
             21: "B2", 22: "D1", 23: "C2", 24: "  ", 25: "H1", 26: "L2", 27: "J1", 28: "M1",
             31: "E2", 32: "A2", 33: "D2", 34: "F1", 35: "G2", 36: "K2", 37: "M2", 38: "I2",
             41: "F2", 42: "B3", 43: "C3", 44: "E3", 45: "H2", 46: "L3", 47: "M3", 48: "J2",
             51: "G3", 52: "A3", 53: "D3", 54: "F3", 55: "H3", 56: "K3", 57: "J3", 58: "I3",

             1: "N", 2: "O", 3: "V", 4: "W", 5: "P", 6: "Q", 7: "R", 8: "S", 9: "T", 10: "U"}

    Slot_key = {"A1": 11, "B1": 12, "C1": 13, "E1": 14, "G1": 15, "K1": 16, "L1": 17, "I1": 18,
                "B2": 21, "D1": 22, "C2": 23, "BLANK": 24,"H1": 25, "L2": 26, "J1": 27, "M1": 28,
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
                    #( "N" or "O" or "V" or "W" or "P" or "Q" or "R" or "S" or "T" or "U")
                    match alphabet:
                        case "N":
                            add.append(Slot_key[f"B1"])
                            add.append(Slot_key[f"C1"])
                            add.append(Slot_key[f"E1"])
                        case "O":
                            add.append(Slot_key[f"K1"])
                            add.append(Slot_key[f"L1"])
                            add.append(Slot_key[f"I1"])
                        case "V":
                            add.append(Slot_key[f"D1"])
                            add.append(Slot_key[f"C2"])
                            add.append(Slot_key[f"BLANK"])
                        case "W":
                            add.append(Slot_key[f"L2"])
                            add.append(Slot_key[f"J1"])
                            add.append(Slot_key[f"M1"])
                        case "P":
                            add.append(Slot_key[f"A2"])
                            add.append(Slot_key[f"D2"])
                            add.append(Slot_key[f"F1"])
                        case "Q":
                            add.append(Slot_key[f"K2"])
                            add.append(Slot_key[f"M2"])
                            add.append(Slot_key[f"I2"])
                        case "R":
                            add.append(Slot_key[f"B3"])
                            add.append(Slot_key[f"C3"])
                            add.append(Slot_key[f"E3"])
                        case "S":
                            add.append(Slot_key[f"L3"])
                            add.append(Slot_key[f"M3"])
                            add.append(Slot_key[f"J2"])
                        case "T":
                            add.append(Slot_key[f"A3"])
                            add.append(Slot_key[f"D3"])
                            add.append(Slot_key[f"F3"])
                        case "U":
                            add.append(Slot_key[f"K3"])
                            add.append(Slot_key[f"J3"])
                            add.append(Slot_key[f"I3"])

                        case _: # NOT LAB SLOTS
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

    """i = 0
    for lst in keys:
        for key in lst:
            index[key] = user_input[i]

        i = i + 1

    return index"""
    content=[]
    clashes=[]
    pattern = re.compile("[0-9]{3}")  # course codes have 3 digits in the end
    i = 0
    for lst in keys:
        for key in lst:
            if re.findall(pattern, index[key]) != []: # clash has occured course is already present in that section
                clashes.append(f"Course {user_input[i]} is clashing with {index[key]} in the {permanent_index[key]} slot ")

            else:
                index[key] = user_input[i]

        i = i + 1

    content=[index,clashes]
    return content

def fetch_course_codes_db(db_filepath):
    context={'BM':[],'CS':[],'CY':[],'DS':[],'EC':[],'EE':[],'EVT':[],'LA':[],'MA':[],'ME':[],'MSME':[],'MT':[],'NA':[],'PH':[] }
    disciplines=['BM','CS','CY','DS','EC','EE','EVT','LA','MA','ME','MSME','MT','NA','PH']
    connection = sqlite3.connect(db_filepath)
    cursor = connection.cursor()

    for discipline in disciplines:

        cursor.execute(f"SELECT course_code FROM TimeTable_Generator_coursedata WHERE discipline='{discipline}'")
        code_rows = cursor.fetchall()
        for Tuple in code_rows:
            for code in Tuple:

                context[f'{discipline}'].append(code)





    connection.close()
    return context



def fetch_course_info_db(db_filepath,code):
    connection = sqlite3.connect(db_filepath)
    cursor = connection.cursor()

    # Query certain columns

    cursor.execute(f"SELECT course_code,course_name,slot FROM TimeTable_Generator_coursedata WHERE course_code='{code}'")
    rows = cursor.fetchall()


    connection.close()
    return list(rows[0])

def generate_pdf(content):
    index=content[0]
    clashes=content[1]
    Day = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thrusday", 5: "Friday"}
    """ LOADING DATA IN PDF """

    pdf = FPDF(orientation="P", unit="mm", format="A4" )

    pdf.add_page()


    # TITLE ROW
    pdf.set_font(family="Times", size=8, style="B")
    pdf.set_text_color(0, 0, 0)
    pdf.set_fill_color(148, 255, 255)  # 94FFFF(teal bluish)
    pdf.cell(w=20, h=8, txt="Day", border=1)

    pdf.cell(w=20, h=8, txt="8:30-9:25", border=1)
    pdf.cell(w=20, h=8, txt="9:30-20:25", border=1)
    pdf.cell(w=20, h=8, txt="20:30-11:25", border=1)
    pdf.cell(w=20, h=8, txt="11:30-12:25", border=1)
    pdf.cell(w=20, h=8, txt="12:30-1:25", border=1)
    pdf.cell(w=20, h=8, txt="2:30-3:25", border=1)
    pdf.cell(w=20, h=8, txt="3:30-4:25", border=1)
    pdf.cell(w=20, h=8, txt="4:30-5:25", border=1, ln=1)

    # Adding  courses  in table
    pattern = re.compile("[0-9]{3}") # course codes have 3 digits in the end
    for i in range(1, 6, 1):
        pdf.cell(w=20, h=8, txt=Day[i], border=1)
        for j in range(1, 9, 1):
            if j != 8:
                if re.findall(pattern, index[(i * 10 + j)]) != []:
                    pdf.cell(w=20, h=8, txt=index[(i * 10 + j)], border=1,fill=True) # coloring cells which have courses
                else:
                    pdf.cell(w=20, h=8, txt=index[(i * 10 + j)], border=1, fill=False)
            else:
                if re.findall(pattern, index[(i * 10 + j)]) != []:
                    pdf.cell(w=20, h=8, txt=index[(i * 10 + j)], border=1,fill=True,ln=1) # coloring cells which have courses
                else:
                    pdf.cell(w=20, h=8, txt=index[(i * 10 + j)], border=1, fill=False,ln=1)

    # adding clash messages
    pdf.ln(80)
    pdf.set_font(family="Times", size=13)

    pdf.cell(w=100, h=8, txt="Clash Detection:", ln=2)

    pdf.set_font(family="Times", size=9)

    if clashes==[]: # no clashes
        pdf.cell(w=100, h=8, txt="No clashes Detected")
    else:
        for clash in clashes:
            pdf.cell(w=100, h=8, txt=clash,ln=1)



    pdf.output(f"TT.pdf")

def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


if __name__ == "__main__":
    fetch_course_codes_db("db.sqlite3")
    """courses=[]
    while True:
        course_code=input(" Enter course code . (break to stop) :").upper()
        if(course_code=="BREAK"):
            break
        else:
            courses.append(course_code)"""

    """ users must be given a drop down to choose their courses as courses like IC202 must be refereed
    as IC202/MA506 to fetch data"""

    """print(courses)

    index=fetch_csv_data(user_input=courses)
    generate_pdf(index=index)"""