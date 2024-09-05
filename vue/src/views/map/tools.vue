<template>
  <div class="toolbar">
    <ul class="define_ul">
      <li>
        <i
          class="mdi mdi-home"
          @click="mapTools('gohome')"
          title="Home"
        ></i>
      </li>
      <li>
        <i
          class="mdi mdi-minus"
          @click="mapTools('zoomin')"
          title="缩小"
        ></i>
      </li>
      <li>
        <i
          class="mdi mdi-plus"
          @click="mapTools('zoomout')"
          title="放大"
        ></i>
      </li>
      <li>
        <i
          class="mdi mdi-ruler"
          @click="mapTools('celiang')"
          title="测量"
        ></i>
      </li>
      <li>
        <i
          class="mdi mdi-delete"
          @click="mapTools('clearDrawings')"
          title="清除"
        ></i>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "tools",
  methods: {
    mapTools(targetment) {
      this.$emit("mapTools", targetment);
    },
  },
};
</script>

<style>
.define_ul {
  padding: 0;
  margin: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  align-items: center;
}

li {
  padding: 6px 0;
  text-align: center;
}

.toolbar {
  position: absolute;
  height: 165px;
  right: 20px;
  bottom: 120px;
  width: 30px;
  background-color: #fff;
  border: 1px solid #cecece;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  z-index: 2;
}

.toolbar ul li {
  width: 100%;
  border-bottom: 1px solid #cecece;
  cursor: pointer;
}

.toolbar ul li:last-child {
  border: none;
}

.iconfont {
  font-size: 24px;
  display: block;
  width: 100%;
  text-align: center;
}

.iconfont:hover {
  background-color: #f0f0f0;
}
</style>
