<template>
  <div class="form-group">
<BaseInput label="Имя пользователя" v-model="username"></BaseInput>
    <BaseInput label="Пароль" type="password" v-model="password"></BaseInput>
  </div>
<BaseButton on-click="auth()">Вход</BaseButton>
</template>

<script>
import BaseButton from "@/components/BaseButton";
import BaseInput from "@/components/BaseInput";
import {api} from "@/helpers";


export default {
  name: "LoginView",
  components: {
    BaseInput,
    BaseButton
  },
  methods:{
    login() {
      console.log('Trying to login with ' + this.username + 'password ' + this.password);
      api.post(
          'auth/token/', {'username': this.username, 'password': this.password}
      )
    }
  }
}
</script>
