<script setup>
import {defineProps} from 'vue';
import {BASE_URL} from "@/constants/api.js";

const props = defineProps({
    product: {
        type: Object,
        id: Number,
        image: String,
        description: String,
    }
})
</script>

<template>
    <div class="card w-100" style="width: 18rem;">
        <div class="image-wrapper">
            <img :src="BASE_URL + '/products/image/' + product.id" class="card-img-top" :alt="product.description">
        </div>
        <div class="card-body">
            <p class="card-title">{{ product.description }}</p>
        </div>
    </div>
</template>

<style scoped lang="scss">
.card-body {
    display: flex;
    justify-content: center;
    align-items: self-start;
    padding: 15px 10px 30px;
}

.card-img-top {
    object-fit: contain;
    height: 100%;
    width: 100%;
}

.image-wrapper {
    height: 300px;
}

.card {
    height: 400px;
}
</style>