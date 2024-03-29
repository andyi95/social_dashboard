<script lang="ts">
export default defineComponent({
  name: 'Group',
  async setup() {
    const {params} = useRoute();
    const groupID = params.groupID;
    const {data, error, pending, refresh } = await useMyFetch(
        `dashboard/groups/${groupID}/`,
    )
    return {
      group: data.value
    }
  }
})
</script>

<template>
<div class="mb-10 container m-auto grid grid-cols-2 gap-3">
  <div class="tile col-span-2">
  <div class="title">{{group.name}}</div>
  <div>{{group.screen_name}}</div>
  <div> {{group.description}}</div>
    </div>
  <div class="tile col-span-2">
    <div v-for="post in group.posts" :key="post.id">
      <div class="title">{{post.text}}</div>
      <div>{{post.likes_count}}</div>
      <div>{{post.repost_count}}</div>
</div>
    </div>
  </div>
</template>

<style scoped>

</style>