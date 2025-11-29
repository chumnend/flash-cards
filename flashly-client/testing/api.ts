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
    type ISettingsResponse,
    type IFollowResponse,
    type IUnfollowResponse,
    type IUser,
    type IChangePasswordResponse,
} from '../src/helpers/types';

import * as db from './jsondb';

export async function register(
    firstName: string,
    lastName: string,
    email: string,
    password: string,
): Promise<IRegisterResponse> {
    try {
        await new Promise(resolve => setTimeout(resolve, 1000));

        // check if email already exists
        const existingUser = db.users.find(user => user.email === email);
        if (existingUser) {
            throw new Error('A user with this username already exists');
        }
        
        // validate the all required fields were provided
        if (!firstName.trim() || !lastName.trim() || !email.trim() || !password.trim()) {
            throw new Error('All fields are required');
        }
        
        // validate the password has the correct format
        if (password.length < 6) {
            throw new Error('The password contains less than 6 characters');
        }

        // generate unique user ids
        const userId = Math.random().toString(36).substring(2, 10);
        const userDetailsId = Math.random().toString(36).substring(2, 10);
        
        // create user details entry
        const newUserDetails = {
            id: userDetailsId,
            aboutMe: '',
            createdAt: new Date(),
            updatedAt: new Date(),
        };

        // create new user
        const newUser = {
            id: userId,
            firstName,
            lastName,
            email,
            password,
            details: userDetailsId,
            following: [],
            followers: [],
            decks: [],
            createdAt: new Date(),
            updatedAt: new Date(),
        };

        // add to database
        db.userDetails.push(newUserDetails);
        db.users.push(newUser);

        return {
            message: 'Registration successful',
            user: {
                id: userId,
                name: `${firstName} ${lastName.charAt(0)}.`,
                email,
            },
            token: userId,
        }
    } catch (error) {
        console.error(error);
        throw error;
    }
}

