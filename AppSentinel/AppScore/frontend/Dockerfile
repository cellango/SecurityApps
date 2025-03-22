# Build stage
FROM node:14 as build

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PORT=3001
ENV REACT_APP_API_URL=http://localhost:5001

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy build files from build stage
COPY --from=build /app/build /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 3001

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
