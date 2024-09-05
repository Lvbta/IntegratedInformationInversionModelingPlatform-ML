import Vue from 'vue'
import App from './App.vue'
import http from "./js/http";
import router from './router';
import { notification, Tree, Icon } from 'ant-design-vue';

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import 'ant-design-vue/lib/notification/style/index.css'
import 'ant-design-vue/lib/tree/style/index.css'
import 'ant-design-vue/lib/icon/style/index.css'
import '@mdi/font/css/materialdesignicons.css';


Vue.config.productionTip = false;
notification.config({
    placement: 'bottomRight',
    bottom: '30px',
    duration: 3,
});
Vue.use(ElementUI)
Vue.use(notification);
Vue.use(Tree);
Vue.use(Icon)
Vue.prototype.$http = http;
Vue.prototype.$notify = notification;
new Vue({
    router,
    render: h => h(App),
}).$mount('#app')