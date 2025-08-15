# React Frontend Dockerfile
# 
# Author: Eon (Himanshu Shekhar)
# Email: eonhimanshu@gmail.com
# 
# Docker configuration for the React TypeScript Frontend

FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "start"] 