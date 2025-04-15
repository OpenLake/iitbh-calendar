import { timetable } from "@/src/lib/types";
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

const initialState: timetable = {
    mapping: {},
    clashes: [],
    additional_messages: []
}

export const timetableSlice = createSlice({
    name: "timetable",
    initialState: initialState,
    reducers: {
        setTimetable: (state, action: PayloadAction<timetable>) => {
            state.mapping = action.payload.mapping;
            state.clashes = action.payload.clashes;
            state.additional_messages = action.payload.additional_messages
        }
    }
})

export const { setTimetable } = timetableSlice.actions;
export default timetableSlice.reducer;












