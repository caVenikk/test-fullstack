import {createApp} from 'vue'
import {createPinia} from 'pinia';
import App from './App.vue'

import "jquery/dist/jquery.js"
import "jquery"

import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap/dist/js/bootstrap.bundle.js"
import "bootstrap"

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);

app.mount('#app');
