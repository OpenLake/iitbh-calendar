export const backendDomain = "http://localhost:8080"

export interface Course {
    id: number;
    course_code: string;
    course_name: string;
    slot: string;
    room: string;
    discipline: string;
    instructor: string;
}

export interface timetable {
    mapping: {
        [key: string]: string | string[];
    };
    clashes: string[];
    additional_messages: string[]
}

export const timeSlots = [
    "8:30-9:25",
    "9:30-20:25",
    "20:30-11:25",
    "11:30-12:25",
    "12:30-1:25",
    "2:30-3:25",
    "3:30-4:25",
    "4:30-5:25",
];

export const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];