<template>
<div class="ms-2 me-auto">
  {{ title }}
</div>
  <span class="badge bg-primary rounded-pill">{{ text }}</span>
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