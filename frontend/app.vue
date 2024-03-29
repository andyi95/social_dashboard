<template>
  <NConfigProvider :theme="theme" :locale="ruRU" :date-locale="dateRuRU">
    <NMessageProvider>
      <NDialogProvider>
        <NuxtPage />
      </NDialogProvider>
    </NMessageProvider>
  </NConfigProvider>
</template>
<script setup lang="ts">
import {NMessageProvider, NConfigProvider, NDialogProvider, ruRU, dateRuRU, darkTheme, useMessage} from 'naive-ui';
import {useTheme} from "~/store/useTheme";
// import {useTheme} from 'store/useTheme.ts'
  // components: {NMessageProvider, NConfigProvider, NDialogProvider},
  // setup(){
const themeStore = useTheme();
const theme = computed(() => {
  return themeStore.$state.themeType === 'dark' ? darkTheme : null;
});


</script>