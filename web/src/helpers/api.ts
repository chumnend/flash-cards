import { 
    type IExploreResponse, 
    type IRegisterResponse, 
    type ILoginResponse, 
    type IFeedResponse, 
    type IDecksResponse,
    type IDeckResponse,
    type INewDeckResponse,
    type INewCardResponse,
} from './types';

import * as db from '../../testing/jsondb';

export async function register(
    firstName: string,
    lastName: string,
    email: string,
    password: string,
): Promise<IRegisterResponse> {
    try {
        // TODO: Implement actual logic
        await new Promise(resolve => setTimeout(resolve, 1000));

        // simulate validation - check if email already exists
        const existingUser = db.users.find(user => user.email === email);
        if (existingUser) {
            throw new Error('A user with this username already exists');
        }
        
        // simulate basic validation
        if (!firstName.trim() || !lastName.trim() || !email.trim() || !password.trim()) {
            throw new Error('All fields are required');
        }
        
        if (password.length < 6) {
            throw new Error('The password contains less than 6 characters');
        }

        return {
            message: 'Registration successful',
            user: {
                id: '12345',
                name: `${firstName} ${lastName.charAt(0)}.`,
                email,
            },
            token: 'randomtokenforencryption',
        }
    } catch (error) {
        console.error(error);
        throw error;
    }
}

export async function login(email: string, password: string): Promise<ILoginResponse> {
    try {
        // TODO: Implement actual logic  
        await new Promise(resolve => setTimeout(resolve, 1000));

        // simulate search for user
        const foundUser = db.users.find(user => user.email === email && user.password === password);

        if (!foundUser) {
             throw new Error('User not found');
        }

        return {
            message: 'Login successful',
            user: {
                id: foundUser.id,
                name: `${foundUser.firstName} ${foundUser.lastName.charAt(0)}.`,
                email,
            },
            token: `${foundUser.id}`,
        }
    } catch (error) {
        console.error(error);
        throw error;
    }
}

export async function explore(): Promise<IExploreResponse> {
    try {
        // TODO: Implement actual logic
        await new Promise(resolve => setTimeout(resolve, 1000));

        const publicDecks = db.decks.filter(deck => deck.publishStatus === "public");

        // Transform decks with populated categories and cards
        const enrichedDecks = publicDecks.map(deck => {
            const populatedCategories = deck.categories
                .map(categoryId => db.categories.find(category => category.id === categoryId)?.name)
                .filter(category => category !== undefined);

            const populatedCards = deck.cards
                .map(cardId => db.cards.find(card => card.id === cardId))
                .filter(card => card !== undefined);

            return {
                ...deck,
                categories: populatedCategories,
                cards: populatedCards
            };
        });

        return {
            message: enrichedDecks.length > 0 ? 'Explore loaded successfully' : 'No decks found for the explore page',
            decks: enrichedDecks,
        }
    } catch (error) {
        console.error(error);
        throw error;
    }
}

export async function feed(token: string): Promise<IFeedResponse> {
    try {
        // TODO: Implement actual logic
        await new Promise(resolve => setTimeout(resolve, 1000));

        if (!token || typeof token !== 'string') {
            throw new Error('Invalid token provided');
        }

        const currentUser = db.users.find(user => user.id === token);
        if (!currentUser) {
            throw new Error('User not found');
        }
        const userFollowing = currentUser.following as string[];
        const followingDecks = db.decks.filter(deck => 
            deck.owner !== currentUser.id &&
            userFollowing.includes(deck.owner) && 
            deck.publishStatus !== 'private'
        );

        const enrichedDecks = followingDecks.map(deck => {
            const populatedCategories = deck.categories
                .map(categoryId => db.categories.find(category => category.id === categoryId)?.name)
                .filter(category => category !== undefined);

            const populatedCards = deck.cards
                .map(cardId => db.cards.find(card => card.id === cardId))
                .filter(card => card !== undefined);

            return {
                ...deck,
                categories: populatedCategories,
                cards: populatedCards
            };
        });

        enrichedDecks.sort((a, b) => 
            new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime()
        );

        return {
            message: enrichedDecks.length > 0 ? 'Feed loaded successfully' : 'No decks found for your feed',
            decks: enrichedDecks,
        };
    } catch (error) {
        console.error(error);
        throw error;
    }
}

