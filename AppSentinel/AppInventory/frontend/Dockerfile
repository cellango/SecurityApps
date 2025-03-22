FROM node:18.19-alpine3.18 as builder

WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./

# Install dependencies with additional flags
RUN npm install --legacy-peer-deps --no-optional --ignore-scripts && \
    npm install -D @babel/plugin-proposal-private-property-in-object@7.21.11

# Copy the entire source code
COPY . .

# Ensure the assets directory exists
RUN mkdir -p src/assets

# Build the app
ENV NODE_ENV=production
ENV GENERATE_SOURCEMAP=false
RUN npm run build

# Production stage
FROM node:18.19-alpine3.18

WORKDIR /app

# Install serve
RUN npm install -g serve@14.2.1

# Copy built files
COPY --from=builder /app/build ./build

# Create a simple serve configuration with proper routing
RUN echo '{"rewrites":[{"source":"/api/**","destination":"http://backend:5000/api/:splat"},{"source":"/**","destination":"/index.html"}]}' > /app/build/serve.json

EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]
