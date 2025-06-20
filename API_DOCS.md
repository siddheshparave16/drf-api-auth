# API Documentation

## Postman Collection

🔗 Click this link to open in Postman:

https://.postman.co/workspace/My-Workspace~5f5a6295-1f39-499f-8fcf-600cb1254adb/collection/45900437-a54f7956-36cf-4ce9-924c-f5f51bc16eb2?action=share&creator=45900437


This link will provide API documentation


📍 API Endpoint Paths
All endpoints are served under:

API Base URL
http://127.0.0.1:8000/api/v1/
For production, replace with your domain: https://yourdomain.com/api/v1/


Core Endpoints:
User Management

POST /telegramuser/create/ - Create new user

GET /telegramuser/ - List all users

PUT/PATCH /telegramuser/update/<id>/ - Update user

DELETE /telegramuser/delete/<id>/ - Remove user

Authentication

POST /api/token-jwt/ - Get JWT tokens

POST /api-token-auth/ - Get DRF token


