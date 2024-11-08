<template>
    <div class="dashboard-container">
      <h1 class="dashboard-title">Dashboard</h1>
      <div class="button-container">
        <button class="dashboard-button" @click="navigateTo('/assets')">Assets</button>
        <button class="dashboard-button" @click="navigateTo('/campaigns')">Campaigns</button>
        <button class="dashboard-button" @click="navigateTo('/insights')">Insights</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      navigateTo(route) {
        this.$router.push(route);
      },
    },
  };
  </script>
  
<style scoped>
    .dashboard-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh; /* Full viewport height */
        padding: 0 20px;
        box-sizing: border-box;
        position: relative;
    }
    .dashboard-title {
        position: absolute;
        top: 20px;
        left: 20px;
        font-size: 24px;
        color: #fff;
        margin: 0;
    }
    .button-container {
        display: flex;
        gap: 20px; /* Space between buttons */
    }
    .dashboard-button {
        padding: 15px 30px;
        font-size: 16px;
        cursor: pointer;
        border: none;
        border-radius: 8px;
        background-color: #fff; /* Aesthetic green color */
        color: black;
        transition: all 0.3s ease;
    }
    .dashboard-button:hover {
        background-color: #45a049;
    }

    .dashboard-button:active {
        transform: scale(0.98);
    }
    nav {
        margin-top: 20px;
    }
    button {
        margin-right: 10px;
        padding: 10px 20px;
        cursor: pointer;
    }
</style>
  