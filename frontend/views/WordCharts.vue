<template>
  <n-input v-model:value="word" placeholder="слово для поиска"/>
  <n-button @click="fetchData">Показать график</n-button>
<n-button @click="increaseLimit">Показать ещё</n-button>
<DateCharts :words="sampleData" v-if="sampleData"/>
</template>

<script>

import {NButton, NInput} from "naive-ui";
import {api} from "@/helpers";
import DateCharts from "../components/DateCharts.vue";
import {defineComponent, ref} from "vue";

export default defineComponent({
  name: "WordCharts",
  components: {DateCharts, NInput, NButton},
  data(){
    return {
      sampleData: null,
      errors: [],
      word: '',
      limit: 10
    }
  },
  methods: {
    increaseLimit(){
      this.limit += 10
      this.fetchData()
    },
    fetchData(){
      api.get('dashboard/'+ this.word + '/?exact=true&limit=' + this.limit).then(
          response => {
            this.sampleData = response.data;
          }
      ).catch(e => {
        this.errors.push(e)
      })
    }
  },

})
</script>

<style scoped>

</style>
