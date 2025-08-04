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
