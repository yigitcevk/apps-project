<template>
  <div class="page-container">
    <button class="navigation-button" @click="navigateTo('/dashboard')">Return to Dashboard</button>
    <h1 class="page-title">Campaigns</h1>
    <table class="campaigns-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Title</th>
          <th>Active</th>
          <th>Created At</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in data" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.title }}</td>
          <td>{{ item.active ? "Yes" : "No" }}</td>
          <td>{{ new Date(item.created_at).toLocaleString() }}</td>
          <td>
            <button class="edit-button" @click="editCampaign(item.id)">Edit</button>
          </td>
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
    await this.fetchCampaigns();
  },
  methods: {
    async fetchCampaigns() {
      const token = "2906bad1fa1ee07630bf4029750872eda6a5c0e3b118cf5a";
      const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
      try {
        const response = await fetch(`${apiUrl}/proxy/campaigns`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (!response.ok) {
          throw new Error(`Failed to fetch campaigns. Status: ${response.status}`);
        }
        this.data = await response.json();
      } catch (error) {
        console.error("Error fetching campaigns:", error);
      }
    },
    async editCampaign(campaignId) {
      const token = "2906bad1fa1ee07630bf4029750872eda6a5c0e3b118cf5a";
      const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";

      try {
        const response = await fetch(`${apiUrl}/proxy/campaigns/${campaignId}`, {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            active: true, // Örnek olarak aktif durumu değiştiriliyor
          }),
        });

        if (!response.ok) {
          throw new Error(`Failed to edit campaign. Status: ${response.status}`);
        }

        alert("Campaign updated successfully!");
        await this.fetchCampaigns();
      } catch (error) {
        console.error("Error updating campaign:", error);
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

.campaigns-table {
  width: 80%;
  border-collapse: collapse;
  margin-top: 20px;
}

.campaigns-table th,
.campaigns-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
  color: #fff;
}

.campaigns-table th {
  background-color: #555;
}

.campaigns-table tr:nth-child(even) {
  background-color: #333;
}

.campaigns-table tr:hover {
  background-color: #444;
}

.edit-button {
  padding: 5px 10px;
  font-size: 14px;
  background-color: #3498db;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.edit-button:hover {
  background-color: #2980b9;
}
</style>
