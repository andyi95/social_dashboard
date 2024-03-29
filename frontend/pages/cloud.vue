<script>
import Datepicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import {ref, onMounted} from "vue";

import BaseButton from "../components/BaseButton";
import BaseCard from "../components/BaseCard";
import WordCloud from "../components/WordCloud";
import {NSpace, NDatePicker, NButton, NInputNumber} from "naive-ui";

function transformWords(words){
  var result = [];
  words.forEach(function (a) {
    result.push({name: a.word, value: a.count})
  })
  return result
}
export default {
  name: "cloud",

  components: {WordCloud, BaseCard, BaseButton, NSpace, NDatePicker, NButton, NInputNumber},
  data() {
    return {
      date: [],
      fetchedWords: [],
      errors: [],
      state: {
        limit: 100
      }
    }
  },
  methods: {
    retrieveWords() {
      useMyFetch(
          'dashboard/stats/',
          {
            params: {
              date__gt: this.date[0], date__lt: this.date[1]
            }
          }).then(response => {
        this.fetchedWords = transformWords(response.data.value);
      })
          .catch(e => {
            this.errors.push(e)
          })
    },
    increaseLimit() {
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
  },
  computed: {
    defaultDate() {
      const startDate = new Date(new Date().setMonth(new Date().getMonth() - 1));
      const endDate = new Date();
      return [startDate, endDate];
    }
  }
}
</script>

<template>
    <NuxtLayout>

<!--    <div class="container mt-3">-->
<!--    <div class="form-group">-->
<!--      <div class="row mb-2">-->
<!--        <div class="w-25 mb-2">-->
          <NSpace>
  <NDatePicker type="daterange" v-model="date" range :enable-time-picker="false" :default-value="defaultDate"/>
            <NInputNumber v-model:value="state.limit"/>
<NButton mb-2 @click=retrieveWords()>Топ слов</NButton>
          </NSpace>
        <div class="row mb-2 mt-4" v-if="fetchedWords && fetchedWords.length">
          <WordCloud :words="{words: fetchedWords}"></WordCloud>

<!--          <BaseCard v-for="item in fetchedWords" :key="item.word" :title=item.word :text="item.count"/>-->
        </div>
<!--        <BaseButton class="w-25" @click=increaseLimit()>Показать ещё</BaseButton>-->
<!--      </div></div></div>-->
    </NuxtLayout>

</template>

<style scoped>

</style>