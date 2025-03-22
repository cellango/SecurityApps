# Developer Guide

This guide will help you get started with developing the AppInventory frontend application.

## Prerequisites

- Docker
- Make
- Git

## Quick Start

1. Clone the repository
2. Navigate to the frontend directory
3. Start the development server:
```bash
make dev
```

The application will be available at `http://localhost:3000`.

## Development Environment

### Available Commands

All development commands are available through Make:

```bash
# Start development server with hot reloading
make dev

# Start in detached mode (background)
make dev-detach

# View logs
make logs

# Restart development server
make restart

# Clean up everything (containers, images, node_modules)
make clean

# Run tests
make test

# Run linting
make lint

# Run type checking
make type-check

# Format code
make format

# Show all available commands
make help
```

### Development Workflow

1. Start the development server:
```bash
make dev
```

2. Make your changes - the application will automatically reload

3. Before committing:
   - Run tests: `make test`
   - Run linting: `make lint`
   - Run type checking: `make type-check`
   - Format code: `make format`

### Docker Development Setup

The development environment uses Docker Compose with the following features:
- Hot reloading enabled
- Volume mounts for local development
- Node modules cached in container
- TypeScript type checking
- ESLint with caching
- Prettier for code formatting

## Production Build

### Building for Production

```bash
# Build production image
make prod

# Build and run production image
make prod-run
```

The production build includes:
- Multi-stage Docker build
- Minimized bundle size
- No source maps
- Production-only dependencies
- Optimized performance

### Production Optimizations

- Cached npm dependencies
- Reduced Docker image size
- Production-only Node modules
- Optimized bundle size
- Disabled source maps

## Project Structure

```
frontend/
├── src/                    # Source code
│   ├── components/        # React components
│   ├── contexts/          # React contexts
│   ├── services/          # API services
│   ├── types/            # TypeScript types
│   ├── utils/            # Utility functions
│   └── theme.ts          # MUI theme configuration
├── public/                # Static files
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose for development
├── .dockerignore         # Docker ignore file
├── package.json          # NPM package configuration
├── tsconfig.json         # TypeScript configuration
├── .eslintrc.js         # ESLint configuration
├── .prettierrc          # Prettier configuration
└── Makefile             # Development commands
```

## Testing

### Running Tests

```bash
# Run all tests
make test

# Run tests in watch mode (in container)
docker-compose run --rm frontend npm run test
```

### Test Structure

- Tests are located next to the components they test
- Use React Testing Library for component tests
- Jest for unit tests
- Coverage reports available with `npm run test -- --coverage`

## Code Style

### Formatting

The project uses:
- ESLint for code linting
- Prettier for code formatting
- TypeScript for type checking

Format your code before committing:
```bash
make format
```

### Style Guide

- Use functional components with hooks
- Use TypeScript for all files
- Follow Material-UI best practices
- Use named exports for components
- Keep components small and focused
- Use proper TypeScript types

## Troubleshooting

### Common Issues

1. **Hot Reloading Not Working**
   ```bash
   make restart
   ```

2. **Type Errors**
   ```bash
   make type-check
   ```

3. **Container Issues**
   ```bash
   make clean
   make dev
   ```

4. **Node Modules Issues**
   ```bash
   make clean
   make dev
   ```

### Getting Help

1. Check the logs:
   ```bash
   make logs
   ```

2. Clean and rebuild:
   ```bash
   make clean
   make dev
   ```

## Contributing

1. Create a new branch
2. Make your changes
3. Run tests and linting
4. Submit a pull request

## License

[Add your license information here]
