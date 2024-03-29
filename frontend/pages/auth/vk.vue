<script setup lang="ts">
const route = useRoute();
const router = useRouter();
const selectedKeys = ref<string>(route.name as string);
useMyFetch(
    'social/accounts/1/vk/token/', {
      method: 'POST',
      body: {
        code: route.query.code,
        redirect_uri: 'http://localhost:3000/auth'
      }
    }
).then(response => {
  localStorage.setItem('vk_token', response.data.value.token)
  router.push({name: 'index'})
}).catch(e => {
  console.log(e)
})
</script>

<template>
  <NuxtLayout>
        <template #header>
      <NavBar />
    </template>
<NCard>Success</NCard>
    </NuxtLayout>
</template>

<style scoped>

</style>