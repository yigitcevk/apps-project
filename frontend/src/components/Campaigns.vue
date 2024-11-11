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
        <tr v-for="campaign in campaigns" :key="campaign.id">
          <td>{{ campaign.id }}</td>
          <td>{{ campaign.title }}</td>
          <td>{{ campaign.active ? "Active" : "Not Active" }}</td>
          <td>{{ new Date(campaign.created_at).toLocaleString() }}</td>
          <td>
            <button class="edit-button" @click="openPopup(campaign)">Edit</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-if="showPopup" class="popup-overlay">
      <div class="popup-content">
        <button class="close-button" @click="closePopup">×</button>
        <h2>Edit Campaign {{ currentCampaign.title }}</h2>
                <div>
          <h3>Assign Assets</h3>
          <select v-model="selectedAsset" class="dropdown">
            <option disabled value="">Select Asset</option>
            <option v-for="asset in assets" :key="asset.id" :value="asset.id">{{ asset.title }}</option>
          </select>
          <button class="assign-button" @click="assignAsset">Assign Selected Asset</button>
        </div>
        <div>
          <h3>Campaign Creatives</h3>
          <table class="creatives-table">
            <thead>
              <tr>
                <th><input type="checkbox" @change="toggleSelectAll" /></th>
                <th>ID</th>
                <th>Asset ID</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="creative in campaignCreatives" :key="creative.id">
                <td><input type="checkbox" v-model="selectedCreatives" :value="creative.id" /></td>
                <td>{{ creative.id }}</td>
                <td>{{ creative.asset_id }}</td>
                <td>{{ creative.status }}</td>
              </tr>
            </tbody>
          </table>
          <button class="unassign-button" @click="unassignSelectedCreatives">Unassign Selected Creatives</button>
        </div>
        <div>
          <h3>Campaign Status</h3>
          <select v-model="currentCampaign.active" class="dropdown">
            <option :value="true">Active</option>
            <option :value="false">Not Active</option>
          </select>
        </div>

        <button class="submit-button" @click="submitChanges">Submit</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      campaigns: [],
      assets: [],
      campaignCreatives: [],
      currentCampaign: null,
      selectedAsset: "",
      selectedCreatives: [],
      showPopup: false,
    };
  },
  async mounted() {
    await this.fetchCampaigns();
    await this.fetchAssets();
  },
  methods: {
    async fetchCampaigns() {
      const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
      const token = "2906bad1fa1ee07630bf4029750872eda6a5c0e3b118cf5a";
      try {
        const response = await fetch(`${apiUrl}/proxy/campaigns`, {
          method: "GET",
          headers: { Authorization: `Bearer ${token}` },
        });
        if (response.ok) {
          this.campaigns = await response.json();
        } else {
          console.error("Failed to fetch campaigns");
        }
      } catch (error) {
        console.error(error);
      }
    },
    async fetchAssets() {
      const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
      const token = "2906bad1fa1ee07630bf4029750872eda6a5c0e3b118cf5a";
      try {
        const response = await fetch(`${apiUrl}/proxy/assets`, {
          method: "GET",
          headers: { Authorization: `Bearer ${token}` },
        });
        if (response.ok) {
          this.assets = await response.json();
        } else {
          console.error("Failed to fetch assets");
        }
      } catch (error) {
        console.error(error);
      }
    },
    async fetchCampaignCreatives(campaignId) {
      const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
      const token = "2906bad1fa1ee07630bf4029750872eda6a5c0e3b118cf5a";
      try {
        const response = await fetch(`${apiUrl}/proxy/campaign_creatives?campaign_id=${campaignId}`, {
          method: "GET",
          headers: { Authorization: `Bearer ${token}` },
        });
        if (response.ok) {
          this.campaignCreatives = await response.json();
        } else {
          console.error("Failed to fetch campaign creatives");
        }
      } catch (error) {
        console.error(error);
      }
    },
    openPopup(campaign) {
      this.currentCampaign = { ...campaign };
      this.fetchCampaignCreatives(campaign.id);
      this.showPopup = true;
    },
    closePopup() {
      this.showPopup = false;
      this.currentCampaign = null;
      this.selectedAsset = "";
      this.campaignCreatives = [];
      this.selectedCreatives = [];
    },
    async assignAsset() {
      if (!this.selectedAsset) {
        alert("Please select an asset.");
        return;
      }
      const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
      const token = "2906bad1fa1ee07630bf4029750872eda6a5c0e3b118cf5a";
      
      try {
        const response = await fetch(`${apiUrl}/proxy/campaign_creatives`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            campaign_id: this.currentCampaign.id,
            asset_id: this.selectedAsset,
            status: "Pending",
          }),
        });
        
        if (response.ok) {
          await this.fetchCampaignCreatives(this.currentCampaign.id);
          this.selectedAsset = "";
        } else {
          console.error("Failed to assign asset");
        }
      } catch (error) {
        console.error(error);
      }
    },
    async unassignSelectedCreatives() {
      const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
      const token = "2906bad1fa1ee07630bf4029750872eda6a5c0e3b118cf5a";
      try {
        for (const creativeId of this.selectedCreatives) {
          await fetch(`${apiUrl}/proxy/campaign_creatives/${creativeId}`, {
            method: "DELETE",
            headers: { Authorization: `Bearer ${token}` },
          });
        }
        await this.fetchCampaignCreatives(this.currentCampaign.id);
        this.selectedCreatives = [];
      } catch (error) {
        console.error(error);
      }
    },
    async submitChanges() {
      const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
      const token = "2906bad1fa1ee07630bf4029750872eda6a5c0e3b118cf5a";
      console.log(this.currentCampaign.active);
      
      try {
        const response = await fetch(`${apiUrl}/proxy/campaigns/${this.currentCampaign.id}/status`, {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ 
            campaign_id: this.currentCampaign.id, 
            active: this.currentCampaign.active }),
        });
        if (response.ok) {
          await this.fetchCampaigns();
          this.closePopup();
        } else {
          console.error("Failed to update campaign");
        }
      } catch (error) {
        console.error(error);
      }
    },
    toggleSelectAll(event) {
      if (event.target.checked) {
        this.selectedCreatives = this.campaignCreatives.map((creative) => creative.id);
      } else {
        this.selectedCreatives = [];
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
  background-color: #4caf50;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.edit-button:hover {
  background-color: #45a049;
}

.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.popup-content {
  background: #2c2c2c;
  padding: 20px;
  border-radius: 10px;
  width: 600px;
  max-width: 90%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.popup-content h2,
.popup-content h3 {
  color: #fff;
}

.close-button {
  background: #e74c3c;
  border: none;
  font-size: 24px;
  color: #fff;
  position:absolute;
  top: 25%;
  right: 35%;
  cursor: pointer;
}

.close-button:hover {
  color: #e74c3c;
}

.dropdown {
  padding: 8px;
  font-size: 14px;
  margin-right: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #fff;
  color: black;
}

.assign-button {
  padding: 8px 16px;
  font-size: 14px;
  background-color: #4caf50;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.assign-button:hover {
  background-color: #45a049;
}

.creatives-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.creatives-table th,
.creatives-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
  color: #fff;
}

.creatives-table th {
  background-color: #555;
}

.creatives-table tr:nth-child(even) {
  background-color: #333;
}

.creatives-table tr:hover {
  background-color: #444;
}

.unassign-button {
  padding: 8px 16px;
  font-size: 14px;
  background-color: #e74c3c;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 10px;
}

.unassign-button:hover {
  background-color: #c0392b;
}

.dropdown {
  padding: 8px;
  font-size: 14px;
  margin-top: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #fff;
  color: black;
}

.submit-button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #4caf50;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  display: block;
  margin: 20px auto 0;
}

.submit-button:hover {
  background-color: #45a049;
}
</style>
