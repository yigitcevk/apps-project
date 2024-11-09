<template>
  <div class="page-container">
    <button class="navigation-button" @click="navigateTo('/dashboard')">Return to Dashboard</button>
    <h1 class="page-title">Insights</h1>
    <ul class="data-list">
      <li v-for="item in data" :key="item.id">
        {{ JSON.stringify(item, null, 2) }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      data: [],
    };
  },
  async mounted() {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const response = await fetch('${apiUrl}/insights');
    this.data = await response.json();
  },
  methods: {
    navigateTo(route) {
      this.$router.push(route);
    },
  },
};
</script>

<style scoped>
.page-container {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
  box-sizing: border-box;
}

.page-title {
  margin-top: 20px;
  font-size: 24px;
  color: #fff;
}

.navigation-button {
  position: absolute;
  top: 20px;
  right: 20px;
  padding: 10px 20px;
  font-size: 16px;
  background-color: #fff;
  color: black;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.navigation-button:hover {
  background-color: #45a049;
}

.data-list {
  list-style-type: none;
  padding: 0;
  margin-top: 20px;
  width: 80%;
}

.data-list li {
  font-size: 16px;
  color: #fff;
  background-color: #333;
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 5px;
  white-space: pre-wrap;
}
</style>
