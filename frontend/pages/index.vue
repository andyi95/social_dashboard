<template>
  <NuxtLayout>
    <template #sidebar>
      <SideMenu />
    </template>
    <h1>Intro</h1>
    <p>In the age of digital connectivity, social media has become an indispensable part of our lives.</p>
    <p>It's a treasure trove of opinions, trends, and valuable information waiting to be uncovered.</p>
    <p>Welcome to the \"Social Media Insights Dashboard,\" your gateway to unlocking the power of social media data.</p>

    <h2>Last News</h2>
    <div v-if="pending">
    <NSpin size="large"/></div>
<div v-if="data">
    <NTimeline>
      <NTimelineItem v-for="(item, idx) in data.results" :key="idx">
        <NCard>
          {{item.text}}
          <template #footer>
            {{item.likes_count}} likes
            {{item.repost_count}} reposts
          </template>
        </NCard>
      </NTimelineItem>
    </NTimeline></div>
  </NuxtLayout>
</template>

<script setup lang="ts">
import {NTimeline, NTimelineItem, NCard, NSpin} from "naive-ui";

let limit = 10;
let page = 1
const {data, error, pending, refresh } = await useMyFetch(
    'dashboard/posts/', {
      params: {page: page}
    }
)
</script>