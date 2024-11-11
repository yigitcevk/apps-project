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
          <th>Created At</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="insight in insights" :key="insight.id">
          <td>{{ insight.id }}</td>
          <td>{{ insight.campaign_creative_id }}</td>
          <td>{{ insight.impressions }}</td>
          <td>{{ insight.cpi }}</td>
          <td>{{ insight.ctr }}</td>
          <td>{{ insight.cpm }}</td>
          <td>{{ insight.ipm }}</td>
          <td>{{ new Date(insight.created_at).toLocaleString() }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      insights: [],
      intervalId: null,
    };
  },
  async mounted() {
    await this.fetchInsights();

    // Background updates
    this.intervalId = setInterval(async () => {
      console.log("Fetching latest insights...");
      await this.fetchInsights();
    }, 60000); // 1 minute
  },
  beforeUnmount() {
    if (this.intervalId) clearInterval(this.intervalId);
  },
  methods: {
    async fetchInsights() {
      const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
      const token = "2906bad1fa1ee07630bf4029750872eda6a5c0e3b118cf5a";
      try {
        const response = await fetch(`${apiUrl}/proxy/insights/all`, {
          method: "GET",
          headers: { Authorization: `Bearer ${token}` },
        });
        if (response.ok) {
          this.insights = await response.json();
        } else {
          console.error("Failed to fetch insights");
        }
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
</style>
