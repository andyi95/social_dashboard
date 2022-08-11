<template>
<Navigation/>
</template>

<script>


import Navigation from "./components/Navigation";
// export default defineComponent({
//   setup(){
//     return {
//       darkTheme,
//       Navigation
//     }
//   },
//   components:
//       {Navigation, NConfigProvider }
// })

export default {
  components: {Navigation},
}
</script>

<style lang="css">

#app {
  font-family: Roboto, Helvetica, Arial, sans-serif;
}
</style>
