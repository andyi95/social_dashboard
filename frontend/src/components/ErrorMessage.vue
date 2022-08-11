<template>
  <div class="accordion-item">
  <div class=" accordion-header" id="headingError">
<button class="btn btn-warning btn-sm w-100" type="button" data-mdb-toggle="collapse" data-mdb-target="#collapseOne" aria-expanded="false" aria-controls="collapseOne">
  {{ error.message }}</button></div>
      <div class="collapse alert alert-warning mt-3" id="collapseOne">
        {{ error.stack }}</div>
</div>
</template>

<script>
export default {
  name: "ErrorMessage",
  props: {
    error: Error
  }
}
</script>
