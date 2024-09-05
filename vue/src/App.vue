<template>
  <router-view></router-view>
</template>

<script>
import login from "./views/login/login.vue";
import olmap from "./views/map/olmap.vue";

export default {
  name: "App",
  components: {
    login,
    olmap,
  },
};
</script>

<style>
@import url("assets/css/base.css");
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100%;
}
</style>