<script setup lang="ts">
import {NDatePicker} from 'naive-ui';
import {defaultDt} from '~/helpers/date-ranges';
const props = defineProps({
  dateRange: {
    type: Array,
    default: [defaultDt.start, defaultDt.end]
  }
})
</script>

<template>
<NDatePicker type="daterange" v-model:value="$props.dateRange" range :enable-time-picker="false"/>
</template>

<style scoped>

</style>