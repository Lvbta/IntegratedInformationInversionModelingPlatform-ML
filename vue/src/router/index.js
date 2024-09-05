import Vue from 'vue'
import VueRouter from 'vue-router'
import login from '../views/login/login.vue'
import olmap from '../views/map/olmap.vue'

Vue.use(VueRouter)

const routes = [{
        path: '/',
        name: 'login',
        component: login
    },
    {
        path: '/working',
        name: 'olMap',
        component: olmap,
    },
]

const router = new VueRouter({
    routes
})

export default router