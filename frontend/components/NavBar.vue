<template>
        <NMenu
            :options="menuOptions" mode="horizontal"
            @update:value="clickMenuItem"
        />
</template>

<script lang="ts">
import type {MenuOption, MenuDividerOption, MenuGroupOption} from 'naive-ui';
import {NH2, NMenu, NInput} from 'naive-ui';
import {NuxtLink} from "#components";
import {h} from "vue";
import useAuth from "~/store/useAuth";
type MenuOptions = (MenuOption | MenuDividerOption | MenuGroupOption)[];

export default defineComponent({
    components: {
        NH2,
        NMenu,
        NInput
    },
  props: {
      location: {
        type: String,
        default: 'left'
      }
  },

    async setup(props, { emit }) {
      const currentRoute = useRoute();
      const router = useRouter();
      const selectedKeys = ref<string>(currentRoute.name as string);

      const menuOptions =
        [
          {
            key: 'words',
            label: () => h(
                NuxtLink,
                {
                  to: {name: 'cloud'}
                }, {default: () => 'WordCloud'}
            )
          },
          {
            key: 'WordCharts',
            label: () => h(
                NuxtLink,
                {
                  to: {name: 'index'}
                }, {default: () => 'Main'}
            )
          }
            // {label: 'Облако слов', key: 'WordCloud'}
            ]
      function clickMenuItem(key: string){
        console.log(key)
      }
      const auth = useAuth();
      if (!auth.token){
        menuOptions.push(
          {
            key: 'login',
            label: () => h(
                NuxtLink,
                {
                  to: {name: 'login'}
                }, {default: () => 'Вход'}
            )
          })
      }
      return {menuOptions, clickMenuItem}

    }

});
</script>
