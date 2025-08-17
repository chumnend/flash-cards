export const users = [
    {
        id: 'agew2153',
        firstName: 'Nicholas',
        lastName: 'Chumney',
        email: 'nicholas.chumney@outlook.com',
        password: 'test123',
        details: 'safv4567',
        following: [],
        followers: ['bvwr4021'],
        decks: ['bsd3s2s', 'agfa0921'],
        createdAt: new Date(100000),
        updatedAt: new Date(100000),
    }, 
    {
        id: 'bvwr4021',
        firstName: 'John',
        lastName: 'Doe',
        email: 'johndoe@gmail.com',
        password: 'jd2025',
        details: 'resf6578',
        following: ['agew2153'],
        followers: [],
        decks: [],
        createdAt: new Date(145600),
        updatedAt: new Date(145600),
    }
]

export const userDetails = [
    {
        id: 'safv4567',
        aboutMe: 'I am Nicholas!',
        createdAt: new Date(100000),
        updatedAt: new Date(100000),
    },
    {
        id: 'resf6578',
        aboutMe: '',
        createdAt: new Date(145600),
        updatedAt: new Date(145600),
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
        id: 'bsd3s2s',
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
        id: 'agfa0921',
        name: 'Math Basics',
        description: 'A deck for basic math problems',
        publishStatus: 'public',
        categories: ['edf342'],
        owner: 'agew2153',
        rating: 4.8,
        cards: ['red123', 'agt520'],
        createdAt: new Date(100005),
        updatedAt: new Date(100005),
    },
    {
        id: 'dech5321',
        name: 'Francais debutant',
        description: '',
        publishStatus: 'public',
        categories: [],
        owner: 'agew2153',
        rating: 0.0,
        cards: [],
        createdAt: new Date(100005),
        updatedAt: new Date(100005),
    },
]

export const cards = [
    {
        id: 'red123',
        frontText: '1 + 1',
        backText: '2',
        difficulty: 'easy',
        timesReviewed: 0,
        successRate: 0,
        deck: 'agfa0921',
        createdAt: new Date(),
        updatedAt: new Date(),
    },
    {
        id: 'agt520',
        frontText: '6 + 8',
        backText: '14',
        difficulty: 'easy',
        timesReviewed: 0,
        successRate: 0,
        deck: 'agfa0921',
        createdAt: new Date(),
        updatedAt: new Date(),
    },
]

export const categories = [
    {
        id: 'edf342',
        name: 'Math',
    }
]
