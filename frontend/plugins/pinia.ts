import {createPinia} from "pinia";
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

export default defineNuxtPlugin(async (nuxtApp) => {
    // @ts-ignore
    nuxtApp.$pinia.use(piniaPluginPersistedstate);
});