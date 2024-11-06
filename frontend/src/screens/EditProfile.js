import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Form, Button, Container, Alert } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

const EditProfile = () => {
    const [profile, setProfile] = useState({
        name: '',
        bio: '',
        profile_picture: null,
    });
    const [successMessage, setSuccessMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
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
                setProfile({
                    name: response.data.name,
                    bio: response.data.bio,
                    profile_picture: response.data.profile_picture,
                });
            } catch (error) {
                console.error('Error fetching profile:', error);
                setErrorMessage('Could not load profile.');
            }
        };

        fetchProfile();
    }, []);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setProfile((prevProfile) => ({
            ...prevProfile,
            [name]: value,
        }));
    };

    const handleFileChange = (e) => {
        setProfile((prevProfile) => ({
            ...prevProfile,
            profile_picture: e.target.files[0],
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('name', profile.name);
        formData.append('bio', profile.bio);
        if (profile.profile_picture) {
            formData.append('profile_picture', profile.profile_picture);
        }

        try {
            const token = localStorage.getItem('access_token');
            await axios.put('http://127.0.0.1:8000/blog/profile/', formData, {
                headers: {
                    Authorization: `JWT ${token}`,
                    'Content-Type': 'multipart/form-data',
                },
            });
            setSuccessMessage('Profile updated successfully!');
            setErrorMessage('');
            navigate('/profile');
        } catch (error) {
            console.error('Error updating profile:', error);
            setErrorMessage('Could not update profile. Please try again.');
        }
    };

    return (
        <Container className="mt-5">
            <h2>Edit Profile</h2>
            {successMessage && <Alert variant="success">{successMessage}</Alert>}
            {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}
            <Form onSubmit={handleSubmit}>
                <Form.Group controlId="formName">
                    <Form.Label>Name</Form.Label>
                    <Form.Control
                        type="text"
                        name="name"
                        value={profile.name}
                        onChange={handleInputChange}
                        required
                    />
                </Form.Group>

                <Form.Group controlId="formBio" className="mt-3">
                    <Form.Label>Bio</Form.Label>
                    <Form.Control
                        as="textarea"
                        name="bio"
                        value={profile.bio}
                        onChange={handleInputChange}
                        rows={3}
                    />
                </Form.Group>

                <Form.Group controlId="formProfilePicture" className="mt-3">
                    <Form.Label>Profile Picture</Form.Label>
                    <Form.Control type="file" onChange={handleFileChange} />
                </Form.Group>

                <Button variant="primary" type="submit" className="mt-4">
                    Save Changes
                </Button>
            </Form>
        </Container>
    );
};

export default EditProfile;