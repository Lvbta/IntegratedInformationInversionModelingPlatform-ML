<template>
  <div>
    <!-- 表格展示MSE和最佳超参数 -->
    <div v-if="results">
      <h3>精度指标</h3>
      <el-table :data="tableData" border>
        <el-table-column
          prop="key"
          label="指标"
          width="150"
        />
        <el-table-column
          prop="value"
          label="值"
        />
      </el-table>
    </div>

    <!-- Line Chart -->
    <h3>真实值与预测值</h3>
    <canvas id="lineChart"></canvas>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';

// Register the components needed for Chart.js
Chart.register(...registerables);

export default {
  name: 'CustomLineChart',
  props: {
    results: {
      type: Object,
      default: () => ({})
    }
  },
  mounted() {
    this.renderChart();
  },
  methods: {
    renderChart() {
      const ctx = document.getElementById('lineChart').getContext('2d');
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: this.trueData.length ? this.trueData.map((_, i) => i + 1) : [], // Example: label indices
          datasets: [
            {
              label: 'True Data',
              data: this.trueData,
              borderColor: 'rgba(75, 192, 192, 1)',
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              fill: false,
            },
            {
              label: 'Predictions',
              data: this.predictions,
              borderColor: 'rgba(255, 99, 132, 1)',
              backgroundColor: 'rgba(255, 99, 132, 0.2)',
              fill: false,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            x: {
              title: {
                display: true,
                text: '样本序号',
              },
            },
            y: {
              title: {
                display: true,
                text: '值',
              },
            },
          },
        },
      });
    },
  },
  computed: {
    trueData() {
      console.log(this.results)
      return this.results.ture_data || []; // Use results.ture_data from props
    },
    predictions() {
      return this.results.predictions || []; // Use results.predictions from props
    },
    tableData() {
      return [
        { key: 'MSE', value: this.results.mse },
        { key: 'RMSE', value: this.results.rmse },
        { key: 'MAE', value: this.results.mae },
        { key: 'R²', value: this.results.r2 },
        { key: '最佳超参数', value: JSON.stringify(this.results.params) },
      ];
    },
  },
};
</script>

<style scoped>
/* Add styles if needed */
</style>
