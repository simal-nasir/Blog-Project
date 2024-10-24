import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './screens/Login';
import Home from './screens/Home';
import Post from './screens/Post';
import 'bootstrap/dist/css/bootstrap.min.css';
import Register from './screens/Register';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Login/>} />
          <Route path="/register" element={<Register/>} />
          <Route path="/home" element={<Home/>} />
          <Route path="/post" element={<Post/>} />

        </Routes>
      </div>
    </Router>
  );
}

export default App;