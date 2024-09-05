<template>
  <el-container>
    <el-aside width="500px !important" :class="{ 'sidebar': true, 'collapsed': isCollapsed }">
      <div v-if="!isCollapsed">
        <div class="data-import-title">
            <h2 class="header-title">综合信息反演建模平台</h2>
        </div>
        <!-- 功能点1: 数据上传与展示 -->
        <div class="section">
          
          <div class="data-import-header">
            <h2>数据导入</h2>
            <h6>支持csv、xls、xlsx格式(UTF-8)</h6>
          </div>
          <el-upload
            class="upload-demo"
            action=""
            :before-upload="handleFileUpload"
            :show-file-list="true"
            :on-change="handleFileUploadChange"
          >
            <el-button class="full-width-button" type="primary">上传文件</el-button>
          </el-upload>
          <el-alert v-if="uploadError" type="error" :description="uploadError" />
          <div v-if="previewData.length">
            <h6>前5行数据</h6>
            <el-table :data="previewData" border>
              <el-table-column
                v-for="(header, index) in tableHeaders"
                :key="index"
                :label="header"
                :prop="header"
              />
            </el-table>
          </div>
        </div>

        <!-- 功能点2: 机器学习回归模型训练 -->
        <div class="section">
          <h2>模型训练</h2>
          <el-form :model="form" ref="form">
            <div class="form-group">
              <el-form-item label="选择模型:" :inline="true">
                <el-select v-model="form.selectedModel" placeholder="请选择模型" @change="handleModelChange">
                  <el-option
                    v-for="model in models"
                    :key="model"
                    :label="model"
                    :value="model"
                  />
                </el-select>
              </el-form-item>
            </div>
            <div class="form-group">
              <el-form-item label="选择数据标准化或归一化算法:" :inline="true">
                <el-select v-model="form.selectProcessMethod" placeholder="选择数据预处理算法">
                  <el-option
                    v-for="processMethod in processMethods"
                    :key="processMethod"
                    :label="processMethod"
                    :value="processMethod"
                  />
                </el-select>
              </el-form-item>
            </div>
            <!-- Only show optimization algorithm selection for certain models -->
            <div v-if="shouldShowOptimization" class="form-group">
              <el-form-item label="选择优化算法:" :inline="true">
                <el-select v-model="form.selectedOptimizationAlgorithm" placeholder="选择优化算法">
                  <el-option label="TPE" value="tpe"></el-option>
                  <el-option label="Random Search" value="random_search"></el-option>
                </el-select>
              </el-form-item>
            </div>

            <div class="form-group">
              <el-form-item label="选择自变量:" :inline="true">
                <el-select
                  v-model="form.selectedIndependentVars"
                  multiple
                  placeholder="请选择自变量"
                >
                  <el-option
                    v-for="field in fields"
                    :key="field"
                    :label="field"
                    :value="field"
                  />
                </el-select>
              </el-form-item>
            </div>

            <div class="form-group">
              <el-form-item label="选择因变量:" :inline="true">
                <el-select v-model="form.selectedDependentVar" placeholder="请选择因变量">
                  <el-option
                    v-for="field in fields"
                    :key="field"
                    :label="field"
                    :value="field"
                  />
                </el-select>
              </el-form-item>
            </div>

            <div class="form-group">
              <el-button class="full-width-button" type="primary" @click="startTraining">开始训练</el-button>
              <el-alert v-if="trainingError" type="error" :description="trainingError" />
            </div>
          </el-form>
        </div>
        <!-- 功能点3: 训练结果展示 -->
        <div v-if="results" class="section">
          <h2>训练结果展示</h2>
          <CustomLineChart :results="results" />
        </div>
      </div>
      <LoadingOverlay :visible="isLoading" />
    </el-aside>
  </el-container>
</template>

<script>
import CustomLineChart from './LineChart.vue';
import LoadingOverlay from './LoadingOverlay.vue';

