import type { 
    ILoginResponse, 
    IProfileResponse, 
    IRegisterResponse,
    IExploreResponse,
    IFeedResponse,
    IDecksResponse,
    IDeckResponse,
    INewDeckResponse,
    IUpdateDeckResponse,
    IDeleteDeckResponse,
    INewCardResponse,
    IModifyCardResponse,
    IDeleteCardResponse,
    IGetCardsResponse,
    IGetCardResponse,
    ISettingsResponse,
    IChangePasswordResponse,
    IFollowResponse,
    IUnfollowResponse,
    IGetFollowers,
    IGetFollowing
} from "./types";

const API_BASE_URL = '/api';

export async function hello(): Promise<{ message: string}> {
    const response = await fetch(`${API_BASE_URL}/`);
    if (!response.ok) {
        throw new Error('Something went wrong!')
    }

    return response.json();
}

export async function register(
    firstName: string,
    lastName: string,
    username: string,
    email: string,
    password: string,
): Promise<IRegisterResponse> {
    const response = await fetch(`${API_BASE_URL}/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            firstName,
            lastName,
            username,
            email,
            password
        })
    });
    if (!response.ok) {
        throw new Error('Registration failed');
    }

    const data = await response.json();
    return {
        message: data.message,
        user: data.user ? {
            id: data.user.id,
            firstName: data.user.firstName,
            lastName: data.user.lastName,
            username: data.user.username,
            email: data.user.email,
        } : null,
        token: data.token || null,
    }
}


export async function login(
    email: string,
    password: string,
): Promise<ILoginResponse> {
    const response = await fetch(`${API_BASE_URL}/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email,
            password
        })
    });
    if (!response.ok) {
        throw new Error('Login failed');
    }

    const data = await response.json();
    return {
        message: data.message,
        user: data.user ? {
            id: data.user.id,
            firstName: data.user.firstName,
            lastName: data.user.lastName,
            username: data.user.username,
            email: data.user.email,
        } : null,
        token: data.token || null,
    }
}


export async function profile(
    id: string
): Promise<IProfileResponse> {
    const response = await fetch(`${API_BASE_URL}/users/${id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    if (!response.ok) {
        throw new Error('Login failed');
    }

    const data = await response.json();
    return {
        message: data.message,
        user: data.user,
        userDetails: data.userDetails,
        decks: data.decks,
        statistics: data.statistics,
    }
}

export async function settings(
    id: string,
    token: string,
    firstName?: string,
    lastName?: string,
    email?: string,
    aboutMe?: string,
): Promise<ISettingsResponse> {
    const response = await fetch(`${API_BASE_URL}/users/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
            firstName,
            lastName,
            email,
            aboutMe
        })
    });
    if (!response.ok) {
        throw new Error('Failed to update user settings');
    }

    const data = await response.json();
    return {
        message: data.message,
        user: data.user,
    }
}

export async function changePassword(newPassword: string, token: string): Promise<IChangePasswordResponse> {
    const response = await fetch(`${API_BASE_URL}/change_password`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
            newPassword
        })
    });
    if (!response.ok) {
        throw new Error('Failed to change password');
    }

    const data = await response.json();
    return {
        message: data.message,
    }
}

export async function follow(userToFollowId: string, token: string): Promise<IFollowResponse> {
    const response = await fetch(`${API_BASE_URL}/users/${userToFollowId}/follow`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        }
    });
    if (!response.ok) {
        throw new Error('Failed to follow user');
    }

    const data = await response.json();
    return {
        message: data.message,
    }
}

export async function unfollow(userToUnfollowId: string, token: string): Promise<IUnfollowResponse> {
    const response = await fetch(`${API_BASE_URL}/users/${userToUnfollowId}/unfollow`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        }
    });
    if (!response.ok) {
        throw new Error('Failed to unfollow user');
    }

    const data = await response.json();
    return {
        message: data.message,
    }
}

