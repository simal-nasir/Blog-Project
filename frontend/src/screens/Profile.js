import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Card, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

const Profile = () => {
    const [profile, setProfile] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const token = localStorage.getItem('access_token');
                const response = await axios.get('http://127.0.0.1:8000/blog/profile/', {
                    headers: {
                        Authorization: `JWT ${token}`,
                    },
                });
                setProfile(response.data);
            } catch (error) {
                console.error('Error fetching profile:', error);
                if (error.response && error.response.status === 401) {
                    navigate('/login');
                }
            }
        };

        fetchProfile();
    }, [navigate]);

    if (!profile) {
        return <p>Loading profile...</p>;
    }

    return (
        <div className="container mt-5">
            <Card className="text-center">
                <Card.Body>
                    <Card.Title>{profile.name}</Card.Title>
                    <Card.Subtitle className="mb-2 text-muted">{profile.email}</Card.Subtitle>
                    {profile.profile_picture && (
                        <Card.Img
                            variant="top"
                            src={`http://127.0.0.1:8000${profile.profile_picture}`}
                            alt="Profile"
                            className="mb-3"
                            style={{ width: '150px', height: '150px', borderRadius: '50%', objectFit: 'cover' }}
                        />
                    )}
                    <Card.Text>{profile.bio}</Card.Text>
                    <Button variant="primary" onClick={() => navigate('/edit-profile')}>
                        Edit Profile
                    </Button>
                </Card.Body>
            </Card>
        </div>
    );
};

export default Profile;