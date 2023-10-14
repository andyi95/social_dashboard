<template>
  <n-input :id="inputID" v-model:value="value" :placeholder="label" />
</template>

<script lang="js">
import {defineComponent, ref} from "vue";
import NInput from 'naive-ui'

export default defineComponent( {
  name: "BaseInput",
  components: {
    NInput,
  },
  props: {
    label: {
      type: String, required: true
    },
    type: {
      type: String, required: false
    }
  },
    setup() {
    const inputID = ref(null);
    return {
      value: ref(null),
      inputID
    }
  }
})
</script>

<style scoped>

</style>
