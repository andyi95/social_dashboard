<template>
  <div>
    <NLayout>
      <NLayoutHeader bordered class="bg-white px-15 border-b bc-eee flex items-center h-[60]">
            <NButton @click="themeStore.doToggleTheme">{{ themeStore.themeType === 'light' ? 'Dark' : 'Light' }}</NButton>
<NavBar/>
      </NLayoutHeader>
      <NLayoutContent class="flex-1 overflow-hidden px-3 min-h-100">
            <slot />
      </NLayoutContent>
    </NLayout>
  </div>
</template>
<style>
body, #app, .n-layout-scroll-container, .n-config-provider, .n-layout--static--positioned{
  min-height: 100vh;
}

#app {
  font-family: Roboto, Helvetica, Arial, sans-serif;
  /*height: 100%;*/

}
.n-layout-scroll-container{
  padding-left: .75rem;
  padding-right: .75rem;
  padding-top: .50rem;
  padding-bottom: .25rem;
}
</style>

<script>
import {NLayout, NButton, NLayoutHeader, NLayoutContent, NLayoutSider, NAlert, useMessage} from 'naive-ui';
import ButtonLink from '../components/ButtonLink';
import {useTheme} from '~/store/useTheme';

export default defineComponent({
  components: {
    ButtonLink,
    NAlert,
    NLayoutContent,
    NLayoutSider,
    NButton,
    NLayoutHeader,
    NLayout
  },
  setup() {
    const themeStore = useTheme();
    return {
      themeStore,
      randomPhrase: computed(() => {
        const all = [
            'social media',
            'inspiration'
        ];

        return all[Math.floor(Math.random() * all.length)];
      })
    };
  },

});
</script>
