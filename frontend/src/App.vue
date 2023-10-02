<template>
    <div class="main">
        <button type="button" class="btn btn-primary mt-3" data-bs-toggle="modal" data-bs-target="#createProductModal">
            Создать товар
        </button>
        <CreateProductModal/>
        <ProductGrid v-if="!loading && !cantLoad && !(productsStore.products.length === 0)"/>
        <span v-else-if="!loading && !cantLoad && productsStore.products.length === 0"><br>Товаров нет.</span>
        <Loader v-else-if="loading && !cantLoad"/>
        <span v-else><br>Сервис временно недоступен.<br>Приносим извинения за предоставленные неудобства.</span>
    </div>
</template>

<script setup>
import {onMounted, ref} from 'vue';
import {useProductsStore} from '@/stores/products';
import {BASE_URL} from "@/constants/api.js"
import ProductGrid from "@/components/ProductGrid.vue";
import Loader from "@/components/Loader.vue";
import CreateProductModal from "@/components/CreateProductModal.vue";

const loading = ref(false);
const cantLoad = ref(false);
const productsStore = useProductsStore();

const fetchProducts = () => {
    loading.value = true;
    return fetch(BASE_URL + '/products/')
        .then((response) => {
            if (!response.ok) {
                throw new Error('Failed to fetch products');
            }
            return response.json();
        });
};

onMounted(async () => {
    if (productsStore.products.length !== 0) {
        loading.value = false;
        return;
    }

    const maxAttempts = 5;
    const retryDelay = 1000;

    const retryFetch = async (attempt) => {
        try {
            productsStore.products = await fetchProducts();
            loading.value = false;
        } catch (err) {
            console.log("Failed attempt: " + attempt);
            if (attempt < maxAttempts) {
                setTimeout(() => retryFetch(attempt + 1), retryDelay);
            } else {
                cantLoad.value = true;
                loading.value = false;
            }
        }
    };
    await retryFetch(1);
});
</script>

<style lang="scss">
.main {
    width: 100%;
    text-align: center;
    margin: 0 auto;
    overflow-x: hidden;
}
</style>