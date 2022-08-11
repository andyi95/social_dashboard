<template>
  <div class="form-group pt-8 pb-4">
<label :for="id" v-if="help_text">{{ help_text }}</label>
  <input type="text" class="form-control" id="id">
    </div>
</template>

<script>
export default {
  name: "BaseInput",
  props: {
    label: {
      type: String, required: true
    },
    help_text: {
      type: String, required: false
    },
    type: {
      type: String, required: false
    }
  },
  mounted() {
    this.id = this._uid;
  }
}
</script>

<style scoped>

</style>