export async function login(email: string, password: string): Promise<ILoginResponse> {
    try {
        await new Promise(resolve => setTimeout(resolve, 1000));

        // check if user exists and compare passwords
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
        await new Promise(resolve => setTimeout(resolve, 1000));

        // fetch all public decks
        const publicDecks = db.decks.filter(deck => deck.publishStatus === "public");

        // hydrate the decks with populated categories and cards
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
        await new Promise(resolve => setTimeout(resolve, 1000));

        // check if token was provided
        if (!token || typeof token !== 'string') {
            throw new Error('Invalid token provided');
        }

        // check if user exists
        const currentUser = db.users.find(user => user.id === token);
        if (!currentUser) {
            throw new Error('User not found');
        }

        // get followeds users decks
        const userFollowing = currentUser.following as string[];
        const followingDecks = db.decks.filter(deck => 
            deck.owner !== currentUser.id &&
            userFollowing.includes(deck.owner) && 
            deck.publishStatus !== 'private'
        );

        // hydate the following decks with categories and cards
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

        // sort decks by update time
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
        await new Promise(resolve => setTimeout(resolve, 1000));

        // check if token was provided
        if (!token || typeof token !== 'string') {
            throw new Error('Invalid token provided');
        }

        // check if user exists
        const currentUser = db.users.find(user => user.id === token);
        if (!currentUser) {
            throw new Error('User not found');
        }

        // get the current user's decks
        const userDecks = db.decks.filter(deck => deck.owner === currentUser.id);

        // hydrate the user's decks with categories and cards
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

        // sort decks by update time
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
        await new Promise(resolve => setTimeout(resolve, 1000));

        // check if deck exists
        const deck = db.decks.find(deck => deck.id === id);
        if (!deck) {
            throw new Error('Deck not found');
        }

        // hydrate the deck with categories and cards
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
        await new Promise(resolve => setTimeout(resolve, 1000));

        // create new deck
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

        // append deck to db
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
        await new Promise(resolve => setTimeout(resolve, 1000));

        // check if deck exists
        const deckIndex = db.decks.findIndex(deck => deck.id === id);
        if (deckIndex === -1) {
            throw new Error('Deck not found');
        }

        // retrieve the deck to delete
        const deck = db.decks[deckIndex];
        
        // delete all cards associated with this deck
        const cardIdsToDelete = deck.cards;
        for (let i = db.cards.length - 1; i >= 0; i--) {
            if (cardIdsToDelete.includes(db.cards[i].id)) {
                db.cards.splice(i, 1);
            }
        }

        // remove deck from users' deck arrays
        db.users.forEach(user => {
            const userDeckIndex = (user.decks as string[]).indexOf(id);
            if (userDeckIndex > -1) {
                (user.decks as string[]).splice(userDeckIndex, 1);
            }
        });

        // delete the deck itself
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
        await new Promise(resolve => setTimeout(resolve, 1000));

        // check if deck exists
        const deck = db.decks.find(d => d.id === deckId);
        if (!deck) {
            throw new Error('Deck not found');
        }

        // create new card
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

        // add card to db
        db.cards.push(newCard);

        // add card to the associated deck
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
        await new Promise(resolve => setTimeout(resolve, 1000));

        // check if card exists
        const card = db.cards.find(card => card.id === id);
        if (!card) {
            throw new Error('Card not found');
        }

        // update the card
        card.frontText = frontText;
        card.backText = backText;
        card.updatedAt = new Date();

        // update the associated deck's update time
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
        await new Promise(resolve => setTimeout(resolve, 1000));

        // check if card exists
        const cardIndex = db.cards.findIndex(card => card.id === id);
        if (cardIndex === -1) {
            throw new Error('Card not found');
        }

        // retrive the card and the parent deck id
        const card = db.cards[cardIndex];
        const deckId = card.deck;

        // remove card from the database
        db.cards.splice(cardIndex, 1);

        // remove card reference from its parent deck
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
        await new Promise(resolve => setTimeout(resolve, 1000));

        // find the main user
        const user = db.users.find(u => u.id === id);
        if (!user) {
            throw new Error('User not found');
        }

        // find user details
        const userDetails = db.userDetails.find(details => details.id === user.details);
        
        // helper function to create a simplified user object (to avoid circular references)
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

        // populate following list with simplified user objects
        const populatedFollowing = user.following
            .map(followingId => createSimplifiedUser(followingId))
            .filter((u): u is IUser => u !== null);

        // populate followers list with simplified user objects
        const populatedFollowers = user.followers
            .map(followerId => createSimplifiedUser(followerId))
            .filter((u): u is IUser => u !== null);

        // populate decks list with full deck objects
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

        // build the complete user object
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

export async function settings(
    id: string,
    firstName?: string,
    lastName?: string,
    email?: string,
    aboutMe?: string,
): Promise<ISettingsResponse> {
    try {
        await new Promise(resolve => setTimeout(resolve, 1000));

        // check if user exists
        const user = db.users.find(u => u.id === id);
        if (!user) {
            throw new Error('User not found');
        }

        // find user details
        const userDetails = db.userDetails.find(details => details.id === user.details);
        if (!userDetails) {
            throw new Error('User details not found');
        }

        // validate email uniqueness if email is being updated
        if (email && email !== user.email) {
            const existingUserWithEmail = db.users.find(u => u.email === email && u.id !== id);
            if (existingUserWithEmail) {
                throw new Error('A user with this email already exists');
            }
        }

        // validate required fields
        const updatedFirstName = firstName !== undefined ? firstName.trim() : user.firstName;
        const updatedLastName = lastName !== undefined ? lastName.trim() : user.lastName;
        const updatedEmail = email !== undefined ? email.trim() : user.email;
        const updatedAboutMe = aboutMe !== undefined ? aboutMe.trim() : userDetails.aboutMe;
        if (!updatedFirstName || !updatedLastName || !updatedEmail) {
            throw new Error('First name, last name, and email are required');
        }

         // update user information
        if (firstName !== undefined) user.firstName = updatedFirstName;
        if (lastName !== undefined) user.lastName = updatedLastName;
        if (email !== undefined) user.email = updatedEmail;
        user.updatedAt = new Date();

        // update user details
        if (aboutMe !== undefined) userDetails.aboutMe = updatedAboutMe;
        userDetails.updatedAt = new Date();

         // helper function to create a simplified user object (to avoid circular references)
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

        // populate following list with simplified user objects
        const populatedFollowing = user.following
            .map(followingId => createSimplifiedUser(followingId))
            .filter((u): u is IUser => u !== null);

        // populate followers list with simplified user objects
        const populatedFollowers = user.followers
            .map(followerId => createSimplifiedUser(followerId))
            .filter((u): u is IUser => u !== null);

        // populate decks list with full deck objects
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

        // build the complete updated user object
        const completeUser: IUser = {
            id: user.id,
            firstName: user.firstName,
            lastName: user.lastName,
            email: user.email,
            password: user.password,
            details: userDetails,
            following: populatedFollowing,
            followers: populatedFollowers,
            decks: populatedDecks,
            createdAt: user.createdAt,
            updatedAt: user.updatedAt,
        };

        return {
            message: 'Settings updated successfully',
            user: completeUser,
        };
    } catch (error) {
        console.error(error);
        throw error; 
    }
}

export async function changePassword(id: string, newPassword: string): Promise<IChangePasswordResponse> {
    try {
        await new Promise(resolve => setTimeout(resolve, 1000));

        // validate inputs
        if (!id || !newPassword) {
            throw new Error('All fields are required');
        }

        // validate new password format
        if (newPassword.length < 6) {
            throw new Error('The password must contain at least 6 characters');
        }

        // check if current user exists
        const currentUser = db.users.find(user => user.id === id);
        if (!currentUser) {
            throw new Error('User not found');
        }

        // check if new password is different from current password
        if (currentUser.password === newPassword) {
            throw new Error('New password must be different from current password');
        }

        // update password
        currentUser.password = newPassword;
        currentUser.updatedAt = new Date();

        return {
            message: 'Password changed successfully',
        };
    } catch (error) {
        console.error(error);
        throw error;
    }
}

export async function follow(currentUserId: string, userToFollowId: string): Promise<IFollowResponse> {
    try {
        await new Promise(resolve => setTimeout(resolve, 1000));

        // validate inputs
        if (!currentUserId || !userToFollowId) {
            throw new Error('Both user IDs are required');
        }

        if (currentUserId === userToFollowId) {
            throw new Error('You cannot follow yourself');
        }

        // check if current user exists
        const currentUser = db.users.find(user => user.id === currentUserId);
        if (!currentUser) {
            throw new Error('Current user not found');
        }

        // check if user to follow exists
        const userToFollow = db.users.find(user => user.id === userToFollowId);
        if (!userToFollow) {
            throw new Error('User to follow not found');
        }

        // check if already following
        const currentUserFollowing = currentUser.following as string[];
        if (currentUserFollowing.includes(userToFollowId)) {
            throw new Error('You are already following this user');
        }

        // add userToFollowId to current user's following list
        (currentUser.following as string[]).push(userToFollowId);
        currentUser.updatedAt = new Date();

        // add currentUserId to the other user's followers list
        (userToFollow.followers as string[]).push(currentUserId);
        userToFollow.updatedAt = new Date();

        return {
            message: 'Successfully followed user',
        };
    } catch (error) {
        console.error(error);
        throw error; 
    }
}

export async function unfollow(currentUserId: string, userToUnfollowId: string): Promise<IUnfollowResponse> {
    try {
        await new Promise(resolve => setTimeout(resolve, 1000));

        // validate inputs
        if (!currentUserId || !userToUnfollowId) {
            throw new Error('Both user IDs are required');
        }

        if (currentUserId === userToUnfollowId) {
            throw new Error('You cannot unfollow yourself');
        }

        // check if current user exists
        const currentUser = db.users.find(user => user.id === currentUserId);
        if (!currentUser) {
            throw new Error('Current user not found');
        }

        // check if user to unfollow exists
        const userToUnfollow = db.users.find(user => user.id === userToUnfollowId);
        if (!userToUnfollow) {
            throw new Error('User to unfollow not found');
        }

        // check if currently following
        const currentUserFollowing = currentUser.following as string[];
        const followingIndex = currentUserFollowing.indexOf(userToUnfollowId);
        if (followingIndex === -1) {
            throw new Error('You are not following this user');
        }

        // remove userToUnfollowId from current user's following list
        (currentUser.following as string[]).splice(followingIndex, 1);
        currentUser.updatedAt = new Date();

        // remove currentUserId from the other user's followers list
        const userToUnfollowFollowers = userToUnfollow.followers as string[];
        const followerIndex = userToUnfollowFollowers.indexOf(currentUserId);
        if (followerIndex > -1) {
            (userToUnfollow.followers as string[]).splice(followerIndex, 1);
            userToUnfollow.updatedAt = new Date();
        }

        return {
            message: 'Successfully unfollowed user',
        };
    } catch (error) {
        console.error(error);
        throw error; 
    }
}
