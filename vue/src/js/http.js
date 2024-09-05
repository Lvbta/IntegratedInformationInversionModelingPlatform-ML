import axios from 'axios'
import Vue from "vue";
const http = axios.create({
    //baseURL:'http://192.168.1.8:5000'
})

http.interceptors.response.use(res => {
    return res
}, error => {
    if (error.response.data.message) {
        Vue.prototype.$message({
            type: 'error',
            message: error.response.data.message
        })
    }
    if (error.response.status === 500) {
        // router.push('/login')
        Vue.prototype.$message({
            type: 'error',
            message: "服务器内部错误，请检查服务器！"
        })
    }
    return Promise.reject(error)
})
export default http