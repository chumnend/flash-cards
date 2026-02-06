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
    user: {
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
    userDetails: IUserDetails,
    decks: IDeck[],
    statistics: {
        followingCount: number,
        followersCount: number,
        decksCount: number
    }
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

export interface IGetFollowers {
    message: string,
    followers: IUser[],
    count: number
}

export interface IGetFollowing {
    message: string,
    followers: IUser[],
    count: number
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

export interface IUpdateDeckResponse {
    message: string,
    deck: IDeck,
}

export interface IDeleteDeckResponse {
    message: string,
}

//  ====================== CARDS ====================================

export interface IGetCardsResponse {
    message: string,
    cards: ICard[],
    deck_info: {
        id: string,
        name: string,
        card_count: number
    }
}

export interface IGetCardResponse {
    message: string,
    cards: ICard,
    deck_info: {
        id: string,
        name: string,
        card_count: number
    }
}


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
