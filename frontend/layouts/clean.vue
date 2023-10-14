<template>
    <div>
        <NLayout position="absolute">
            <NLayoutContent>
                <slot />
            </NLayoutContent>
        </NLayout>
    </div>
</template>

<script>
import {NLayout, NLayoutContent} from 'naive-ui';

export default defineComponent({
    components: {
        NLayoutContent,
        NLayout
    }
});
</script>
