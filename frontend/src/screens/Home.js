import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Navbar, Nav, Card, Form, FormControl, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

const Home = () => {
    const [categories, setCategories] = useState([]);
    const [posts, setPosts] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const fetchCategories = async () => {
            try {
                const token = localStorage.getItem('access_token');
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
                setPosts(response.data.map(post => ({ ...post, liked: false, disliked: false })));
            } catch (error) {
                console.error('Error fetching posts:', error);
            }
        };

        fetchCategories();
        fetchPosts();
    }, []);

    const handleSearchChange = (e) => setSearchTerm(e.target.value);

    const handleSearchSubmit = async (e) => {
        e.preventDefault();
        try {
            const token = localStorage.getItem('access_token');
            const response = await axios.get(`http://127.0.0.1:8000/blog/posts/search/?q=${searchTerm}`, {
                headers: {
                    Authorization: `JWT ${token}`,
                },
            });
            setPosts(response.data);
        } catch (error) {
            console.error('Error searching posts:', error);
        }
    };

    const handleNavigateToPostDetail = (postId) => {
        navigate(`/post/${postId}`);
    };

    const handleLike = async (postId) => {
        try {
            const token = localStorage.getItem('access_token');
            const response = await axios.post(`http://127.0.0.1:8000/blog/posts/${postId}/like/`, {}, {
                headers: {
                    Authorization: `JWT ${token}`,
                },
            });
            console.log('Like response:', response.data);

            setPosts((prevPosts) => 
                prevPosts.map(post => 
                    post.id === postId 
                        ? { 
                            ...post, 
                            like_count: response.data.likes,
                            liked: true, 
                            disliked: false 
                        } 
                        : post
                )
            );
        } catch (error) {
            console.error('Error liking the post:', error);
        }
    };

    const handleDislike = async (postId) => {
        try {
            const token = localStorage.getItem('access_token');
            const response = await axios.post(`http://127.0.0.1:8000/blog/posts/${postId}/dislike/`, {}, {
                headers: {
                    Authorization: `JWT ${token}`,
                },
            });
            console.log('Dislike response:', response.data);

            setPosts((prevPosts) => 
                prevPosts.map(post => 
                    post.id === postId 
                        ? { 
                            ...post, 
                            dislikes_count: response.data.dislikes, 
                            disliked: true, 
                            liked: false 
                        } 
                        : post
                )
            );
        } catch (error) {
            console.error('Error disliking the post:', error);
        }
    };

    return (
        <div>
            <Navbar bg="light" expand="lg">
                <Navbar.Brand>Blog</Navbar.Brand>
                <Navbar.Brand href="/home">Home</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="me-auto">
                        {categories.map((category) => (
                            <Nav.Link key={category.id} href={`#${category.name}`}>
                                {category.name}
                            </Nav.Link>
                        ))}
                        <Nav.Link onClick={() => navigate('/my-posts')}>My Posts</Nav.Link>
                    </Nav>
                    <Form className="d-flex me-2" onSubmit={handleSearchSubmit}>
                        <FormControl
                            type="text"
                            placeholder="Search by category or tag"
                            className="me-2"
                            value={searchTerm}
                            onChange={handleSearchChange}
                        />
                        <Button variant="outline-success" type="submit">Search</Button>
                    </Form>
                    <Button variant="outline-primary" onClick={() => navigate('/profile')}>Profile</Button>
                </Navbar.Collapse>
            </Navbar>

            <div className="container mt-3 d-flex justify-content-between">
                <h1>Welcome to the Blog Website</h1>
                <Button variant="primary" onClick={() => navigate('/post')}>Post</Button>
            </div>

            <div className="container mt-3">
                {posts.length > 0 ? (
                    posts.map((post) => (
                        <Card key={post.id} className="mb-4">
                            <Card.Body onClick={() => handleNavigateToPostDetail(post.id)}>
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
                            <Card.Footer>
                                <Button 
                                    variant={post.liked ? "primary" : "outline-primary"} 
                                    onClick={(e) => { 
                                        e.stopPropagation(); 
                                        handleLike(post.id); 
                                    }}
                                >
                                    Like ({post.like_count || 0}) {/* Show like count */}
                                </Button>{' '}
                                <Button 
                                    variant={post.disliked ? "secondary" : "outline-secondary"} 
                                    onClick={(e) => { 
                                        e.stopPropagation(); 
                                        handleDislike(post.id); 
                                    }}
                                >
                                    Dislike ({post.dislike_count || 0}) {/* Show dislike count */}
                                </Button>
                            </Card.Footer>
                        </Card>
                    ))
                ) : (
                    <p>No posts available.</p>
                )}
            </div>
        </div>
    );
};

export default Home;