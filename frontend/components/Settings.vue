<template>
<select class="form-select" aria-label="цветовая схема">
  <option selected >Упрощенная</option>
</select>
</template>

<script>
export default {
  name: "Settings",
  props: {
    colors: [
      {
        tag: 'NOUN', color: '#0000ff'
      },
      {tag: 'VERB', color: '#009933'},
      {tag: 'INFN', color: '#009933'},
    ]
  }
}
</script>

<style scoped>

</style>