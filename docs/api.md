# API Documentation

## Cloud Cost Optimizer API

### Base URL
- Development: http://localhost:8000
- Production: https://your-domain.com

### Authentication
API key required for production use.

### Endpoints

#### Health Check
`GET /api/v1/health`

Returns system health status.

#### Cost Summary  
`GET /api/v1/summary`

Returns current cost summary and optimization score.

#### Indian Pricing
`GET /api/v1/pricing/india`

Returns pricing tiers for Indian market.

### Response Format
All responses are in JSON format with INR currency.