export async function getFollowers(userId: string): Promise<IGetFollowers> {
    const response = await fetch(`${API_BASE_URL}/users/${userId}/followers`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    if (!response.ok) {
        throw new Error('Failed to fetch followers');
    }

    const data = await response.json();
    return {
        message: data.message,
        followers: data.followers,
        count: data.count,
    }
}

export async function getFollowing(userId: string): Promise<IGetFollowing> {
    const response = await fetch(`${API_BASE_URL}/users/${userId}/following`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    if (!response.ok) {
        throw new Error('Failed to fetch following');
    }

    const data = await response.json();
    return {
        message: data.message,
        followers: data.following,
        count: data.count,
    }
}

export async function explore(): Promise<IExploreResponse> {
    const response = await fetch(`${API_BASE_URL}/decks/explore`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    if (!response.ok) {
        throw new Error('Failed to fetch explore decks');
    }

    const data = await response.json();
    return {
        message: data.message,
        decks: data.decks,
    }
}

export async function feed(token: string): Promise<IFeedResponse> {
    const response = await fetch(`${API_BASE_URL}/decks/feed`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        }
    });
    if (!response.ok) {
        throw new Error('Failed to fetch feed');
    }

    const data = await response.json();
    return {
        message: data.message,
        decks: data.decks,
    }
}

export async function decks(token: string): Promise<IDecksResponse> {
    const response = await fetch(`${API_BASE_URL}/decks`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        }
    });
    if (!response.ok) {
        throw new Error('Failed to fetch user decks');
    }

    const data = await response.json();
    return {
        message: data.message,
        decks: data.decks,
    }
}

export async function deck(id: string): Promise<IDeckResponse> {
    const response = await fetch(`${API_BASE_URL}/decks/${id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    if (!response.ok) {
        throw new Error('Failed to fetch deck');
    }

    const data = await response.json();
    return {
        message: data.message,
        deck: data.deck,
    }
}

export async function newDeck(name: string, description: string, token: string): Promise<INewDeckResponse> {
    const response = await fetch(`${API_BASE_URL}/decks`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
            name,
            description
        })
    });
    if (!response.ok) {
        throw new Error('Failed to create deck');
    }

    const data = await response.json();
    return {
        message: data.message,
        deck: data.deck,
    }
}

export async function updateDeck(id: string, name: string, description: string, publishStatus: string, token: string): Promise<IUpdateDeckResponse> {
    const response = await fetch(`${API_BASE_URL}/decks/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
            name,
            description,
            publishStatus
        })
    });
    if (!response.ok) {
        throw new Error('Failed to update deck');
    }

    const data = await response.json();
    return {
        message: data.message,
        deck: data.deck,
    }
}

export async function deleteDeck(id: string, token: string): Promise<IDeleteDeckResponse> {
    const response = await fetch(`${API_BASE_URL}/decks/${id}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        }
    });
    if (!response.ok) {
        throw new Error('Failed to delete deck');
    }

    const data = await response.json();
    return {
        message: data.message,
    }
}

export async function getCards(deckId: string): Promise<IGetCardsResponse> {
    const response = await fetch(`${API_BASE_URL}/decks/${deckId}/cards`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    if (!response.ok) {
        throw new Error('Failed to fetch cards');
    }

    const data = await response.json();
    return {
        message: data.message,
        cards: data.cards,
        deck_info: data.deck_info,
    }
}

export async function getCard(deckId: string, cardId: string): Promise<IGetCardResponse> {
    const response = await fetch(`${API_BASE_URL}/decks/${deckId}/cards/${cardId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    if (!response.ok) {
        throw new Error('Failed to fetch card');
    }

    const data = await response.json();
    return {
        message: data.message,
        cards: data.card,
        deck_info: data.deck_info,
    }
}

export async function newCard(frontText: string, backText: string, deckId: string, token: string): Promise<INewCardResponse> {
    const response = await fetch(`${API_BASE_URL}/decks/${deckId}/cards`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
            frontText,
            backText
        })
    });
    if (!response.ok) {
        throw new Error('Failed to create card');
    }

    const data = await response.json();
    return {
        message: data.message,
        card: data.card,
    }
}

export async function modifyCard(deckId: string, cardId: string, frontText: string, backText: string, token: string): Promise<IModifyCardResponse> {
    const response = await fetch(`${API_BASE_URL}/decks/${deckId}/cards/${cardId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
            frontText,
            backText
        })
    });
    if (!response.ok) {
        throw new Error('Failed to update card');
    }

    const data = await response.json();
    return {
        message: data.message,
        card: data.card,
    }
}

export async function deleteCard(deckId: string, cardId: string, token: string): Promise<IDeleteCardResponse> {
    const response = await fetch(`${API_BASE_URL}/decks/${deckId}/cards/${cardId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        }
    });
    if (!response.ok) {
        throw new Error('Failed to delete card');
    }

    const data = await response.json();
    return {
        message: data.message,
    }
}
