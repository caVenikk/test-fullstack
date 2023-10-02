<script setup>
import {ref} from 'vue';
import {BASE_URL} from "@/constants/api.js";

const productDescription = ref('');
let productImageFile = null;

const createProduct = async () => {
    if (!productDescription.value || !productImageFile) {
        console.log('Fill form data');
        return;
    }

    const formData = new FormData();
    formData.append('description', productDescription.value);
    formData.append('image', productImageFile);

    try {
        const response = await fetch(BASE_URL + '/products/', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            console.log(response);
            const product = await response.json();
            console.log('Product created:', product);
        } else {
            console.log(response)
            console.error('Error creating product:', response.statusText);
        }
    } catch (error) {
        console.error('An error occurred:', error);
    }
    location.reload();
};

const handleFileChange = (event) => {
    productImageFile = event.target.files[0];
};
</script>

<template>
    <div class="modal fade" id="createProductModal" tabindex="-1" aria-labelledby="createProductModalLabel"
         aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="createProductModalLabel">Создать товар</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form @submit.prevent="createProduct">
                    <div class="modal-body">
                        <div class="mb-3">
                            <label for="product-description" class="col-form-label">Описание товара:</label>
                            <input type="text" class="form-control" id="product-description"
                                   v-model="productDescription">
                        </div>
                        <div class="mb-3">
                            <label for="product-image" class="col-form-label">Изображение товара</label>
                            <input type="file" class="form-control" id="product-image" @change="handleFileChange">
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Закрыть</button>
                        <button type="submit" class="btn btn-primary">Создать</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss">

</style>