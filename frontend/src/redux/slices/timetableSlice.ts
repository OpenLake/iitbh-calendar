import { timetable } from "@/src/lib/types";
import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { TimetablePayload } from "@/src/lib/types";

const initialState: timetable = {
    mapping: {},
    clashes: [],
    additional_messages: []
}

export const timetableSlice = createSlice({
    name: "timetable",
    initialState: initialState,
    reducers: {
        setTimetable: (state, action: PayloadAction<TimetablePayload>) => {
            state.mapping = action.payload.mapping;
            state.clashes = action.payload.clashes;
            state.additional_messages = action.payload.additional_messages
        },
        clearTimetable: (state) => {
            state.additional_messages = [],
                state.clashes = [],
                state.mapping = {}
        }
    }
})

export const { setTimetable, clearTimetable } = timetableSlice.actions;
export default timetableSlice.reducer;












