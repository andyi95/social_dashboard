<template>
        <NH2>Projects</NH2>
        <NMenu
            :options="menuOptions"
            @update:value="clickMenuItem"
        />
</template>

<script lang="ts">
import type {MenuOption, MenuDividerOption, MenuGroupOption} from 'naive-ui';
import {NH2, NMenu, NInput} from 'naive-ui';
import {NuxtLink} from "#components";
import {h} from "vue";

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
          },
          {
            key: 'login',
            label: () => h(
                NuxtLink,
                {
                  to: {name: 'login'}
                }, {default: () => 'Вход'}
            )
          }
            // {label: 'Облако слов', key: 'WordCloud'}
            ]
      function clickMenuItem(key: string){
        console.log(key)
      }
      return {menuOptions, clickMenuItem}

    }

});
</script>
