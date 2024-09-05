<template>
  <div class="layer-manager">
    <button @click="toggleDropdown" class="layer-manager-button">图层管理</button>
    <div v-if="showDropdown" class="dropdown">
      <button @click="uploadImage">影像上传</button>
      <button @click="publishToGeoServer">发布至GeoServer</button>
      <button @click="loadLayer">加载图层</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LayerManage',
  data() {
    return {
      showDropdown: false
    };
  },
  methods: {
    toggleDropdown() {
      this.showDropdown = !this.showDropdown;
    },
    async uploadImage() {
      try {
        const formData = new FormData();
        formData.append('file', this.$refs.imageFile.files[0]);
        const response = await axios.post('/api/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log('影像上传成功:', response.data);
      } catch (error) {
        console.error('影像上传失败:', error);
      }
    },
    async publishToGeoServer() {
      try {
        const response = await axios.post('/api/publish');
        console.log('发布至GeoServer成功:', response.data);
      } catch (error) {
        console.error('发布至GeoServer失败:', error);
      }
    },
    async loadLayer() {
      try {
        const response = await axios.get('/api/load-layer');
        console.log('加载图层成功:', response.data);
      } catch (error) {
        console.error('加载图层失败:', error);
      }
    }
  }
};
</script>

<style scoped>
.layer-manager {
  position: fixed;
  top: 50px;
  right: 50px;
  z-index:999999999;
}

.layer-manager-button {
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.dropdown {
  position: absolute;
  top: 40px;
  right: 0;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.dropdown button {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: white;
  border: none;
  text-align: left;
  cursor: pointer;
}

.dropdown button:hover {
  background-color: #f8f9fa;
}
</style>
