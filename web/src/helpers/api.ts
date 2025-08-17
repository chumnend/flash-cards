import { 
    type IExploreResponse, 
    type IRegisterResponse, 
    type ILoginResponse, 
    type IFeedResponse, 
    type IDecksResponse,
    type IDeckResponse,
    type INewDeckResponse,
    type IDeleteDeckResponse,
    type INewCardResponse,
    type IModifyCardResponse,
    type IDeleteCardResponse,
    type IProfileResponse,
    type IUser,
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

export async function deleteDeck(id: string): Promise<IDeleteDeckResponse> {
    try {
        // TODO: Implement actual logic
        await new Promise(resolve => setTimeout(resolve, 1000));

        const deckIndex = db.decks.findIndex(deck => deck.id === id);
        if (deckIndex === -1) {
            throw new Error('Deck not found');
        }

        const deck = db.decks[deckIndex];
        
        // Delete all cards associated with this deck
        const cardIdsToDelete = deck.cards;
        for (let i = db.cards.length - 1; i >= 0; i--) {
            if (cardIdsToDelete.includes(db.cards[i].id)) {
                db.cards.splice(i, 1);
            }
        }

        // Remove deck from users' deck arrays
        db.users.forEach(user => {
            const userDeckIndex = (user.decks as string[]).indexOf(id);
            if (userDeckIndex > -1) {
                (user.decks as string[]).splice(userDeckIndex, 1);
            }
        });

        // Delete the deck itself
        db.decks.splice(deckIndex, 1);

        return {
            message: 'Deck successfully deleted',
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


export async function modifyCard(id: string, frontText: string, backText: string): Promise<IModifyCardResponse> {
    try {
        // TODO: Implement actual logic
        await new Promise(resolve => setTimeout(resolve, 1000));

        const card = db.cards.find(card => card.id === id);
        if (!card) {
            throw new Error('Card not found');
        }

        card.frontText = frontText;
        card.backText = backText;
        card.updatedAt = new Date();

        const parentDeck = db.decks.find(deck => deck.id === card.deck);
        if (parentDeck) {
            parentDeck.updatedAt = new Date();
        }

        return {
            message: 'Card successfully modified',
            card,
        }
    } catch (error) {
        console.error(error);
        throw error; 
    }
}

export async function deleteCard(id: string): Promise<IDeleteCardResponse> {
    try {
        // TODO: Implement actual logic
        await new Promise(resolve => setTimeout(resolve, 1000));

        const cardIndex = db.cards.findIndex(card => card.id === id);
        if (cardIndex === -1) {
            throw new Error('Card not found');
        }

        const card = db.cards[cardIndex];
        const deckId = card.deck;

        // Remove card from the database
        db.cards.splice(cardIndex, 1);

        // Remove card reference from its parent deck
        const parentDeck = db.decks.find(deck => deck.id === deckId);
        if (parentDeck) {
            const cardIdIndex = parentDeck.cards.indexOf(id);
            if (cardIdIndex > -1) {
                parentDeck.cards.splice(cardIdIndex, 1);
            }
            parentDeck.updatedAt = new Date();
        }

        return {
            message: 'Card successfully deleted',
        }
    } catch (error) {
        console.error(error);
        throw error; 
    } 
}

export async function profile(id: string): Promise<IProfileResponse> {
    try {
        // TODO: Implement actual logic
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Find the main user
        const user = db.users.find(u => u.id === id);
        if (!user) {
            throw new Error('User not found');
        }

        // Find user details
        const userDetails = db.userDetails.find(details => details.id === user.details);
        
        // Helper function to create a simplified user object (to avoid circular references)
        const createSimplifiedUser = (userId: string): IUser | null => {
            const u = db.users.find(user => user.id === userId);
            if (!u) return null;

            const uDetails = db.userDetails.find(details => details.id === u.details);
            
            return {
                id: u.id,
                firstName: u.firstName,
                lastName: u.lastName,
                email: u.email,
                password: u.password,
                details: uDetails || {
                    id: u.details,
                    aboutMe: '',
                    createdAt: u.createdAt,
                    updatedAt: u.updatedAt,
                },
                following: [], // Empty to avoid circular references
                followers: [], // Empty to avoid circular references
                decks: [], // Empty to avoid circular references  
                createdAt: u.createdAt,
                updatedAt: u.updatedAt,
            };
        };

        // Populate following list with simplified user objects
        const populatedFollowing = user.following
            .map(followingId => createSimplifiedUser(followingId))
            .filter((u): u is IUser => u !== null);

        // Populate followers list with simplified user objects
        const populatedFollowers = user.followers
            .map(followerId => createSimplifiedUser(followerId))
            .filter((u): u is IUser => u !== null);

        // Populate decks list with full deck objects
        const populatedDecks = (user.decks as string[])
            .map(deckId => {
                const deck = db.decks.find(d => d.id === deckId);
                if (!deck) return null;

                // Enrich deck with categories and cards
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
            })
            .filter(deck => deck !== null);

        // Build the complete user object
        const completeUser: IUser = {
            id: user.id,
            firstName: user.firstName,
            lastName: user.lastName,
            email: user.email,
            password: user.password,
            details: userDetails || {
                id: user.details,
                aboutMe: '',
                createdAt: user.createdAt,
                updatedAt: user.updatedAt,
            },
            following: populatedFollowing,
            followers: populatedFollowers,
            decks: populatedDecks,
            createdAt: user.createdAt,
            updatedAt: user.updatedAt,
        };

        return {
            message: 'Profile successfully retrieved',
            user: completeUser,
        }
    } catch (error) {
        console.error(error);
        throw error; 
    }
}
