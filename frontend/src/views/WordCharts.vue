<template>
  <n-input v-model="word" placeholder="слово для поиска"/>
  <n-button @click="fetchData">Показать график</n-button>

<DateCharts :words="sampleData" v-if="sampleData"/>
</template>

<script>
import DateCharts from "@/components/DateCharts";
import {NInput, NButton} from "naive-ui";
import {api} from "@/helpers";
// import {onMounted} from "vue";
// const sampleData =
//     [
//       {
//         "ex_date": "2017-01-01",
//         "id": 400632,
//         "word": "россия",
//         "count": 5,
//         "date": "2017-01-01T13:28:42Z"
//       },
//       {
//         "ex_date": "2017-01-02",
//         "id": 400519,
//         "word": "россия",
//         "count": 5,
//         "date": "2017-01-02T21:35:15Z"
//       },
//       {
//         "ex_date": "2017-01-03",
//         "id": 400313,
//         "word": "россия",
//         "count": 2,
//         "date": "2017-01-03T23:26:00Z"
//       }
//       ]
export default {
  name: "WordCharts",
  components: {DateCharts, NInput, NButton},
  data(){
    return {
      sampleData: null,
      errors: [],
      word: String
    }
  },
  emits:['update:word'],
  methods: {
    fetchData(){
      api.get('posts/'+ this.word + '/?exact=true').then(
          response => {
            this.sampleData = response.data;
          }
      ).catch(e => {
        this.errors.push(e)
      })
    }
  },
  // setup(){
  //   onMounted(() => {
  //     api.get('posts/россия/?exact=true').then(
  //         response => {
  //           this.sampleData = response.data;
  //         }
  //     ).catch(e => {
  //       this.errors.push(e)
  //     })
  //   })
  // }

}
</script>

<style scoped>

</style>
