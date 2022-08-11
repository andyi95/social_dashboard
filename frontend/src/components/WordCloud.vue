<template>
  <div ref="wordCloud" id="wordCloud" class="wordCloud"/>
</template>

<script type="ts">
import * as echarts from 'echarts';
import 'echarts-wordcloud';
import 'echarts-wordcloud/dist/echarts-wordcloud';
import 'echarts-wordcloud/dist/echarts-wordcloud.min';
// eslint-disable-next-line no-unused-vars
import {onMounted, ref} from "vue";

export default {
  name: "WordCloud",
  components: {
    // eslint-disable-next-line vue/no-unused-components
    echarts
  },
  props: {
    words: []
  },
  setup(props) {
    const wordCloud = ref(HTMLElement | null);
    // charts.value =
    onMounted(() => {
      const container = document.getElementById('wordCloud')

      var resizeContainer = function () {
        container.style.width = window.innerWidth + 'px';
        container.style.height = window.innerHeight + 'px';
      }
      resizeContainer();
      const myChart = echarts.init(
          container
      )
      var resizeListen = function () {
        resizeContainer();
        myChart.resize();
      }
      window.addEventListener('resize', resizeListen)
      myChart.setOption({
        tooltip: {
          backgroundColor: '',
          borderColor: 'blue',
          textStyle: {
                                  color: '#FFF',
                              },},
          series: [{
            type: 'wordCloud',
            gridSize: 8, // The size of the space between words
// sizeRange: [12, 50], // Minimum font and maximum font
            sizeRange: [10, 125], // Minimum font and maximum font A range must be written, not directly sizeRange: 14,
            rotationRange: [0, 0], // The range of font rotation angle , Here level
            shape: 'circle', // shape,
            keepAspect: false,
            width: '200%',
            height: '200%',
            drawOutOfBound: true, // Whether the words are superimposed
                      textStyle: {
            color: function (){
              return (
                  'rgb(' +
                  Math.round(Math.random() * 255 ) + ', ' +
                  Math.round(Math.random() * 255 ) + ', ' + Math.round(Math.random() * 255 ) + ', ' + ')'
              )
            },
          },
            emphasis: { // Highlight the effect of
              textStyle: {
                shadowBlur: 10, // Shadow distance
                shadowColor: '#red', // Shadow color
              },
            },
            data: props.words
          }]

      })
    })
    return {wordCloud}
  }
}

</script>

<style scoped>

</style>
