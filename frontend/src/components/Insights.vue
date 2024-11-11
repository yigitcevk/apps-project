<template>
  <div class="page-container">
    <button class="navigation-button" @click="navigateTo('/dashboard')">Return to Dashboard</button>
    <h1 class="page-title">Insights</h1>
    <table class="insights-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Creative ID</th>
          <th>Impressions</th>
          <th>CPI</th>
          <th>CTR</th>
          <th>CPM</th>
          <th>IPM</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in data" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.campaign_creative_id }}</td>
          <td>{{ item.impressions }}</td>
          <td>{{ item.cpi }}</td>
          <td>{{ item.ctr }}</td>
          <td>{{ item.cpm }}</td>
          <td>{{ item.ipm }}</td>
        </tr>
      </tbody>
    </table>
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
    await this.fetchInsights();
  },
  methods: {
    async fetchInsights() {
      const token = "2906bad1fa1ee07630bf4029750872eda6a5c0e3b118cf5a";
      const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
      try {
        const response = await fetch(`${apiUrl}/proxy/insights`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (!response.ok) {
          throw new Error(`Failed to fetch insights. Status: ${response.status}`);
        }
        this.data = await response.json();
      } catch (error) {
        console.error("Error fetching insights:", error);
      }
    },
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

.insights-table {
  width: 80%;
  border-collapse: collapse;
  margin-top: 20px;
}

.insights-table th,
.insights-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
  color: #fff;
}

.insights-table th {
  background-color: #555;
}

.insights-table tr:nth-child(even) {
  background-color: #333;
}

.insights-table tr:hover {
  background-color: #444;
}
</style>
