import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import Loader from '../common/Loader';
import * as api from '../../helpers/api';

import './ProfilePage.css';
import type { IUser } from '../../helpers/types';
import { useAuthContext } from '../../helpers/context';

const ProfilePage = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [user, setUser] = useState<IUser | null>(null);

  const  { authUser } = useAuthContext();

  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const data = await api.profile(authUser!.id);
        setUser(data.user);
      } catch (error) { 
        console.error(error);
        navigate('/error');
      } finally {
        setIsLoading(false);
      }
    }
    fetchProfile();
  }, [authUser, navigate])

  if (isLoading) {
    return <Loader />
  }

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
      </div>
    </div>
  );
};

export default ProfilePage;
