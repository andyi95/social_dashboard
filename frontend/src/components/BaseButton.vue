<template>
<button class="btn btn-primary">
  <slot>Button</slot>
</button>
</template>

<script>
export default {
  name: "BaseButton",
  // props: {
  //   onClick: {
  //     type: Function,
  //     required: true
  //   }
  // }
}
</script>

<style scoped>

</style>