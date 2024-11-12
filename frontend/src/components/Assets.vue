<template>
  <div class="page-container">
    <button class="navigation-button" @click="navigateTo('/dashboard')">Return to Dashboard</button>
    <h1 class="page-title">Assets</h1>
    <div class="upload-container">
      <select v-model="selectedFileName" class="upload-dropdown" @change="triggerFileInput">
        <option disabled value="">Select Image</option>
        <option value="upload">Upload from Computer</option>
        <option v-if="selectedFileName && selectedFileName !== 'Select Image'" :value="selectedFileName">
          {{ selectedFileName }}
        </option>
      </select>
      <input type="file" ref="fileInput" class="upload-input" @change="handleFileChange" />
      <button class="upload-button" @click="uploadAsset">Upload</button>
    </div>
    <table class="assets-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Title</th>
          <th>Status</th>
          <th>Created At</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in data" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.title }}</td>
          <td>{{ item.status }}</td>
          <td>{{ new Date(item.created_at).toLocaleString() }}</td>
          <td>
            <button class="delete-button" @click="deleteAsset(item.id)">Delete</button>
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
      selectedFile: null,
      selectedFileName: "Select Image",
      intervalId: null,
    };
  },
  async mounted() {
    await this.fetchAssets();

    this.intervalId = setInterval(async () => {
      console.log("Refreshing asset statuses...");
      await this.fetchAssets();
    }, 60000); // 1 minute

  },
  beforeUnmount() {
    // Clear the interval to avoid memory leaks
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  },
  methods: {
    async fetchAssets() {
      const token = "2906bad1fa1ee07630bf4029750872eda6a5c0e3b118cf5a";
      const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
      console.log(apiUrl);
      
      try {
        const response = await fetch(`${apiUrl}/asset/all`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (!response.ok) {
          throw new Error(`Failed to fetch assets. Status: ${response.status}`);
        }
        this.data = await response.json();
      } catch (error) {
        console.error("Error fetching assets:", error);
      }
    },
    triggerFileInput(event) {
      if (event.target.value === "upload") {
        this.$refs.fileInput.click();
      }
    },
    handleFileChange(event) {
      this.selectedFile = event.target.files[0];
      this.selectedFileName = this.selectedFile ? this.selectedFile.name : "Select Image";
    },
    async uploadAsset() {
      if (!this.selectedFile) {
        alert("Please select a file to upload.");
        return;
      }

      const token = "2906bad1fa1ee07630bf4029750872eda6a5c0e3b118cf5a";
      const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";

      const formData = new FormData();
      formData.append("file", this.selectedFile);

      try {
        const response = await fetch(`${apiUrl}/asset/create`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        });

        if (!response.ok) {
          throw new Error(`Failed to upload asset. Status: ${response.status}`);
        }

        alert("Asset uploaded successfully!");
        this.selectedFile = null;
        this.selectedFileName = "Select Image";
        await this.fetchAssets();
      } catch (error) {
        console.error("Error uploading asset:", error);
      }
    },
    async deleteAsset(assetId) {
      const token = "2906bad1fa1ee07630bf4029750872eda6a5c0e3b118cf5a";
      const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";

      try {
        const response = await fetch(`${apiUrl}/asset/${assetId}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error(`Failed to delete asset. Status: ${response.status}`);
        }

        alert("Asset deleted successfully!");
        await this.fetchAssets();
      } catch (error) {
        console.error("Error deleting asset:", error);
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

.upload-container {
  display: flex;
  justify-content: flex-end;
  width: 100%;
  margin-bottom: 20px;
}

.upload-dropdown {
  padding: 8px;
  font-size: 16px;
  margin-right: 10px;
  color: #000; 
  background-color: #fff;
}

.upload-input {
  display: none;
}

.upload-button {
  padding: 8px 16px;
  font-size: 16px;
  background-color: #4caf50;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.upload-button:hover {
  background-color: #45a049;
}

.assets-table {
  width: 80%;
  border-collapse: collapse;
  margin-top: 20px;
}

.assets-table th,
.assets-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
  color: #fff;
}

.assets-table th {
  background-color: #555;
}

.assets-table tr:nth-child(even) {
  background-color: #333;
}

.assets-table tr:hover {
  background-color: #444;
}

.delete-button {
  padding: 5px 10px;
  font-size: 14px;
  background-color: #e74c3c;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.delete-button:hover {
  background-color: #c0392b;
}
</style>
