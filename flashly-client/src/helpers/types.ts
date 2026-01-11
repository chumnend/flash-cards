export interface IAuthUser {
    id: string;
    name: string;
    email: string;
    token: string;
};

export interface ICard {
    id: string,
    frontText: string,
    backText: string,
    difficulty: string,
    timesReviewed: number,
    successRate: number,
    deck: string,
    createdAt: Date,
    updatedAt: Date,
}

export interface ICategory {
    id: string,
    name: string,
    createdAt: Date,
    updatedAt: Date,
}

export interface IDeck {
    id: string,
    name: string,
    description: string,
    publishStatus: string,
    categories: Array<string>,
    owner: string,
    rating: number,
    cards: Array<ICard>,
    createdAt: Date,
    updatedAt: Date,
}

export interface IUserDetails {
    id: string,
    userId: string,
    aboutMe: string,
    createdAt: Date,
    updatedAt: Date,
}

export interface IUser {
    id: string,
    firstName: string,
    lastName: string,
    username: string,
    email: string,
    password: string,
    details: IUserDetails,
    following: Array<IUser>,
    followers: Array<IUser>,
    decks: Array<IDeck>,
    createdAt: Date,
    updatedAt: Date,
}

// ====================== USERS ====================================

export interface IRegisterResponse {
    message: string,
    user: {
        id: string,
        firstName: string,
        lastName: string,
        username: string,
        email: string,
    } | null | undefined,
    token: string | null | undefined,
}

export interface ILoginResponse {
    message: string,
    user?: {
        id: string,
        firstName: string,
        lastName: string,
        username: string,
        email: string,
    } | null | undefined,
    token: string | null | undefined,
}

export interface IProfileResponse {
    message: string,
    user: IUser,
}

export interface ISettingsResponse {
    message: string,
    user: IUser,
}

export interface IChangePasswordResponse {
    message: string,
}

export interface IFollowResponse {
    message: string,
}

export interface IUnfollowResponse {
    message: string,
}

// ====================== DECKS ====================================

export interface IExploreResponse {
    message: string,
    decks: Array<IDeck>,
}

export interface IFeedResponse {
    message: string,
    decks: Array<IDeck>,
}

export interface IDecksResponse {
    message: string,
    decks: Array<IDeck>,
}

export interface IDeckResponse {
    message: string,
    deck: IDeck,
}

export interface INewDeckResponse {
    message: string,
    deck: IDeck,
}

export interface IDeleteDeckResponse {
    message: string,
}

//  ====================== CARDS ====================================

export interface INewCardResponse {
    message: string,
    card: ICard,
}

export interface IModifyCardResponse {
    message: string,
    card: ICard,
}

export interface IDeleteCardResponse {
    message: string,
}
