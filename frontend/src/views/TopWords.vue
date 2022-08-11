<template>
    <div class="container mt-3">
    <div class="form-group">
      <div class="row mb-2">
        <div class="w-25 mb-2">
  <Datepicker class="mb-2" v-model="date" range :enable-time-picker="false"/>
<BaseButton mb-2 @click=retrieveWords()>Топ слов</BaseButton></div>
        <div class="row mb-2 mt-4" v-if="fetchedWords && fetchedWords.length">
          <WordCloud :words="fetchedWords"></WordCloud>

<!--          <BaseCard v-for="item in fetchedWords" :key="item.word" :title=item.word :text="item.count"/>-->
        </div>
<!--        <BaseButton class="w-25" @click=increaseLimit()>Показать ещё</BaseButton>-->
      </div></div></div>
</template>

<script type="ts">
import Datepicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import {ref, onMounted} from "vue";

import BaseButton from "../components/BaseButton";
import BaseCard from "../components/BaseCard";
import {api} from "../helpers";
import WordCloud from "../components/WordCloud";

function transformWords(words){
  var result = [];
  words.forEach(function (a) {
    result.push({name: a.word, value: a.count})
  })
  return result
}
export default {
  name: "TopWords",
  // eslint-disable-next-line vue/no-unused-components
  components: {WordCloud, BaseCard, BaseButton, Datepicker},
  data(){
    return {
      date: [],
      fetchedWords: [],
      errors: [],
      state: {
        limit:100
      }
    }
  },
  methods:{
    retrieveWords(){
      api.get('posts/', {params: {
        date__gt: this.date[0], date__lt: this.date[1]
      }})
          .then(response => {
            this.fetchedWords = null;
            this.fetchedWords = transformWords(response.data);
          })
          .catch(e => {
            this.errors.push(e)
          })
    },
  increaseLimit(){
    this.state.limit += 100
    this.retrieveWords()
  },
  },
  setup() {
    const date = ref();

    onMounted(() => {
      const startDate = new Date();
      const endDate = new Date(new Date().setDate(startDate.getDate() + 7));
      date.value = [startDate, endDate]
    })
  }
}
</script>

<style scoped>

</style>