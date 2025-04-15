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