export async function decks(token: string): Promise<IDecksResponse> {
    try {
        // TODO: Implement actual logic
        await new Promise(resolve => setTimeout(resolve, 1000));

        if (!token || typeof token !== 'string') {
            throw new Error('Invalid token provided');
        }

        const currentUser = db.users.find(user => user.id === token);
        if (!currentUser) {
            throw new Error('User not found');
        }

        const userDecks = db.decks.filter(deck => deck.owner === currentUser.id);

        const enrichedDecks = userDecks.map(deck => {
            const populatedCategories = deck.categories
                .map(categoryId => db.categories.find(category => category.id === categoryId)?.name)
                .filter(category => category !== undefined);

            const populatedCards = deck.cards
                .map(cardId => db.cards.find(card => card.id === cardId))
                .filter(card => card !== undefined);

            return {
                ...deck,
                categories: populatedCategories,
                cards: populatedCards
            };
        });

        enrichedDecks.sort((a, b) => 
            new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime()
        );

        return {
            message: enrichedDecks.length > 0 ? 'Feed loaded successfully' : 'No decks found for your decks',
            decks: enrichedDecks,
        };
    } catch (error) {
        console.error(error);
        throw error; 
    }
}


export async function deck(id: string): Promise<IDeckResponse> {
    try {
        // TODO: Implement actual logic
        await new Promise(resolve => setTimeout(resolve, 1000));

        const deck = db.decks.find(deck => deck.id === id);
        if (!deck) {
            throw new Error('Deck not found');
        }

        const populatedCategories = deck.categories
            .map(categoryId => db.categories.find(category => category.id === categoryId)?.name)
            .filter(category => category !== undefined);

        const populatedCards = deck.cards
                .map(cardId => db.cards.find(card => card.id === cardId))
                .filter(card => card !== undefined);
        
        const enrichedDeck = {
            ...deck,
            categories: populatedCategories,
            cards: populatedCards,
        }

        return {
            message: 'testing',
            deck: enrichedDeck,
        }
    } catch (error) {
        console.error(error);
        throw error; 
    }
}

export async function newDeck(name: string, description: string): Promise<INewDeckResponse> {
    try {
        // TODO: Implement actual logic
        await new Promise(resolve => setTimeout(resolve, 1000));

        const newDeck = {
            id: Math.random().toString(36).substring(2, 10),
            name,
            description,
            publishStatus: 'private',
            categories: [],
            owner: '',
            rating: 0.0,
            cards: [],
            createdAt: new Date(),
            updatedAt: new Date(),
        }

        db.decks.push(newDeck);

        return {
            message: 'Deck successfully created',
            deck: newDeck,
        }
    } catch (error) {
        console.error(error);
        throw error; 
    }
}

export async function newCard(frontText: string, backText: string, deckId: string): Promise<INewCardResponse> {
    try {
        // TODO: Implement actual logic
        await new Promise(resolve => setTimeout(resolve, 1000));

        const deck = db.decks.find(d => d.id === deckId);
        if (!deck) {
            throw new Error('Deck not found');
        }

        const newCard = {
            id: Math.random().toString(36).substring(2, 10),
            frontText,
            backText,
            difficulty: 'easy',
            timesReviewed: 0,
            successRate: 0,
            deck: deckId,
            createdAt: new Date(),
            updatedAt: new Date(),
        }

        db.cards.push(newCard);

        deck.cards.push(newCard.id);
        deck.updatedAt = new Date();

        return {
            message: 'Card successfully created',
            card: newCard,
        }
    } catch (error) {
        console.error(error);
        throw error; 
    }
}
