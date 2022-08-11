<template>
  <div id="app">
    <n-menu :options="navlinks" mode="horizontal"/>
    <router-view/>
  </div>
</template>

<script>
/* eslint-disable no-unused-vars */
import {defineComponent, h, Component} from "vue";
import {NIcon} from 'naive-ui';
import {RouterLink} from 'vue-router';
import {NMenu} from "naive-ui";
const navlinks = [
  {
    key: 'words',
    label: () => h(
        RouterLink,
        {
          to: {name: 'TopWords'}
        }, {default: () => 'Анализ слов'}
    )
  },  {
    key: 'about',
    label: () => h(
        RouterLink,
        {
          to: {name: 'About'}
        }, {default: () => 'Что-то будет'}
    )
  },
  {
    key: 'WordCharts',
    label: () => h(
        RouterLink,
        {
          to: {name: 'WordCharts'}
        }, {default: () => 'Тренды слов'}
    )
  },
  {
    key: 'login',
    label: 'Вход'
  }
]
// function renderIcon (icon: Component)
export default {
  data() {
    return {
      navlinks: navlinks
    }
  },components: {NMenu}
}
</script>
<style scoped>
.nav-link a{
  color: #1FAB89!important;
  padding-left: 7px!important;
  display: block!important;
}
.brand-logo {
  color: #1266f1;
}

.nav-item{
    color: #6098a1!important;
    padding-left: 7px!important;
    display: block;
}
.nav-item:hover {
  background-color: #393E46;
}

.nav-bg-custom {
    background-color: #222831;
}

</style>
