// src/redux/store.ts
import { configureStore } from '@reduxjs/toolkit';
import timetableReducer from './slices/timetableSlice';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';

const persistConfig = {
    key: 'root',
    storage,
    whitelist: ['timetable'] // only persist timetable
};

const persistedReducer = persistReducer(persistConfig, timetableReducer);

export const store = configureStore({
    reducer: {
        timetable: persistedReducer,
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({
            serializableCheck: {
                ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE', 'persist/REGISTER'],
            },
        }),
});

export const persistor = persistStore(store);

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;