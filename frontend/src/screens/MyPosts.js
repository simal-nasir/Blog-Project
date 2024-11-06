import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Card, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

const MyPosts = () => {
    const [myPosts, setMyPosts] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchMyPosts = async () => {
            try {
                const token = localStorage.getItem('access_token');
                const response = await axios.get('http://127.0.0.1:8000/blog/my-posts/', {
                    headers: {
                        Authorization: `JWT ${token}`,
                    },
                });
                setMyPosts(response.data);
            } catch (error) {
                console.error('Error fetching my posts:', error);
            }
        };

        fetchMyPosts();
    }, []);

    const handleNavigateToPostDetail = (postId) => {
        navigate(`/post/${postId}`); // Navigate to PostDetail.js with post ID
    };

    return (
        <div className="container mt-3">
            <h2>My Posts</h2>
            {myPosts.length > 0 ? (
                myPosts.map((post) => (
                    <Card key={post.id} className="mb-4" onClick={() => handleNavigateToPostDetail(post.id)}>
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
            <Button variant="primary" onClick={() => navigate('/post')}>Create New Post</Button>
        </div>
    );
};

export default MyPosts;