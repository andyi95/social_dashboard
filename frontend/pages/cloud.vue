<script setup>
import Datepicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import {ref, onMounted, computed} from "vue";

import BaseButton from "../components/BaseButton";
import BaseCard from "../components/BaseCard";
import WordCloud from "../components/WordCloud";
import {NSpace, NDatePicker, NButton, NInputNumber} from "naive-ui";
import {format} from 'date-fns';

const date = ref([Date.now() - 10080, Date.now()]);
const state = ref({limit: 100})
const errors = ref([])
const fetchedWords = ref([])

const transformWords = (words) => {
    var result = [];
  words.forEach(function (a) {
    result.push({name: a.word, value: a.count})
  })
  return result
}
const retrieveWords = () => {
  const startDate = format(
      new Date(date.value[0]), 'dd-MM-yyyy'
  )
  const endDate = format(
      new Date(date.value[1]),
      'dd-MM-yyyy'
  )
        useMyFetch(
          'dashboard/stats/',
          {
            params: {
              date__gt: startDate, date__lt: endDate, limit: state.value.limit
            }
          }).then(response => {
        fetchedWords.value = transformWords(response.data.value);
      })
          .catch(e => {
            errors.value.push(e)
          })
}
const increaseLimit = () => {
  state.value.limit += 100;
  retrieveWords();
}
onMounted(() => {
        const startDate = new Date();
      const endDate = new Date(new Date().setDate(startDate.getDate() + 7));
      date.value = [startDate, endDate]
})
const defaultDate = computed(() => {
        const startDate = new Date(new Date().setMonth(new Date().getMonth() - 1));
      const endDate = new Date();
      return [startDate, endDate];
})
function updateDate(value){
  console.log(value)
  date.value = value;
}
</script>

<template>
    <NuxtLayout>

<!--    <div class="container mt-3">-->
<!--    <div class="form-group">-->
<!--      <div class="row mb-2">-->
<!--        <div class="w-25 mb-2">-->
          <NSpace>
  <NDatePicker
      type="daterange" v-model:value="date" range :enable-time-picker="false" :default-value="defaultDate"
  />
            <NInputNumber v-model:value="state.limit"/>
<NButton mb-2 @click=retrieveWords()>Топ слов</NButton>
          </NSpace>
        <div class="row mb-2 mt-4" v-if="fetchedWords && fetchedWords.length">
          <WordCloud :words="fetchedWords"></WordCloud>

<!--          <BaseCard v-for="item in fetchedWords" :key="item.word" :title=item.word :text="item.count"/>-->
        </div>
<!--        <BaseButton class="w-25" @click=increaseLimit()>Показать ещё</BaseButton>-->
<!--      </div></div></div>-->
    </NuxtLayout>

</template>

<style scoped>

</style>