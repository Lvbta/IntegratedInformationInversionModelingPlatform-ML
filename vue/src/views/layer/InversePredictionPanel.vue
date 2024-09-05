<template>
  <div>
    <!-- 主按钮 -->
    <el-button type="primary" @click="togglePanel">
      反演预测出图
    </el-button>

    <!-- 侧边面板 -->
    <el-drawer
      :visible.sync="drawerVisible"
      size="50%"
      direction="rtl"
      title="反演预测出图"
    >
      <el-form :model="form" label-width="120px">
        <!-- 上传 TIF 数据 -->
        <el-form-item label="TIF 数据上传">
          <el-upload
            class="upload-demo"
            drag
            action="#"
            :on-change="handleTifChange"
            :before-upload="beforeTifUpload"
            :auto-upload="false"
          >
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">拖拽文件到此处，或<em>点击上传</em></div>
          </el-upload>
        </el-form-item>

        <!-- 模型权重选择 -->
        <el-form-item label="模型权重选择">
          <el-select v-model="form.modelWeight" placeholder="请选择模型权重">
            <el-option
              v-for="item in modelWeights"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>

        <!-- 执行预测 -->
        <el-form-item>
          <el-button type="primary" @click="executePrediction">执行预测</el-button>
        </el-form-item>
      </el-form>
    </el-drawer>
  </div>
</template>

<script>
export default {
  name: 'InversePredictionPanel',
  data() {
    return {
      drawerVisible: True,
      form: {
        tifFile: null,
        modelWeight: ''
      },
      modelWeights: [
        { label: '模型1', value: 'model1' },
        { label: '模型2', value: 'model2' },
        // 添加更多模型权重选项
      ]
    };
  },
  methods: {
    togglePanel() {
      this.drawerVisible = !this.drawerVisible;
    },
    handleTifChange(file) {
      this.form.tifFile = file.raw;
    },
    beforeTifUpload(file) {
      // 可以添加自定义上传前的逻辑
      return true;
    },
    executePrediction() {
      if (!this.form.tifFile || !this.form.modelWeight) {
        this.$message.error('请上传TIF数据并选择模型权重');
        return;
      }
      
      // 执行预测的逻辑
      // 这里假设你有一个 API 可以发送文件和模型权重
      // 你可以用 Axios 或其他 HTTP 库来发送请求
      // 例如：
      // axios.post('/api/predict', {
      //   tifFile: this.form.tifFile,
      //   modelWeight: this.form.modelWeight
      // }).then(response => {
      //   console.log('预测结果:', response.data);
      // }).catch(error => {
      //   console.error('预测失败:', error);
      // });

      this.$message.success('预测执行完成');
    }
  }
};
</script>

<style scoped>
.upload-demo i {
  font-size: 28px;
  color: #409EFF;
}
.upload-demo .el-upload__text {
  color: #409EFF;
}
</style>
