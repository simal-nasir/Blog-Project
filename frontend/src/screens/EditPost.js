import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Form, Button } from 'react-bootstrap';

const EditPost = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [post, setPost] = useState({
        title: '',
        content: '',
        category: '',
        // Add other fields if necessary
    });
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchPost = async () => {
            try {
                const token = localStorage.getItem('access_token');
                const response = await axios.get(`http://127.0.0.1:8000/blog/posts/${id}/`, {
                    headers: {
                        Authorization: `JWT ${token}`,
                    },
                });
                setPost(response.data);
            } catch (error) {
                console.error('Error fetching post:', error);
                setError('Failed to fetch post data');
            }
        };

        fetchPost();
    }, [id]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setPost({ ...post, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const token = localStorage.getItem('access_token');
            await axios.put(`http://127.0.0.1:8000/blog/posts/${id}/edit/`, post, {
                headers: {
                    Authorization: `JWT ${token}`,
                },
            });
            alert('Post updated successfully');
            navigate(`/posts/${id}`); // Redirect to the post detail after editing
        } catch (error) {
            console.error('Error updating post:', error);
            setError('Failed to update post');
        }
    };

    if (error) return <p>{error}</p>;

    return (
        <div className="container mt-3">
            <h2>Edit Post</h2>
            <Form onSubmit={handleSubmit}>
                <Form.Group controlId="formTitle">
                    <Form.Label>Title</Form.Label>
                    <Form.Control
                        type="text"
                        name="title"
                        value={post.title}
                        onChange={handleChange}
                        required
                    />
                </Form.Group>

                <Form.Group controlId="formContent">
                    <Form.Label>Content</Form.Label>
                    <Form.Control
                        as="textarea"
                        rows={5}
                        name="content"
                        value={post.content}
                        onChange={handleChange}
                        required
                    />
                </Form.Group>

                <Form.Group controlId="formCategory">
                    <Form.Label>Category</Form.Label>
                    <Form.Control
                        type="text"
                        name="category"
                        value={post.category}
                        onChange={handleChange}
                        required
                    />
                </Form.Group>

                {/* Add more fields as necessary */}

                <Button variant="primary" type="submit">
                    Update Post
                </Button>
            </Form>
        </div>
    );
};

export default EditPost;