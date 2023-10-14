import {darkTheme, useOsTheme} from "naive-ui";

import {defineStore} from "pinia";

const osTheme = useOsTheme()
export const useTheme = defineStore('theme', {
    state: () => {
        return {themeType: osTheme}
    },
    actions: {
        doToggleTheme(){
            this.themeType = this.themeType === 'dark' ? 'light' : 'dark';
        }
    },
    getters: {
        theme: state => state.themeType
    }
})

// export default {useTheme};
