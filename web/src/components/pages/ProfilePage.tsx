import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

import Loader from '../common/Loader';
import * as api from '../../helpers/api';
import type { IUser } from '../../helpers/types';

import './ProfilePage.css';

const ProfilePage = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [user, setUser] = useState<IUser | null>(null);

  const params = useParams();

  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        if (!params.userId) {
            throw new Error('User ID is missing');
        }
        const data = await api.profile(params.userId);
        setUser(data.user);
      } catch (error) { 
        console.error(error);
        navigate('/error');
      } finally {
        setIsLoading(false);
      }
    }
    fetchProfile();
  }, [params.userId, navigate])

  if (isLoading) {
    return <Loader />
  }

  const fullname = `${user?.firstName} ${user?.lastName}`;

  return (
    <div className="profile-page">
      <h1>Profile</h1>
      <p>Manage your account settings and preferences.</p>

      <div className="profile-header">
        <img className='profile-avatar' src="https://avatar.iran.liara.run/public" alt={fullname} />
        <h2>{fullname}</h2>
        <p>{user?.details.aboutMe}</p>
      </div>

      <div className='follow-list'>
        <div className='following'>
          <p>Following: {user?.following.length}</p>
        </div>
        <div className='followers'>
          <p>Followers: {user?.followers.length}</p>
        </div>
      </div>

      <div className='decks'>
        Decks go here
      </div>
    </div>
  );
};

export default ProfilePage;
