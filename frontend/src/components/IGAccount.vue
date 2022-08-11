<template>
    <div class="col-md-6 offset-md-3 mt-5 text-center">
        <div class="card">
            <h4 class="card-header">Vue.js Facebook Login Example</h4>
            <div class="card-body">
              <ul class="list-group">
              <li class="list-group-item" v-for="(value, field) in IGFields" :key="field">
                {{ value }} {{ field }}
              </li>
              </ul>
            </div>
        </div>
    </div>
</template>

<script>
// import IGUserInfo from "@/services/fb.accounts";

export default {
  name: "IGAccount",
  data() {
    return {
      IGFields: [],
    };
    },
  // setup() {
  //   this.IGFields = IGUserInfo;
  // }
}
</script>

<style scoped>

</style>
