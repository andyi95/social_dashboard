import About from "@/views/About";
import {createRouter, createWebHistory} from 'vue-router';
import TopWords from "@/views/TopWords";
import WordCharts from "@/views/WordCharts";

const routes = [
  {path: '/', name: 'Index', component: About},
  {path: '/about', name: 'About', component: About},
  {path: '/words', name: 'TopWords', component: TopWords},
  {path: '/charts', name: 'WordCharts', component: WordCharts},

  {path: '/:catchAll(.*)', redirect: '/'},
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]
const router = createRouter({
  // eslint-disable-next-line no-undef
  history: createWebHistory(process.env.BASE_URL),
  linkActiveClass: 'active',
  routes
});
export default router

