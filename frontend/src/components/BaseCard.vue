<template>
  <n-card :title="title">
    {{ text }}
  </n-card>
</template>

<script>
export default {
  name: "BaseCard",
  props: {
    title: String, text: String
  }
}
</script>

<style scoped>

</style>