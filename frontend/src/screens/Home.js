import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Navbar, Nav, Card, Form, FormControl, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom'; // Import useNavigate for navigation

const Home = () => {
    const [categories, setCategories] = useState([]);
    const [posts, setPosts] = useState([]);
    const [searchTerm, setSearchTerm] = useState(''); // For search input
    const navigate = useNavigate(); // Initialize useNavigate

    useEffect(() => {
        const fetchCategories = async () => {
            try {
                const token = localStorage.getItem('access_token');
                console.log('Token:', token);
                const response = await axios.get('http://127.0.0.1:8000/admin-app/categories/', {
                    headers: {
                        Authorization: `JWT ${token}`,
                    },
                });
                setCategories(response.data);
            } catch (error) {
                console.error('Error fetching categories:', error);
            }
        };

        const fetchPosts = async () => {
            try {
                const token = localStorage.getItem('access_token');
                const response = await axios.get('http://127.0.0.1:8000/blog/posts/', {
                    headers: {
                        Authorization: `JWT ${token}`,
                    },
                });
                setPosts(response.data);
            } catch (error) {
                console.error('Error fetching posts:', error);
            }
        };

        fetchCategories();
        fetchPosts();
    }, []);

    // Handle search input changes
    const handleSearchChange = (e) => {
        setSearchTerm(e.target.value);
    };

    // Handle search form submission
    const handleSearchSubmit = async (e) => {
        e.preventDefault(); // Prevent page reload
        try {
            const token = localStorage.getItem('access_token');
            const response = await axios.get(`http://127.0.0.1:8000/blog/posts/search/?q=${searchTerm}`, {
                headers: {
                    Authorization: `JWT ${token}`,
                },
            });
            setPosts(response.data); // Update posts based on search result
        } catch (error) {
            console.error('Error searching posts:', error);
        }
    };

    // Handle navigation to Post.js
    const handleNavigateToPost = () => {
        navigate('/post'); // Redirects to the Post.js route
    };

    return (
        <div>
            <Navbar bg="light" expand="lg">
                <Navbar.Brand href="#home">Blog</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="ml-auto">
                        {categories.map((category) => (
                            <Nav.Link key={category.id} href={`#${category.name}`}>
                                {category.name}
                            </Nav.Link>
                        ))}
                    </Nav>
                    <Form className="ml-auto" inline onSubmit={handleSearchSubmit}> {/* Search bar */}
                        <FormControl
                            type="text"
                            placeholder="Search by category or tag"
                            className="mr-sm-2"
                            value={searchTerm}
                            onChange={handleSearchChange}
                        />
                        <Button variant="outline-success" type="submit">Search</Button>
                    </Form>
                </Navbar.Collapse>
            </Navbar>

            <div className="container mt-3 d-flex justify-content-between">
                <h1>Welcome to the Blog</h1>
                <Button variant="primary" onClick={handleNavigateToPost}>Post</Button> {/* Post button */}
            </div>

            <div className="container mt-3">
                <div>
                    {posts.length > 0 ? (
                        posts.map((post) => (
                            <Card key={post.id} className="mb-4">
                                <Card.Body>
                                    <Card.Title>{post.title}</Card.Title>
                                    <Card.Subtitle className="mb-2 text-muted">Author: {post.author}</Card.Subtitle>
                                    {post.image && (
                                        <Card.Img
                                            variant="top"
                                            src={`http://127.0.0.1:8000${post.image}`}
                                            alt={post.title}
                                            className="mb-3"
                                        />
                                    )}
                                    <Card.Text>{post.content}</Card.Text>
                                </Card.Body>
                            </Card>
                        ))
                    ) : (
                        <p>No posts available.</p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Home;