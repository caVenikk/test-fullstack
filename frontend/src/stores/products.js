import {defineStore} from 'pinia'

export const useProductsStore = defineStore('products', {
    state: () => ({
        products: [],
    }),
    getters: {
        getProducts() {
            return this.products;
        },
    },
    actions: {
        setProducts(products) {
            this.products = products;
        },
    },
})