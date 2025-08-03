import * as testDB from '../../testing/testDB';

export async function register(
    firstName: string,
    lastName: string,
    email: string,
    password: string,
) {
      // TODO: Implement actual registration logic
      console.log('Registration data:', {
        firstName,
        lastName,
        email,
        password,
      });
      
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
