import * as testDB from '../../testing/testDB';

// TODO: Implement actual registration logic
export async function register(
    firstName: string,
    lastName: string,
    email: string,
    password: string,
) {
    try {
        // Simulate validation - check if email already exists
        const existingUser = testDB.users.find(user => user.email === email);
        if (existingUser) {
            throw new Error('A user with this username already exists');
        }
        
        // Simulate basic validation
        if (!firstName.trim() || !lastName.trim() || !email.trim() || !password.trim()) {
            throw new Error('All fields are required');
        }
        
        if (password.length < 6) {
            throw new Error('The password contains less than 6 characters');
        }
        
        // simulate response time for testing
        await new Promise(resolve => setTimeout(resolve, 1000));

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
        console.error('Error with inputs', error);
        throw error;
    }
}

export async function login(email: string, password: string) {
    // TODO: Implement actual login logic
    console.log('Login data:', {
        email,
        password,
    });

    await new Promise(resolve => setTimeout(resolve, 1000));

    const foundUser = testDB.users.find(user => user.email === email && user.password === password);

    if (!foundUser) {
        return {
            message: 'Login failed',
            user: null,
            token: null,
        }
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
}

export async function explore() {
    // TODO: Implement actual explore logic
    const decks = testDB.decks.filter(deck => deck.publishStatus === "public");

    await new Promise(resolve => setTimeout(resolve, 1000));
    
    return {
        message: 'Public decks found',
        decks,
    }
}
