import React, { useState } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navigation from './components/Navigation';
import Login from './components/Login';
import ProtectedRoute from './components/ProtectedRoute';
import './App.css';

function App() {
  const [typingData, setTypingData] = useState([]);
  
  const handleKeyPress = (event) => {
    const newTypingData = [...typingData, {
      key: event.key,
      timestamp: Date.now(),
      keydown: true
    }];
    setTypingData(newTypingData);
  };

  const handleKeyRelease = (event) => {
    const newTypingData = [...typingData, {
      key: event.key,
      timestamp: Date.now(),
      keydown: false
    }];
    setTypingData(newTypingData);
  };

  const handleSubmit = async () => {
    try {
      const response = await axios.post('http://localhost:3000/collect', {
        userId: 'test-user',
        typingData
      });
      console.log('Analysis result:', response.data);
      setTypingData([]);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <Router>
      <div className="App">
        <Navigation />
        <main className="main-content">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route
              path="/applications"
              element={
                <ProtectedRoute>
                  <div className="App">
                    <h1>Keyboard Dynamics Demo</h1>
                    <textarea
                      onKeyDown={handleKeyPress}
                      onKeyUp={handleKeyRelease}
                      placeholder="Type something here..."
                      rows={4}
                      cols={50}
                    />
                    <br />
                    <button onClick={handleSubmit}>Analyze Typing Pattern</button>
                  </div>
                </ProtectedRoute>
              }
            />
            <Route
              path="/applications/:id"
              element={
                <ProtectedRoute>
                  <div>Application Details</div>
                </ProtectedRoute>
              }
            />
            <Route path="/" element={<Navigate to="/applications" replace />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
