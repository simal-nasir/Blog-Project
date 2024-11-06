import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

const AccountActivation = () => {
    const { uid, token } = useParams();
    const navigate = useNavigate();

    useEffect(() => {
        const activateAccount = async () => {
            try {
                const response = await axios.post('http://localhost:8000/auth/users/activation/', {
                    uid,
                    token,
                });
                if (response.status === 204) {
                    alert("Your account has been successfully activated!");
                    navigate('/login');  // Redirect to the login page
                }
            } catch (error) {
                console.error('Account activation failed:', error);
                alert("Failed to activate your account. Please try again or contact support.");
            }
        };

        activateAccount();
    }, [uid, token, navigate]);

    return (
        <div>
            <h2>Activating your account...</h2>
            <p>Please wait a moment.</p>
        </div>
    );
};

export default AccountActivation;