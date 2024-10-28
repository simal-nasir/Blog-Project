import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Form, Button, Alert } from 'react-bootstrap';

const Post = () => {
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [image, setImage] = useState(null);
    const [categories, setCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const navigate = useNavigate();

    // Fetch categories from the API
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

        fetchCategories();
    }, []);

    // Handle file input change (for the image)
    const handleImageChange = (e) => {
        setImage(e.target.files[0]);
    };

    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();
        const token = localStorage.getItem('access_token');

        // Create FormData object to include image and text data
        const formData = new FormData();
        formData.append('title', title);
        formData.append('content', content);
        formData.append('category', selectedCategory); // Add selected category to formData
        if (image) {
            formData.append('image', image); // Add image if provided
        }

        try {
            const response = await axios.post('http://127.0.0.1:8000/blog/posts/create/', formData, {
                headers: {
                    Authorization: `JWT ${token}`,
                    'Content-Type': 'multipart/form-data',
                },
            });

            setSuccess('Post created successfully!');
            setError('');

            // Reset form fields after submission
            setTitle('');
            setContent('');
            setImage(null);
            setSelectedCategory(''); // Reset selected category

            // Optionally redirect to another page after success
            setTimeout(() => {
                navigate('/home');
            }, 2000);
        } catch (error) {
            console.error('Error creating post:', error);
            setError('Failed to create the post. Please try again.');
            setSuccess('');
        }
    };

    return (
        <div className="container mt-3">
            <h1>Create a New Post</h1>

            {error && <Alert variant="danger">{error}</Alert>}
            {success && <Alert variant="success">{success}</Alert>}

            <Form onSubmit={handleSubmit}>
                <Form.Group controlId="formTitle">
                    <Form.Label>Title</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Enter post title"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        required
                    />
                </Form.Group>

                <Form.Group controlId="formContent" className="mt-3">
                    <Form.Label>Content</Form.Label>
                    <Form.Control
                        as="textarea"
                        rows={5}
                        placeholder="Enter post content"
                        value={content}
                        onChange={(e) => setContent(e.target.value)}
                        required
                    />
                </Form.Group>

                <Form.Group controlId="formCategory" className="mt-3">
                    <Form.Label>Select Category</Form.Label>
                    <Form.Select
                        value={selectedCategory}
                        onChange={(e) => setSelectedCategory(e.target.value)}
                        required
                    >
                        <option value="">Choose a category</option>
                        {categories.map((category) => (
                            <option key={category.id} value={category.id}>
                                {category.name}
                            </option>
                        ))}
                    </Form.Select>
                </Form.Group>

                <Form.Group controlId="formImage" className="mt-3">
                    <Form.Label>Upload an Image (optional)</Form.Label>
                    <Form.Control
                        type="file"
                        accept="image/*"
                        onChange={handleImageChange}
                    />
                </Form.Group>

                <Button variant="primary" type="submit" className="mt-3">
                    Submit Post
                </Button>
            </Form>
        </div>
    );
};

export default Post;