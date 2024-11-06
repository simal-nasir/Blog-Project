import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Navbar, Nav, Button, Dropdown, DropdownButton, Form, FormControl, Card, Modal, Table } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import FileSaver from 'file-saver';

const AdminScreen = () => {
    const [categories, setCategories] = useState([]);
    const [posts, setPosts] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [showCreateCategoryModal, setShowCreateCategoryModal] = useState(false);
    const [newCategoryName, setNewCategoryName] = useState('');
    const [selectedPost, setSelectedPost] = useState(null);
    const [showPostModal, setShowPostModal] = useState(false);
    const [showUsersModal, setShowUsersModal] = useState(false);
    const [users, setUsers] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        fetchCategories();
        fetchPosts();
    }, []);

    const fetchCategories = async () => {
        try {
            const token = localStorage.getItem('access_token');
            const response = await axios.get('http://127.0.0.1:8000/admin-app/categories/', {
                headers: { Authorization: `JWT ${token}` },
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
                headers: { Authorization: `JWT ${token}` },
            });
            setPosts(response.data);
        } catch (error) {
            console.error('Error fetching posts:', error);
        }
    };

    const handleSearchChange = (e) => {
        setSearchTerm(e.target.value);
    };

    const handleSearchSubmit = (e) => {
        e.preventDefault();
        console.log('Search submitted with term:', searchTerm);
    };

    const handleExportCSV = async () => {
        try {
            const token = localStorage.getItem('access_token');
            const response = await axios.get('http://127.0.0.1:8000/admin-app/export/csv/', {
                headers: { Authorization: `JWT ${token}` },
                responseType: 'blob',
            });
            FileSaver.saveAs(response.data, 'users_export.csv');
        } catch (error) {
            console.error('Error exporting CSV:', error);
            alert('Failed to export CSV. Please ensure you are logged in.');
        }
    };

    const handleCreateCategory = async () => {
        try {
            const token = localStorage.getItem('access_token');
            await axios.post('http://127.0.0.1:8000/admin-app/categories/', {
                name: newCategoryName,
            }, {
                headers: { Authorization: `JWT ${token}` },
            });
            fetchCategories();
            setNewCategoryName('');
            setShowCreateCategoryModal(false);
        } catch (error) {
            console.error('Error creating category:', error);
        }
    };

    const handlePostClick = (post) => {
        setSelectedPost(post);
        setShowPostModal(true);
    };

    const navigateToPostPage = () => {
        navigate('/post');
    };

    // Fetch users data
    const fetchUsers = async () => {
        try {
            const token = localStorage.getItem('access_token');
            const response = await axios.get('http://127.0.0.1:8000/admin-app/users/', {
                headers: { Authorization: `JWT ${token}` },
            });
            setUsers(response.data);
            setShowUsersModal(true); // Open the modal after fetching users
        } catch (error) {
            console.error('Error fetching users:', error);
        }
    };

    return (
        <div>
            <Navbar bg="light" expand="lg">
                <Navbar.Brand href="#home">Admin Blog</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="me-auto">
                        {categories.map((category) => (
                            <Nav.Link key={category.id} href={`#${category.name}`}>
                                {category.name}
                            </Nav.Link>
                        ))}
                        <Button variant="link" onClick={() => setShowCreateCategoryModal(true)}>
                            Create Category
                        </Button>
                        <Button variant="primary" onClick={navigateToPostPage}>
                            Create Post
                        </Button>
                    </Nav>

                    <DropdownButton
                        id="dropdown-basic-button"
                        title="Admin Options"
                        variant="secondary"
                        className="me-2"
                    >
                        <Dropdown.Item onClick={handleExportCSV}>
                            Export CSV
                        </Dropdown.Item>
                        <Dropdown.Item onClick={fetchUsers}>
                            View Users
                        </Dropdown.Item>
                    </DropdownButton>

                    <Form className="d-flex" onSubmit={handleSearchSubmit}>
                        <FormControl
                            type="text"
                            placeholder="Search by category or tag"
                            className="me-2"
                            value={searchTerm}
                            onChange={handleSearchChange}
                        />
                        <Button variant="outline-success" type="submit">
                            Search
                        </Button>
                    </Form>
                </Navbar.Collapse>
            </Navbar>

            {/* Posts Section */}
            <div className="container mt-4">
                <h2>Posts</h2>
                {posts.length > 0 ? (
                    posts.map((post) => (
                        <Card key={post.id} className="mb-3" onClick={() => handlePostClick(post)} style={{ cursor: 'pointer' }}>
                            <Card.Body>
                                <Card.Title>{post.author}</Card.Title>
                                <Card.Title>{post.title}</Card.Title>
                                <Card.Text>{post.content.substring(0, 100)}...</Card.Text>
                            </Card.Body>
                        </Card>
                    ))
                ) : (
                    <p>No posts available.</p>
                )}
            </div>

            {/* Create Category Modal */}
            <Modal show={showCreateCategoryModal} onHide={() => setShowCreateCategoryModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>Create Category</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <Form.Group controlId="formBasicEmail">
                            <Form.Label>Category Name</Form.Label>
                            <Form.Control
                                type="text"
                                placeholder="Enter category name"
                                value={newCategoryName}
                                onChange={(e) => setNewCategoryName(e.target.value)}
                            />
                        </Form.Group>
                    </Form>
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

            {/* Post Details Modal */}
            <Modal show={showPostModal} onHide={() => setShowPostModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>{selectedPost?.title}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p>{selectedPost?.content}</p>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShowPostModal(false)}>
                        Close
                    </Button>
                </Modal.Footer>
            </Modal>

            {/* Users Modal */}
            <Modal show={showUsersModal} onHide={() => setShowUsersModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>User List</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Table striped bordered hover>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Email</th>
                                <th>Name</th>
                                <th>Is Active</th>
                                <th>Is Staff</th>
                            </tr>
                        </thead>
                        <tbody>
                            {users.map((user) => (
                                <tr key={user.id}>
                                    <td>{user.id}</td>
                                    <td>{user.email}</td>
                                    <td>{user.name}</td>
                                    <td>{user.is_active ? 'Yes' : 'No'}</td>
                                    <td>{user.is_staff ? 'Yes' : 'No'}</td>
                                </tr>
                            ))}
                        </tbody>
                    </Table>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShowUsersModal(false)}>
                        Close
                    </Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
};

export default AdminScreen;