<template>
  <div id="wordChart" ref="wordChart" class="wordChart" :key="keyValue"/>
</template>

<script>
/* eslint-disable no-unused-vars */
import * as echarts from 'echarts';
import {onMounted, ref} from "vue";

function extractDate(items) {
  return  {
    dates: items.map(a => a.ex_date),
    counts: items.map(a => a.count)
  }

}

// type ChartProps = {
//   ex_date: Date,
//   id: number,
//   word: string,
//   count: number,
//   date: Date
// }[]
export default {
  name: "DateCharts",
  components: {
    // eslint-disable-next-line vue/no-unused-components
    echarts
  },
  /* eslint-disable no-unused-vars */

  props: {
    words: {
      type: Array, default() {
        return []
      }
    },
    keyValue: {
      type: Number,
      default() {
        return 0
      }
    }
  },
  setup(props) {
    const dateCharts = ref(HTMLElement | null);

    onMounted(() => {
      const container = document.getElementById('wordChart')
      var resizeContainer = function () {
        container.style.width = window.innerWidth + 'px';
        container.style.height = (window.innerHeight - 20) + 'px';
      }
      resizeContainer();
      // type EChartOptions = echarts.EChartsOption;
      var myChart = echarts.init(container);
      var resizeListen = function () {
        resizeContainer();
        myChart.resize();
      }
      window.addEventListener('resize', resizeListen)
      const transformed = extractDate(props.words)
      let options = {
        xAxis: {
          data: transformed.dates
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: transformed.counts,
            type: 'line'
          }
        ]
      }
      myChart.setOption(options);
    })
  },
  methods: {
    rerenderChart() {
      this.key = this.key + 1
    }
  },
  watch: {
    words: {
      handler: function () {
        // this.renderChart(this.words, {responsive: true, maintainAspectRatio: false, beginAtZero: true})
        this.rerenderChart()
      }
    }
  }
}
</script>

<style scoped>

</style>