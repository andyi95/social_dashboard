<script lang="ts">
import {
  NForm,
  NFormItem,
  NInput,
  NButton,
  NGrid,
  NGridItem,
  NH1, useMessage
} from 'naive-ui';
import useAuth from '~/store/useAuth';

export default {
  components: {
    NForm,
    NFormItem,
    NInput,
    NButton,
    NGrid,
    NGridItem,
    NH1
  },
  setup() {
    const authParams = ref({
      email: '',
      password: ''
    });

    const message = useMessage();

    const auth = useAuth();

    async function onSubmit() {
      const {email, password} = authParams.value;
      if (!email || !password) {
        return;
      }

      try {
        await auth.login({email, password});
      } catch (error) {
        message.error('Auth error');
        console.log(error);
      }
    }

    return {
      formValue: authParams,
      onSubmit
    };
  }}
</script>

<template>
  <NuxtLayout>
    <template #header>
      <NavBar />
    </template>
    <NForm @submit.prevent="onSubmit">
      <NFormItem label="Email">
        <NInput v-model:value="formValue.email" size="large" /></NFormItem>
      <NFormItem label="Password">
        <NInput v-model:value="formValue.password" size="large" type="password" /></NFormItem>
      <NButton attr-type="submit" size="large" >Login</NButton>
    </NForm>
  </NuxtLayout>

</template>

<style scoped>

</style>