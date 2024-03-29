export interface User {
    email: string;
    username: string;
    first_name: string;
    last_name: string;
    token: string;
}
export interface AuthParams {
    email: string;
    password: string;
}