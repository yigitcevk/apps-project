<template>
  <div class="page-container">
    <button class="navigation-button" @click="navigateTo('/dashboard')">Return to Dashboard</button>
    <h1 class="page-title">Assets</h1>
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
    const token = "2906bad1fa1ee07630bf4029750872eda6a5c0e3b118cf5a";
    
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    try {
      const response = await fetch(`${apiUrl}/proxy/assets`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`, //localStorage.getItem('token') if token is dynamic
      },
      });
      if (response.status != 200){
        throw new Error(`Status: ${response.status}`);
      }      
      this.data = await response.json();
    } catch (error) {
      console.error("Error fetching assets:", error);
    }
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
  white-space: pre-wrap; /* Satır uzunluğunu korumak için */
}
</style>
