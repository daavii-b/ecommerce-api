import { configureStore } from '@reduxjs/toolkit';
import rootReducer, { initialState } from './modules/rootReducer';

const store = configureStore({
  reducer: rootReducer,
  preloadedState: initialState,
});

export default store;
