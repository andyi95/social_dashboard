<template>
  <NuxtLayout>
    <h1>Intro</h1>
    <p>In the age of digital connectivity, social media has become an indispensable part of our lives.</p>
    <p>It's a treasure trove of opinions, trends, and valuable information waiting to be uncovered.</p>
    <p>Welcome to the "Social Media Insights Dashboard" your gateway to unlocking the power of social media data.</p>
  <NButton type="primary" size="large" round @click="onClickStarted">Get Started</NButton>
    <h2>Last News</h2>
<div>
    <NTimeline>
      <NTimelineItem v-for="(item, idx) in posts.posts" :key="item.id" v-bind:id="item.id">
        <NCard>
          {{item.text}}
          <template #footer>
            <NIcon style="width: 15px"><Heart style="width: 15px;"/></NIcon>{{item.likes_count}}
            <NIcon style="width: 15px;"><ShareSocial style="width: 15px;"/></NIcon>{{item.repost_count}}
          </template>
          <a :href="`/groups/${item.group.id}`">{{item.group.name}}</a>
        </NCard>
      </NTimelineItem>
    </NTimeline></div>
    <NButton tertiary @click="loadMorePosts">Load More</NButton>
  </NuxtLayout>
</template>

<script setup lang="ts">
import {NTimeline, NTimelineItem, NCard, NSpin, NButton} from "naive-ui";
import {ShareSocial, Heart} from '@vicons/ionicons5'
import {onMounted} from "vue";
// import {GroupResponse} from '~/models/Responses';

import Loader from '@/components/Loader.vue';
let isShow = true;
let page = 1


const posts = reactive({
  posts: []
})
const groups = reactive({
  groups: []
})

const loadMorePosts = () => {
  page += 1
  useMyFetch(
      'dashboard/posts/', {
        params: {page: page, limit: 10}
      }
  ).then(response => {
    posts.posts.push(...response.data.value.results)
  }).catch(e => {
    console.log(e)
  })
}
const handleScroll = (event: any) => {
  const scrollHeight = event.target.scrollingElement.scrollHeight
  const scrollTop = event.target.scrollingElement.scrollTop
  const clientHeight = event.target.scrollingElement.clientHeight
  if (clientHeight + scrollTop >= scrollHeight) {
    isShow = false;
    loadMorePosts()
    isShow = true;
  }
}
function onClickStarted(){
  window.location.href = auth_link
}
// type GroupList = Array<GroupResponse>
let auth_link = ''
onMounted( () => {
  useMyFetch(
      'social/accounts/vk/auth_url/',
      {
        params: {
          redirect_uri: 'http://localhost:3000/auth/vk'
        }
      }
  ).then(response => {
    auth_link = response.data.value.url
  })
  useMyFetch('dashboard/groups/').then(response => {
    groups.groups = response.data.value.results
  })
})


</script>