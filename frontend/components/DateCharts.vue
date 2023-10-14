<template>
  <div id="wordChart" ref="wordChart" class="wordChart" :key="keyValue"/>
</template>

<script>
/* eslint-disable no-unused-vars */
import * as echarts from 'echarts';
import {onMounted, ref} from "vue";

function extractDate(items) {
  return  {
    dates: items.map(a => a.date).reverse(),
    counts: items.map(a => a.ratio).reverse()
  }

}

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
  data(){
    return {
      option: {
        name: 'charts',
        xAxis: {
          data: []
        },
        yAxis: {
          type: 'value'
        },
        series:
          {
            data: [],
            type: 'line'
          }

      },
      chart: null
    }

  },
    methods: {
    rerenderChart() {
      this.key = this.key + 1
    },
      initChart(){
            const container = document.getElementById('wordChart')
      var resizeContainer = function () {
        container.style.width = window.innerWidth + 'px';
        container.style.height = (window.innerHeight - 20) + 'px';
      }
      resizeContainer();
      // type EChartOptions = echarts.EChartsOption;
      this.chart = echarts.init(container);
            var resizeListen = function () {
        resizeContainer();
        this.chart.resize();
        window.addEventListener('resize', resizeListen);
              const transformed = extractDate(this.props.words)
              this.options.xAxis.data = transformed.dates
              this.options.series.data = transformed.counts
      this.chart.setOption(this.options);
      }
      }
  },
    watch: {
    words: {
      handler: function (newData) {
        let transformed = extractDate(newData)
        this.option.xAxis.data = transformed.dates
        this.option.series.data = transformed.counts
        this.chart.clear()
        this.chart.setOption(this.option)

      },
      deep: true
    }
  },
  mounted() {
    this.initChart()
  },

  // setup(props) {
  //   const dateCharts = ref(HTMLElement | null);
  //
  //   onMounted(() => {
  //     const container = document.getElementById('wordChart')
  //     var resizeContainer = function () {
  //       container.style.width = window.innerWidth + 'px';
  //       container.style.height = (window.innerHeight - 20) + 'px';
  //     }
  //     resizeContainer();
  //     // type EChartOptions = echarts.EChartsOption;
  //     var myChart = echarts.init(container);
  //     var resizeListen = function () {
  //       resizeContainer();
  //       myChart.resize();
  //     }
  //     window.addEventListener('resize', resizeListen)
  //     const transformed = extractDate(props.words)
  //     let options = {
  //       xAxis: {
  //         data: transformed.dates
  //       },
  //       yAxis: {
  //         type: 'value'
  //       },
  //       series: [
  //         {
  //           data: transformed.counts,
  //           type: 'line'
  //         }
  //       ]
  //     }
  //     myChart.setOption(options);
  //   })
  // },


}
</script>

<style scoped>

</style>