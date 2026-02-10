import { useEffect, useState } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';

import Loader from '../Loader';
import DeckList from '../DeckList';
import * as api from '../../helpers/api';
import type { IUser } from '../../helpers/types';
import { useAuthContext } from '../../helpers/context';

import './ProfilePage.css';

const ProfilePage = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [user, setUser] = useState<IUser | null>(null);
  const [isFollowLoading, setIsFollowLoading] = useState(false);
  const [isFollowing, setIsFollowing] = useState(false);

  const params = useParams();
  const navigate = useNavigate();
  const { authUser } = useAuthContext();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        if (!params.userId) {
            throw new Error('User ID is missing');
        }
        const data = await api.profile(params.userId);
        setUser(data.user);

        if (authUser) {
          const isUserFollowing = data.user.followers.some(follower => follower.id === authUser.id);
          setIsFollowing(isUserFollowing);
        }
      } catch (error) { 
        console.error(error);
        navigate('/error');
      } finally {
        setIsLoading(false);
      }
    }
    fetchProfile();
  }, [params.userId, navigate, authUser])

  const handleFollowToggle = async () => {
    if (!authUser || !user) return;
    
    setIsFollowLoading(true);

    try {
      if (isFollowing) {
        await api.unfollow(user.id, authUser.token);
        setIsFollowing(false);
        // Update local list of followerss
        setUser(prev => prev ? {
          ...prev,
          followers: prev.followers.filter(follower => follower.id !== authUser.id)
        } : null);
      } else {
        await api.follow(user.id, authUser.token);
        setIsFollowing(true);
        // Update local list of followers
        const followerUser = {
          id: authUser.id,
          firstName: authUser.name.split(' ')[0],
          lastName: authUser.name.split(' ')[1] || '',
          username: authUser.email, // Using email as username fallback
          email: authUser.email,
          password: '',
          details: { 
            id: '', 
            userId: authUser.id, 
            aboutMe: '', 
            createdAt: new Date(), 
            updatedAt: new Date() 
          },
          following: [],
          followers: [],
          decks: [],
          createdAt: new Date(),
          updatedAt: new Date()
        };
        setUser(prev => prev ? {
          ...prev,
          followers: [...prev.followers, followerUser]
        } : null);
      }
    } catch (error) {
      console.error('Error with follow/unfollow:', error);
    } finally {
      setIsFollowLoading(false);
    }
  };

  if (isLoading) {
    return <Loader />
  }

  const isOwnProfile = authUser?.id === user?.id;
  const fullname = `${user?.firstName} ${user?.lastName}`;
  const publicDecks = user?.decks.filter(deck => deck.publishStatus === 'public') || [];
  const joinDate = new Date(user?.createdAt || '').toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });

  return (
    <div className="profile-page">
      <div className="profile-container">
        <div className="profile-header">
          <img className='profile-avatar' src="https://avatar.iran.liara.run/public" alt={fullname} />
          <div className="profile-info">
            <h1 className="profile-name">{fullname}</h1>
            <p className="profile-email">{user?.email}</p>
            <p className="profile-about">{user?.details.aboutMe || 'No description available'}</p>
            <p className="profile-join-date">Member since: {joinDate}</p>
          </div>
          {!isOwnProfile && authUser && (
            <button 
              className={isFollowing ? 'unfollow-button' : 'follow-button'}
              onClick={handleFollowToggle}
              disabled={isFollowLoading}
            >
              {isFollowLoading ? 'Loading...' : (isFollowing ? 'Unfollow' : 'Follow')}
            </button>
          )}
        </div>

        <div className="profile-stats">
          <div className="stat-item">
            <span className="stat-number">{user?.following.length || 0}</span>
            <span className="stat-label">Following</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">{user?.followers.length || 0}</span>
            <span className="stat-label">Followers</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">{user?.decks.length || 0}</span>
            <span className="stat-label">Total Decks</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">{publicDecks.length}</span>
            <span className="stat-label">Public Decks</span>
          </div>
        </div>

        <div className="profile-connections">
          <div className="connections-section">
            <h3>Following ({user?.following.length || 0})</h3>
            {user?.following && user.following.length > 0 ? (
              <div className="users-list">
                {user.following.map((followingUser) => (
                  <Link key={followingUser.id} to={`/profile/${followingUser.id}`} className="user-card">
                    <img 
                      className="user-avatar" 
                      src="https://avatar.iran.liara.run/public" 
                      alt={`${followingUser.firstName} ${followingUser.lastName}`} 
                    />
                    <div className="user-info">
                      <span className="user-name">{followingUser.firstName} {followingUser.lastName}</span>
                      <span className="user-email">{followingUser.email}</span>
                    </div>
                  </Link>
                ))}
              </div>
            ) : (
              <p className="no-connections">Not following anyone yet.</p>
            )}
          </div>

          <div className="connections-section">
            <h3>Followers ({user?.followers.length || 0})</h3>
            {user?.followers && user.followers.length > 0 ? (
              <div className="users-list">
                {user.followers.map((follower) => (
                  <Link key={follower.id} to={`/profile/${follower.id}`} className="user-card">
                    <img 
                      className="user-avatar" 
                      src="https://avatar.iran.liara.run/public" 
                      alt={`${follower.firstName} ${follower.lastName}`} 
                    />
                    <div className="user-info">
                      <span className="user-name">{follower.firstName} {follower.lastName}</span>
                      <span className="user-email">{follower.email}</span>
                    </div>
                  </Link>
                ))}
              </div>
            ) : (
              <p className="no-connections">No followers yet.</p>
            )}
          </div>
        </div>

        <div className="profile-decks-section">
          <h2>Public Decks ({publicDecks.length})</h2>
          {publicDecks.length > 0 ? (
            <DeckList decks={publicDecks} />
          ) : (
            <div className="no-decks">
              <p>This user doesn't have any public decks yet.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
