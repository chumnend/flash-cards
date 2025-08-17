import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

import Loader from '../common/Loader';
import * as api from '../../helpers/api';
import type { IUser } from '../../helpers/types';
import { useAuthContext } from '../../helpers/context';

import './ProfilePage.css';

const ProfilePage = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [user, setUser] = useState<IUser | null>(null);

  const params = useParams();
  const { authUser } = useAuthContext();

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

  const isUserProfile = authUser?.id === params.userId;

  return (
    <div className="profile-page">
      <h1>Profile</h1>
      <p>Manage your account settings and preferences.</p>
      <div>
        <div>
          <h2>{user?.firstName} {user?.lastName}</h2>
          <p>{user?.details.aboutMe}</p>
        </div>
        <div>
          <p>Following: {user?.following.length}</p>
          <p>Followers: {user?.followers.length}</p>
        </div>
        {isUserProfile && <button>Edit Profile</button>}
      </div>
    </div>
  );
};

export default ProfilePage;
