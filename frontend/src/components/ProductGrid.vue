<template>
    <div class="product-grid">
        <ProductCard v-for="product in products" :key="product.id" :product="product"></ProductCard>
    </div>
</template>

<script setup>
import {useProductsStore} from '@/stores/products';
import ProductCard from "@/components/ProductCard.vue";

const productsStore = useProductsStore();

const products = productsStore.products;
</script>

<style lang="scss" scoped>
.product-grid {
    display: grid;
    grid-gap: 16px;
    padding: 16px;

    @media (min-width: 768px) {
        grid-template-columns: repeat(3, 1fr);
    }

    @media (min-width: 960px) {
        grid-template-columns: repeat(4, 1fr);
    }

    @media (min-width: 1200px) {
        grid-template-columns: repeat(5, 1fr);
    }
}
</style>