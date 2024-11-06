import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './screens/Login';
import AccountActivation from './screens/AccountActivation';
import Home from './screens/Home';
import Post from './screens/Post';
import PostDetail from './screens/PostDetail';
import EditPost from './screens/EditPost';
import MyPosts from './screens/MyPosts';
import AdminScreen from './screens/AdminScreen';
import AdminPostDetail from './screens/AdminPostDetail';
import Profile from './screens/Profile';
import EditProfile from './screens/EditProfile';
import 'bootstrap/dist/css/bootstrap.min.css';
import Register from './screens/Register';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/activate/:uid/:token" element={<AccountActivation />} />
          <Route path="/" element={<Login/>} />
          <Route path="/register" element={<Register/>} />
          <Route path="/admin" element={<AdminScreen/>} />
          <Route path="/home" element={<Home/>} />
          <Route path="/post" element={<Post/>} />
          <Route path="/post/:id" element={<PostDetail/>} />
          <Route path="/edit/:id" element={<EditPost/>} />
          <Route path="/my-posts" element={<MyPosts/>} />
          <Route path="/admin-app/post/:id" element={<AdminPostDetail/>} />
          <Route path="/profile" element={<Profile/>} />
          <Route path="/edit-profile" element={<EditProfile/>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;