<template>
  <div class="form-group">

    <n-input v-model:value="username" placeholder="email"/>
    <n-input v-model:value="password">Password</n-input>

  </div>
  <n-button @click="login">Login</n-button>
</template>

<script>
import BaseButton from "@/components/BaseButton";
import BaseInput from "@/components/BaseInput";
import {api} from "@/helpers";
import {NButton, NInput} from "naive-ui";

export default {
  name: "LoginView",
  data() {
    return {
      username: '',
      password: ''
  }
  },
  components: {
    BaseInput,
    BaseButton, NButton, NInput
  },
  methods:{
    login() {
      console.log('Trying to login with ' + this.username + 'password ' + this.password);
      api.post(
          'token/login', {'email': this.username, 'password': this.password}
      ).then((response) => {
        const token = response.data.auth_token;
        this.$store.commit('setToken', token)
        api.defaults.headers.common['Authorization'] = 'Token ' + token;
        this.$router.push('/')
      })
    }
  }
}
</script>