export default {
  components: {
    CustomLineChart,
    LoadingOverlay,
  },
  data() {
    return {
      isCollapsed: false,
      data: null,
      previewData: [],
      tableHeaders: [],
      form: {
        selectedModel: '',
        selectProcessMethod:'',
        selectedIndependentVars: [],
        selectedDependentVar: '',
      },
      models: ['随机森林', '支持向量机', '线性回归', '梯度提升', 
               '决策树回归', 'K近邻回归', '多层感知器回归', '岭回归',
               '拉索回归', 'LSTM'], 
      processMethods: ['最小最大', 'z-score', '最大绝对值', '鲁棒', 'L2', '对数', '不处理'],
      optimizationAlgorithms: ['tpe', 'random_search'],
      fields: [],
      results: null,
      uploadError: null,
      trainingError: null,
      isLoading: false,
      shouldShowOptimization: false,
    };
  },
  methods: {
    async handleFileUpload(file) {
      if (!file) return;

      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await fetch('http://192.168.1.8:50001/upload', {
          method: 'POST',
          body: formData,
          mode: 'cors' // 显式设置 CORS 模式
        });

        if (!response.ok) {
          throw new Error('文件上传失败，请重试。');
        }

        const result = await response.json();
        this.previewData = result.slice(0, 5);
        this.tableHeaders = Object.keys(result[0] || {});
        this.fields = this.tableHeaders;
        this.data = result; // Save the data for scatter plot
      } catch (error) {
        this.uploadError = error.message;
        console.error('Error uploading file:', error);
      }
    },
    handleFileUploadChange(file, fileList) {
      if (file.status === 'error') {
        this.uploadError = '文件上传失败，请检查文件格式或大小。';
      }
    },
    async startTraining() {
      this.isLoading = true;
      try {
        const isValid = this.validateForm();
        if (!isValid) {
          return;
        }

        const response = await fetch('http://192.168.1.8:50001/optimize_and_train', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            model: this.form.selectedModel,
            processMethod: this.form.selectProcessMethod,
            independentVars: this.form.selectedIndependentVars,
            dependentVar: this.form.selectedDependentVar,
          }),
          mode: 'cors', // 显式设置 CORS 模式
        });

        if (!response.ok) {
          throw new Error('模型训练失败，请重试。');
        }

        const result = await response.json();
        this.results = result;
      } catch (error) {
        this.trainingError = error.message;
        console.error('Error during training:', error);
      }finally {
        this.isLoading = false;
      }
    },
    validateForm() {
      const { selectedModel, selectProcessMethod, selectedIndependentVars, selectedDependentVar } = this.form;
      if (!selectedModel) {
        this.trainingError = '请选择模型。';
        return false;
      }
      if (!selectProcessMethod) {
        this.trainingError = '请选择数据处理方式。';
        return false;
      }
      if (selectedIndependentVars.length === 0) {
        this.trainingError = '请选择至少一个自变量。';
        return false;
      }
      if (!selectedDependentVar) {
        this.trainingError = '请选择因变量。';
        return false;
      }
      return true;
    },
    handleModelChange(model) {
      // List of models that do not require optimization algorithms
      const modelsWithoutOptimization = ['线性回归', '岭回归', '拉索回归'];
      this.shouldShowOptimization = !modelsWithoutOptimization.includes(model);
    },
  },
};
</script>

<style scoped>
.data-import-title {
  position: -webkit-sticky; /* For Safari */
  position: sticky;
  top: 0; /* Adjust as needed */
  background-color: #fff; /* Optional: add background color to avoid overlap issues */
  z-index: 100; /* Ensure it stays on top of other content */
  padding: 10px; /* Optional: add padding */
  display: flex;
  flex-direction: column;
  align-items: center; /* Center horizontally */
}

.header-title {
  font-size: 30px; /* Adjust the font size as needed */
  color: green; /* Set the font color to green */
}

.sidebar {
  padding: 20px !important; /* Add padding for gap */
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  height: 100% !important;
  transition: width 0.3s !important;
  background-color: #f5f5f5 !important;
  border-right: 1px solid #ddd !important;
  z-index: 1000 !important;
  overflow: auto !important;
  width: 300px !important; /* Increase width here */
}

/* Custom scrollbar for WebKit browsers */
.sidebar::-webkit-scrollbar {
  width: 4px; /* Width of the scrollbar */
}

.sidebar::-webkit-scrollbar-track {
  background: #f5f5f5; /* Color of the track */
}

.sidebar::-webkit-scrollbar-thumb {
  background: #888; /* Color of the scrollbar thumb */
  border-radius: 4px; /* Rounded corners for the thumb */
}

.sidebar::-webkit-scrollbar-thumb:hover {
  background: #555; /* Darker color when hovering */
}

/* Custom scrollbar for Firefox */
.sidebar {
  scrollbar-width: thin; /* Make the scrollbar thin */
  scrollbar-color: #888 #f5f5f5; /* Thumb color and track color */
}

.sidebar.collapsed {
  width: 60px !important; /* Adjust for collapsed state */
  padding: 20px 5px !important; /* Reduce padding when collapsed */
}

.section {
  margin-bottom: 20px !important;
}

.upload-demo {
  margin-bottom: 20px !important;
}

.form-group {
  margin-bottom: 15px !important;
  display: flex !important; /* Ensure label and input are in one line */
  align-items: center !important;
}

.el-form-item {
  margin-bottom: 15px !important;
  flex: 1 !important; /* Ensure form item takes available space */
}

.el-select, .el-input, .el-upload, .el-button {
  width: 100% !important; /* Ensure all inputs take available width */
}

.line-chart {
  width: 100% !important; /* Ensure chart takes available width */
}

.el-alert {
  margin-top: 10px !important;
}

.full-width-button {
  width: 460px !important; /* Make buttons full width */
}

</style>
