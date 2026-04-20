import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Chat from './components/Chat';
import Home from './components/Home';

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/chat" element={
            <div className="chat-wrapper">
              <h1>Pigeon чат</h1>
              <Chat roomName="general" />
            </div>
          } />
        </Routes>
      </Router>
    </div>
  );
}

export default App;