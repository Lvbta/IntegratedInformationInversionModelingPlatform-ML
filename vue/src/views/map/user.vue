<template>
  <div class="user">
    <span class="mdi mdi-account"></span>
  </div>
</template>

<script>
export default {
  name: "user",
};
</script>

<style>
.user {
  position: absolute;
  top: 140px;
  right: 20px;
  /* width: 50px;
  height: 50px; */
  z-index: 3;
}
.user span {
  display: inline-block;
  width: 50px;
  height: 50px;
  border: 1px solid #cecece;
  border-radius: 25px;
  color: rgb(161, 197, 233);
  line-height: 50px;
  background-color: rgb(15, 58, 101);
  text-align: center;
}
</style>