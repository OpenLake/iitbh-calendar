import re
import django
import os
# Set your Django settings module (replace 'your_project_name.settings' accordingly)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from api.models import CourseData


def process_submission(user_input):

    index = {11: "A1", 12: "B1", 13: "C1", 14: "E1", 15: "G1", 16: "K1", 17: "L1", 18: "I1",
             21: "B2", 22: "D1", 23: "C2", 24: "  ", 25: "H1", 26: "L2", 27: "J1", 28: "M1",
             31: "E2", 32: "A2", 33: "D2", 34: "F1", 35: "G2", 36: "K2", 37: "M2", 38: "I2",
             41: "F2", 42: "B3", 43: "C3", 44: "E3", 45: "H2", 46: "L3", 47: "M3", 48: "J2",
             51: "G3", 52: "A3", 53: "D3", 54: "F3", 55: "H3", 56: "K3", 57: "J3", 58: "I3",
             0:[]}
    # Value of index dictionary changes every time program is run

    permanent_index = {11: "A1", 12: "B1", 13: "C1", 14: "E1", 15: "G1", 16: "K1", 17: "L1", 18: "I1",
             21: "B2", 22: "D1", 23: "C2", 24: "  ", 25: "H1", 26: "L2", 27: "J1", 28: "M1",
             31: "E2", 32: "A2", 33: "D2", 34: "F1", 35: "G2", 36: "K2", 37: "M2", 38: "I2",
             41: "F2", 42: "B3", 43: "C3", 44: "E3", 45: "H2", 46: "L3", 47: "M3", 48: "J2",
             51: "G3", 52: "A3", 53: "D3", 54: "F3", 55: "H3", 56: "K3", 57: "J3", 58: "I3",
             0:[]}

    Slot_key = {"A1": 11, "B1": 12, "C1": 13, "E1": 14, "G1": 15, "K1": 16, "L1": 17, "I1": 18,
                "B2": 21, "D1": 22, "C2": 23, "BLANK": 24,"H1": 25, "L2": 26, "J1": 27, "M1": 28,
                "E2": 31, "A2": 32, "D2": 33, "F1": 34, "G2": 35, "K2": 36, "M2": 37, "I2": 38,
                "F2": 41, "B3": 42, "C3": 43, "E3": 44, "H2": 45, "L3": 46, "M3": 47, "J2": 48,
                "G3": 51, "A3": 52, "D3": 53, "F3": 54, "H3": 55, "K3": 56, "J3": 57, "I3": 58,

                "MSG":0}

    keys = []
    slots = []
    course_codes=[]
    for course_id in user_input:
        try:
            course = CourseData.objects.get(id=course_id)
            slot_list = course.slot.split(',') if course.slot else []
            slots.append(slot_list)
            course_codes.append(course.course_code)
        except CourseData.DoesNotExist:
            return course_id



    pattern1 = re.compile("[A-Z]{1}[0-9]{2}")  # for D12 vaghera
    pattern2 = re.compile("[A-Z]{1}[0-9]{1}")  # for D1


    for course_slot in slots:

        add = []

        for slot in course_slot:
            slot = slot.strip()

            if re.findall(pattern1, slot) == []:
                if re.findall(pattern2, slot) == []:  # single alphabet or (LAB/TBA/NA (ie text string))

                    alphabet = slot
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

                        case "A"|"B"|"C"|"D"|"E"|"F"|"G"|"H"|"I"|"J"|"K"|"L"|"M" :
                            add.append(Slot_key[f"{alphabet}1"])
                            add.append(Slot_key[f"{alphabet}2"])
                            add.append(Slot_key[f"{alphabet}3"])


                        case _: # NON DEFINED SLOTS
                            add.append(Slot_key["MSG"])


                else:
                    add.append(Slot_key[slot])
            else:
                alphabet = slot[0]
                dig_1 = slot[1]
                dig_2 = slot[2]

                add.append(Slot_key[f"{alphabet}{dig_1}"])
                add.append(Slot_key[f"{alphabet}{dig_2}"])
        keys.append(add)


    clashes=[]
    additional_messages = []  # to indicate lab / na courses
    pattern = re.compile("[0-9]{3}")  # course codes have 3 digits in the end
    i = 0
    for lst in keys:
        for key in lst:
            if key==0: # NA slots
                index[key].append(course_codes[i])

            else:
                if re.findall(pattern, index[key]) != []: # clash has occured course is already present in that section
                    clashes.append(f"Course {course_codes[i]} is clashing with {index[key]} in the {permanent_index[key]} slot ")

                else:
                    index[key] = course_codes[i]

        i = i + 1
    for NA_courses in index[0]:
        additional_messages.append(f"Course {NA_courses} has no slot defined")

    index.pop(0)

    content=[index,clashes,additional_messages]

    return content



if __name__ == "__main__":
    process_submission(user_input=[1,2,3,4])
