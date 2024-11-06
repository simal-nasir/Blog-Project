import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, Button } from 'react-bootstrap';

const PostDetail = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [post, setPost] = useState(null);
    const [currentUser, setCurrentUser] = useState(null);

    useEffect(() => {
        const fetchPost = async () => {
            try {
                const token = localStorage.getItem('access_token');
                
                // Fetch post details
                const response = await axios.get(`http://127.0.0.1:8000/blog/posts/${id}/`, {
                    headers: {
                        Authorization: `JWT ${token}`,
                    },
                });
                setPost(response.data);
                console.log('Post data:', response.data);

                const userResponse = await axios.get('http://127.0.0.1:8000/auth/users/me/', {
                    headers: {
                        Authorization: `JWT ${token}`,
                    },
                });
                setCurrentUser(userResponse.data);
                console.log('Current user:', userResponse.data);
            } catch (error) {
                console.error('Error fetching post or user:', error);
            }
        };

        fetchPost();
    }, [id]);

    const handleDelete = async () => {
        try {
            const token = localStorage.getItem('access_token');
            await axios.delete(`http://127.0.0.1:8000/blog/posts/${id}/delete/`, {
                headers: {
                    Authorization: `JWT ${token}`,
                },
            });
            alert('Post deleted successfully');
            navigate('/home');
        } catch (error) {
            console.error('Error deleting post:', error);
            alert('Failed to delete the post');
        }
    };

    const handleEdit = () => {
        navigate(`/edit/${id}`);
    };

    if (!post) return <p>Loading...</p>;

    // Assuming post.author_id is available
    const isAuthor = currentUser && post.author_id === currentUser.id;
    console.log('Is author:', isAuthor);

    return (
        <div className="container mt-3">
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

                    {isAuthor && (
                        <div className="mt-3">
                            <Button variant="warning" onClick={handleEdit} className="mr-2">Edit</Button>
                            <Button variant="danger" onClick={handleDelete}>Delete</Button>
                        </div>
                    )}
                </Card.Body>
            </Card>
        </div>
    );
};

export default PostDetail;