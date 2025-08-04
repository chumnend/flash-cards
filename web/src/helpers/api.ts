import { type IRegisterResponse, type ILoginResponse, type IExploreResponse } from './types';

import * as db from '../../testing/jsondb';

export async function register(
    firstName: string,
    lastName: string,
    email: string,
    password: string,
): Promise<IRegisterResponse> {
    try {
        // TODO: Implement actual registration logic

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
        console.error('Register error', error);
        throw error;
    }
}

export async function login(email: string, password: string): Promise<ILoginResponse> {
    // TODO: Implement actual login logic

    try {
        await new Promise(resolve => setTimeout(resolve, 1000));

        // simulate search for user
        const foundUser = db.users.find(user => user.email === email && user.password === password);

        if (!foundUser) {
             throw new Error('User not found');
        }

        return {
            message: 'Login successful',
            user: {
                id: '12345',
                name: `${foundUser.firstName} ${foundUser.lastName.charAt(0)}.`,
                email,
            },
            token: 'randomtokenforencryption',
        }
    } catch (error) {
        console.error('Login Error', error);
        throw error;
    }
}

export async function explore(): Promise<IExploreResponse> {
    // TODO: Implement actual explore logic

    try {
        await new Promise(resolve => setTimeout(resolve, 1000));

        const publicDecks = db.decks.filter(deck => deck.publishStatus === "public");

        // Transform decks with populated categories and cards
        const enrichedDecks = publicDecks.map(deck => {
            const populatedCategories = deck.categories
                .map(categoryId => db.categories.find(category => category.id === categoryId))
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
            message: 'Public decks found',
            decks: enrichedDecks,
        }
    } catch (error) {
        console.error('Error fetching public decks:', error);
        return {
            message: 'Error fetching public decks',
            decks: [],
        }
    }
}
