import React from 'react';
import './App.css';
import Chat from './components/Chat';

function App() {
  return (
    <div className="App">
      <div className="chat-wrapper">
        <h1>Pigeon чат</h1>
        <Chat roomName="general" /> {/* Указываем название комнаты */}
      </div>
    </div>
  );
}

export default App;