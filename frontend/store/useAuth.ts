import { defineStore } from 'pinia';
import {User, AuthParams} from '~/models/User';


const useAuth = defineStore('auth',  {
    state: () => ({
                      user: null as User | null,
        token: null as string | null,
        isLoading: true
                  }),
    actions: {
        async login({email, password}: AuthParams) {
            const {data} = await useMyFetch('token/login', {
                body: {
                    email: email,
                    password: password
                },
                method: 'POST'
            });

            if (data && data.auth_token) {
                this.token = data.value.auth_token;
            }
        },
        async me() {
            const {data} = await useMyFetch('users/me');

            if (data) {
                this.user = data.value;
            }
        }
    },
    persist: true
});

export default useAuth;
