import { defineStore } from 'pinia';
import {User} from '~/models/User';


const useAuth = defineStore('auth-store', function () {
    const router = useRouter();
    // const userData = useCookie<User | undefined>(USER_COOKIE_NAME, {default: () => undefined, path: '/'});

    // async function doLogin(email: string, password: string) {
    //     const {data} = $fetch('/token/login', {
    //         email,
    //         password
    //     });
    //
    //     if (data) {
    //         userData.value = unref(data);
    //     }
    // }

    function doLogout() {
        // userData.value = undefined;
        router.push('/sign-in');
    }


    return {
        // doLogin,
        doLogout,
        // user: computed(() => userData.value?.user),
        // accessToken: computed(() => userData.value?.token.token)
    };
});

export default useAuth;
