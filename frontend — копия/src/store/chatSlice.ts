import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface Message {
  id: number;
  content: string;
  sender: string;
  timestamp: string;
}

const chatSlice = createSlice({
  name: 'chat',
  initialState: {
    messages: [] as Message[],
    isConnected: false
  },
  reducers: {
    addMessage: (state, action: PayloadAction<Message>) => {
      state.messages.push(action.payload);
    },
    setConnectionStatus: (state, action: PayloadAction<boolean>) => {
      state.isConnected = action.payload;
    }
  }
});

export const { addMessage, setConnectionStatus } = chatSlice.actions;
export default chatSlice.reducer;