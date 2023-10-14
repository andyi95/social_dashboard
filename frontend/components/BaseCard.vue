<template>
  <n-card :title="title">
    {{ content }}
  </n-card>
</template>

<script>
export default {
  name: "BaseCard",
  props: {
    title: String, content: String
  }
}
</script>

<style scoped>

</style>