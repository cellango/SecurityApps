# Database Management Guide

## Database Seeding

The AppSentinel platform provides two methods for seeding the database with test data.

### Using Make Command

The simplest way to seed the database is using the provided make command:

```bash
make seed
```

This command will:
1. Connect to the database container
2. Run the seeding script to populate test data
3. Provide feedback on the seeding process

Note: The seed command will fail if the database already contains data. This is a safety measure to prevent accidental data loss. If you need to reseed:
1. Clear the database first
2. Then run the seed command again

### Via REST API

You can also trigger database seeding through the REST API. This is useful for:
- Setting up test environments
- Initializing new deployments

#### API Endpoint

```
POST /api/admin/seed
```

#### Authentication
- Requires a valid JWT token
- User must have admin privileges

#### Example Request

```bash
curl -X POST \
  http://localhost:5000/api/admin/seed \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN' \
  -H 'Content-Type: application/json'
```

#### Response

Success (200):
```json
{
    "message": "Database seeded successfully"
}
```

Error (403 - Unauthorized):
```json
{
    "error": "Admin privileges required"
}
```

Error (400 - Database Already Seeded):
```json
{
    "error": "Database already contains data. Clear the database first if you want to reseed."
}
```

Error (500 - Server Error):
```json
{
    "error": "Failed to seed database: [error details]"
}
```

### Seed Data Contents

The seeding process creates:
1. Default teams (Security, Development, Operations, Compliance)
2. Sample applications with various risk profiles
3. Default risk parameters
4. Initial ML model versions (if applicable)

### Important Notes

1. Seeding will fail if the database already contains data
2. Only use seeding in development or testing environments
3. For production environments, use proper data migration strategies
4. Seeding is not automatic - it must be explicitly requested either via the make command or REST API
5. To reseed, you must first clear the database
