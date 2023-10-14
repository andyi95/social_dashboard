<template>
  <div>
    <NLayout position="absolute">
      <NLayoutHeader bordered position="absolute" class="h-[50px] flex items-center justify-between px-4">
            <ButtonLink to="/">
              <div class="flex items-center">
                <div class="text-3xl font-extrabold tracking-widest m-0">
                  SM
                </div>
              </div>
            </ButtonLink>
          <div class="ml-auto">
            <NButton @click="doToggleTheme">{{ themeType === 'light' ? 'Dark' : 'Light' }}</NButton>
          </div>
      </NLayoutHeader>

      <NLayout position="absolute" class="layout top-[50px]" has-sider>
        <NLayoutSider bordered class="pr-px">
          <div class="px-3">
            <slot name="sidebar">
              <NAlert type="error"> SliderForgotten! </NAlert>
            </slot>
          </div>
        </NLayoutSider>
        <NLayoutContent>
          <div class="p-5 space-y-4">
            <slot />
          </div>
        </NLayoutContent>
      </NLayout>
    </NLayout>
  </div>
</template>


<script>
import {NLayout, NButton, NLayoutHeader, NLayoutContent, NLayoutSider, NAlert} from 'naive-ui';
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
    const {doToggleTheme, theme, themeType} = useTheme();

    return {
      doToggleTheme,
      theme,
      themeType,
      randomPhrase: computed(() => {
        const all = [
            'social media',
            'inspiration'
        ];

        return all[Math.floor(Math.random() * all.length)];
      })
    };
  }
});
</script>
