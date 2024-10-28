import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Navbar, Nav, Card, Form, FormControl, Button, Modal } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

const AdminScreen = () => {
    const [categories, setCategories] = useState([]);
    const [posts, setPosts] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [showCreateCategoryModal, setShowCreateCategoryModal] = useState(false);
    const [newCategory, setNewCategory] = useState('');
    const [error, setError] = useState('');
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
                setPosts(response.data);
            } catch (error) {
                console.error('Error fetching posts:', error);
            }
        };

        fetchCategories();
        fetchPosts();
    }, []);

    const handleSearchChange = (e) => {
        setSearchTerm(e.target.value);
    };

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

    const handleNavigateToPost = () => {
        navigate('/post');
    };

    const handleCreateCategory = async () => {
        try {
            const token = localStorage.getItem('access_token');
            const response = await axios.post(
                'http://127.0.0.1:8000/admin-app/categories/create/',
                { name: newCategory },
                {
                    headers: {
                        Authorization: `JWT ${token}`,
                    },
                }
            );

            setCategories([...categories, response.data]); // Update categories list
            setShowCreateCategoryModal(false); // Close modal
            setNewCategory('');
            setError('');
        } catch (error) {
            console.error('Error creating category:', error);
            setError('Failed to create category. Ensure you have superuser access.');
        }
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
                        <Button variant="link" onClick={() => setShowCreateCategoryModal(true)}>
                            Create Category
                        </Button>
                    </Nav>
                    <Form className="ml-auto" inline onSubmit={handleSearchSubmit}>
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
                <Button variant="primary" onClick={handleNavigateToPost}>Post</Button>
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

            {/* Create Category Modal */}
            <Modal show={showCreateCategoryModal} onHide={() => setShowCreateCategoryModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>Create a New Category</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {error && <p className="text-danger">{error}</p>}
                    <Form.Group controlId="formNewCategory">
                        <Form.Label>Category Name</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Enter category name"
                            value={newCategory}
                            onChange={(e) => setNewCategory(e.target.value)}
                            required
                        />
                    </Form.Group>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShowCreateCategoryModal(false)}>
                        Close
                    </Button>
                    <Button variant="primary" onClick={handleCreateCategory}>
                        Create Category
                    </Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
};

export default AdminScreen;