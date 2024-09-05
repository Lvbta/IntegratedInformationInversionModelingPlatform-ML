<template>
  <div>
    <nav class="navbar">
      <div class="navbar-title">水质大气反演平台</div>
      <ul class="nav-list">
        <li @click="navigate('DataProcessing')">数据导入</li>
        <li @click="navigate('ModelTraining')">模型训练</li>
        <li @click="navigate('ModelManagement')">模型管理</li>
        <li @click="navigate('Prediction')">反演分析</li>
      </ul>
    </nav>
    <component :is="currentView"></component>
    
    <component :is="currentSubView"></component>
  </div>
</template>

<script>
import DataProcessing from './DataProcessing.vue';
import ModelTraining from './ModelTraining.vue';
import ModelManagement from './ModelManagement.vue';
import Prediction from './Prediction.vue';
import DataImport from '../data/DataImport.vue';
import DataVisualization from '../data/DataVisualization.vue';
import CorrelationAnalysis from '../data/CorrelationAnalysis.vue';

export default {
  components: {
    DataProcessing,
    ModelTraining,
    ModelManagement,
    Prediction,
    DataImport,
    DataVisualization,
    CorrelationAnalysis
  },
  data() {
    return {
      currentView: 'DataProcessing',
      currentSubView: null
    };
  },
  methods: {
    navigate(view) {
      this.currentView = view;
      this.currentSubView = null; // Reset the subview
    },
    navigateSubmenu(view) {
      this.currentSubView = view;
    }
  }
};
</script>

<style>
.navbar {
  background-color: #333;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
}
.navbar-title {
  color: #f2f2f2;
  font-size: 20px;
  font-weight: bold;
}
.nav-list {
  list-style-type: none;
  margin: 0;
  padding: 0;
  display: flex;
  gap: 20px;
}
.nav-list li {
  color: #f2f2f2;
  text-align: center;
  padding: 14px 16px 20px;
  text-decoration: none;
  cursor: pointer;
}
.nav-list li:hover {
  background-color: #ddd;
  color: black;
}
.sub-menu {
  background-color: #f1f1f1;
  padding: 10px;
  display: flex;
  justify-content: flex-start;
  margin-top: 10px;
}
.sub-menu button {
  margin-right: 10px;
  padding: 10px;
  border: none;
  cursor: pointer;
}
.sub-menu button:hover {
  background-color: #ddd;
}
</style>