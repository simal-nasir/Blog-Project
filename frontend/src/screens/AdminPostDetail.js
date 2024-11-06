import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Card, Button } from 'react-bootstrap';
import { useParams, useNavigate } from 'react-router-dom';

const AdminPostDetail = () => {
    const { postId } = useParams();
    const [post, setPost] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchPost = async () => {
            try {
                const token = localStorage.getItem('access_token');
                const response = await axios.get(`http://127.0.0.1:8000/blog/posts/${postId}/`, {
                    headers: {
                        Authorization: `JWT ${token}`,
                    },
                });
                setPost(response.data);
            } catch (error) {
                console.error('Error fetching post:', error);
            }
        };

        fetchPost();
    }, [postId]);

    const handleEdit = () => {
        navigate(`/admin-app/post/${postId}/edit`);
    };

    const handleDelete = async () => {
        if (window.confirm('Are you sure you want to delete this post?')) {
            try {
                const token = localStorage.getItem('access_token');
                await axios.delete(`http://127.0.0.1:8000/admin-app/post/${postId}/delete/`, {
                    headers: {
                        Authorization: `JWT ${token}`,
                    },
                });
                navigate('/admin'); // Redirect after deletion
            } catch (error) {
                console.error('Error deleting post:', error);
            }
        }
    };

    if (!post) return <p>Loading...</p>;

    return (
        <Card>
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
                <Button variant="danger" onClick={handleDelete}>Delete Post</Button>
                <Button variant="primary" onClick={handleEdit} className="ml-2">Edit Post</Button>
            </Card.Body>
        </Card>
    );
};

export default AdminPostDetail;