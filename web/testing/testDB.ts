export const users = [
    {
        ID: 'agew2153',
        firstName: 'Nicholas',
        lastName: 'Chumney',
        email: 'nicholas.chumney@outlook.com',
        password: 'test123',
        details: 'safv4567',
        decks: ['bsd3s2s', 'agfa0921'],
        createdAt: new Date(100000),
    }, 
    {
        ID: 'bvwr4021',
        firstName: 'John',
        lastName: 'Doe',
        email: 'johndoe@gmail.com',
        password: 'jd2025',
        details: 'resf6578',
        followers: [],
        decks: [],
        createdAt: new Date(145600),
    }
]

export const userDetails = [
    {
        ID: 'safv4567',
        aboutMe: 'I am Nicholas!',
        createdAt: new Date(100000),
    },
    {
        ID: 'resf6578',
        aboutMe: '',
        createdAt: new Date(145600),
    }
]

export const followers = [
    {
        followerId: 'bvwr4021',
        followingId: 'agew2153',
    }
]

export const decks = [
    {
        ID: 'bsd3s2s',
        name: 'Test Deck',
        description: 'A deck in progress',
        publishStatus: 'private',
        categories: [],
        owner: 'agew2153',
        rating: 0.0,
        cards: [],
        createdAt: new Date(100005),
        updatedAt: new Date(100005),
    },
        {
        ID: 'agfa0921',
        name: 'Math Basics',
        description: 'A deck for basic math problems',
        publishStatus: 'public',
        categories: ['edf342'],
        owner: 'agew2153',
        rating: 4.8,
        cards: ['red123'],
        createdAt: new Date(100005),
        updatedAt: new Date(100005),
    },
]

export const cards = [
    {
        ID: 'red123',
        frontText: '1 + 1',
        backText: '2',
        difficulty: 'easy',
        timesReviewed: 0,
        successRate: 0,
        deck: 'bsd3s2s',
        createdAt: new Date(),
        updatedAt: new Date(),
    }
]

export const categories = [
    {
        ID: 'edf342',
        name: 'Math',
    }
]
