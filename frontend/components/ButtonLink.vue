<template>
    <NuxtLink v-slot="{href, navigate}" :to="link" custom>
        <NButton :href="href" tag="a" text @click="navigate"><slot></slot></NButton>
    </NuxtLink>
</template>
<script lang="ts">
import {NButton} from 'naive-ui';
export default defineComponent({
    components: {
        NButton
    },
    props: {
        to: {
            type: String,
            default: ''
        }
    },
    setup(props) {
        return {
            link: props.to
        };
    }
});
</script>
