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
        name: firstName + ' ' + lastName.charAt(0) + '.',
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
        return null;
    }

    return {
        name: foundUser.firstName + ' ' + foundUser.lastName + '.',
        token: 'randomtokenforencryption',
    };
}

export async function explore() {
    // TODO: Implement actual explore logic
    const decks = testDB.decks.filter(deck => deck.publishStatus === "public");

    await new Promise(resolve => setTimeout(resolve, 1000));
    
    return decks;
}
