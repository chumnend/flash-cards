import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import Loader from '../Loader';
import * as api from '../../../testing/api';
import type { IUser } from '../../helpers/types';
import { useAuthContext } from '../../helpers/context';

import './SettingsPage.css';

const SettingsPage = () => {
    const [isLoading, setIsLoading] = useState(true);
    const [user, setUser] = useState<IUser | null>(null);
    const [following, setFollowing] = useState<IUser[]>([]);
    const [infoForm, setInfoForm] = useState({
        firstName: '',
        lastName: '',
        email: '',
        aboutMe: '',
    });
    const [passwordForm, setPasswordForm] = useState({
        currentPassword: '',
        newPassword: '',
        confirmPassword: '',
    })

    const navigate = useNavigate();
    const { authUser } = useAuthContext();

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                if (!authUser) {
                    navigate('/login');
                    return;
                }
                const data = await api.profile(authUser.id);
                setUser(data.user);
                setFollowing(data.user.following);
                setInfoForm({
                    firstName: data.user.firstName,
                    lastName: data.user.lastName,
                    email: data.user.email,
                    aboutMe: data.user.details.aboutMe,
                });
            } catch (error) { 
                console.error(error);
                navigate('/error');
            } finally {
                setIsLoading(false);
            }
        }
        fetchProfile();
    }, [navigate, authUser])

    const handleUnfollow = async (id: string) => {
        if (!authUser) return;

        setIsLoading(true)

        try {
            await api.unfollow(authUser.id, id);
            setFollowing(prev => prev.filter(user => user.id !== id));
        } catch (error) {
            console.error(error)
        } finally {
            setIsLoading(false)
        }
    }

    const handleUpdateInfo = async (e: React.FormEvent) => {
        e.preventDefault();

        setIsLoading(true)

        try {
            await api.settings(
                authUser!.id,
                infoForm.firstName,
                infoForm.lastName,
                infoForm.email,
                infoForm.aboutMe,
            );
        } catch (error) {
            console.error(error);
        } finally {
            setIsLoading(false)
        }
    }

    const handleChangePassword = async (e: React.FormEvent) => {
        e.preventDefault();

        if (passwordForm.newPassword !== passwordForm.confirmPassword) {
            return;
        }

        setIsLoading(true)

        try {
            await api.changePassword(user!.id, passwordForm.newPassword);
        } catch (error) {
            console.error(error)
        } finally {
            setIsLoading(false)
        }
    }

    if (isLoading) {
        return <Loader />
    }

    return (
        <div className="settings-page">
            <h1>Settings</h1>
            <p>Manage your account settings and preferences.</p>

            <div className='settings-section following'>
                <h2>Following ({following.length})</h2>
                {following.length === 0 ? (
                    <p className="empty-message">You are not following anyone yet.</p>
                ) : (
                    <div className="following-list">
                        {following.map(user => (
                            <div key={user.id} className="following-item">
                                <div className="user-info">
                                    <img 
                                        src="https://avatar.iran.liara.run/public"
                                        alt={user.email}
                                        className="user-avatar"
                                    />
                                    <span className="username">{user.email}</span>
                                </div>
                                <button 
                                    onClick={() => handleUnfollow(user.id)}
                                    className="unfollow-btn"
                                >
                                    Unfollow
                                </button>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            <div className='settings-section update-info'>
                <h2>Update Information</h2>
                <form onSubmit={handleUpdateInfo} className="update-form">
                    <div className="form-group">
                        <label htmlFor="firstName">First Name</label>
                        <input
                            type="text"
                            id="firstName"
                            value={infoForm.firstName}
                            onChange={(e) => setInfoForm(prev => ({ ...prev, firstName: e.target.value }))}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="lastName">Last Name</label>
                        <input
                            type="text"
                            id="lastName"
                            value={infoForm.lastName}
                            onChange={(e) => setInfoForm(prev => ({ ...prev, lastName: e.target.value }))}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="email">Email</label>
                        <input
                            type="email"
                            id="email"
                            value={infoForm.email}
                            onChange={(e) => setInfoForm(prev => ({ ...prev, email: e.target.value }))}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="aboutMe">About Me</label>
                        <input
                            type="text"
                            id="aboutMe"
                            value={infoForm.aboutMe}
                            onChange={(e) => setInfoForm(prev => ({ ...prev, aboutMe: e.target.value }))}
                        />
                    </div>
                    <button type="submit" className="update-btn">Update Information</button>
                </form>
            </div>

            <div className='settings-section change-password'>
                <h2>Change Password</h2>
                <form onSubmit={handleChangePassword} className="password-form">
                    <div className="form-group">
                        <label htmlFor="currentPassword">Current Password</label>
                        <input
                            type="password"
                            id="currentPassword"
                            value={passwordForm.currentPassword}
                            onChange={(e) => setPasswordForm(prev => ({ ...prev, currentPassword: e.target.value }))}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="newPassword">New Password</label>
                        <input
                            type="password"
                            id="newPassword"
                            value={passwordForm.newPassword}
                            onChange={(e) => setPasswordForm(prev => ({ ...prev, newPassword: e.target.value }))}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="confirmPassword">Confirm New Password</label>
                        <input
                            type="password"
                            id="confirmPassword"
                            value={passwordForm.confirmPassword}
                            onChange={(e) => setPasswordForm(prev => ({ ...prev, confirmPassword: e.target.value }))}
                            required
                        />
                    </div>
                    <button type="submit" className="update-btn">Change Password</button>
                </form>
            </div>
        </div>
    );
}

export default SettingsPage;
