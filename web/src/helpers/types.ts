export interface IAuthUser {
    id: string;
    name: string;
    email: string;
    token: string;
};

export interface IRegisterResponse {
    message: string,
    user: {
        id: string,
        name: string,
        email: string,
    } | null | undefined,
    token: string | null | undefined,
}

export interface ILoginResponse {
    message: string,
    user?: {
        id: string,
        name: string,
        email: string,
    } | null | undefined,
    token: string | null | undefined,
}

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
