# Frontend Dockerfile
FROM node:22

# Set the working directory
WORKDIR /code

# Copy the package.json and package-lock.json files to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy the rest of the application code to the working directory
COPY . .

# Build the Vue.js application for production
RUN npm run build

CMD ["npm", "run", "dev"]
