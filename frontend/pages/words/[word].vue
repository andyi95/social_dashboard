<script lang="ts">
import {defineComponent} from 'vue'
import {NButton, NInput, NGrid, NGridItem} from "naive-ui";
import DateCharts from "@/components/DateCharts.vue";
import Calendar from "@/components/Calendar.vue";
import useAuth from "~/store/useAuth";

export default defineComponent({
  name: "[word]",
  components: {NButton, NInput, DateCharts, Calendar, NGrid, NGridItem},

  data(){
    const route = useRoute();
    return {
      sampleData: null,
      errors: [],
      word: route.params.word,
      limit: 10
    }
  },
  methods: {
    async increaseLimit() {
      this.limit += 30
      await this.fetchData()
    },
    async fetchData() {
      const {data, error, pending} = await useMyFetch(
          `dashboard/stats/${this.word}/`,
          {
            params: {
              limit: this.limit
            }
          })
      if (error){
        console.log(error)
      }
      else{
        this.sampleData = data.value
      }

    }
  },
  setup() {
    const store = useAuth();
    return {store}
  }
})
</script>

<template>
  <NuxtLayout>
  <Loader v-if="store.isLoading"/>
  <div class="container m-auto grid grid-cols-2 gap-3" v-else>
    <div class="">
  <n-input v-model:value="word" placeholder="слово для поиска"/>
  <n-button @click="fetchData">Показать график</n-button>
  <n-button @click="increaseLimit">Показать ещё</n-button></div>
    <div class="">
  <DateCharts :words="sampleData" v-if="sampleData"/></div>
    <div class="tile"><Calendar/></div>
  </div></NuxtLayout>
</template>


<style scoped>

</style>