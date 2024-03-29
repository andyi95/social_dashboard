<script lang="ts">
import {defineComponent, ref} from 'vue'
import {isYesterday, addDays} from "date-fns";
import {NCalendar} from "naive-ui";


export default defineComponent({
  name: "Calendar",
  components: {NCalendar},
  setup(){
    return {
      calendarDays: ref(addDays(Date.now(), 1).valueOf()),
      isDateDisabled: (date) => {
        return isYesterday(date)
      }
    }
  }
})
</script>

<template>
<NCalendar v-model:value="calendarDays" #="{ year, month, date }" :is-date-disabled="isDateDisabled"/>
</template>

<style scoped>

</style>