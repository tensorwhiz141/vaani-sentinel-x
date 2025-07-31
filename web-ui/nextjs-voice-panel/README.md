# Vaani Sentinel-X Backend

Node.js/Express.js backend server for the Vaani Sentinel-X multilingual content generation system.

## Features

- 🔐 JWT Authentication
- 🛡️ Security headers and rate limiting
- 🌐 CORS enabled for frontend integration
- 📁 Static file serving for generated content
- 📊 RESTful API endpoints for all system data
- 🚀 Production-ready with proper error handling

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `GET /api/auth/verify` - Verify JWT token

### Content Management
- `GET /api/content/structured` - Get structured content blocks
- `GET /api/content/ready/:language` - Get content ready for specific language
- `GET /api/translation-previews` - Get translation previews

### Multilingual Data
- `GET /api/translated-content` - Get AI-translated content with confidence scores
- `GET /api/personalized-content` - Get user-personalized content
- `GET /api/tts-simulation` - Get TTS voice assignments and quality metrics
- `GET /api/strategy-recommendations` - Get weekly performance-based strategies

### Analytics
- `GET /api/analytics/metrics` - Get post engagement metrics
- `GET /api/analytics/suggestions` - Get strategy suggestions

### System
- `GET /health` - Health check endpoint
- `GET /api/system/status` - System status and diagnostics
- `GET /api/scheduled-posts` - Get all scheduled posts

## Setup

### Prerequisites
- Node.js 16+ 
- npm 8+

### Installation

1. Navigate to the backend directory:
```bash
cd web-ui/nextjs-voice-panel
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment variables:
```bash
cp .env .env.local
# Edit .env.local with your actual values
```

4. Start the server:
```bash
# Development
npm run dev

# Production
npm start
```

The server will start on `http://localhost:5000`

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `5000` |
| `NODE_ENV` | Environment | `development` |
| `JWT_SECRET` | JWT signing secret | Required |
| `FRONTEND_URL` | Frontend URL for CORS | `http://localhost:3000` |
| `SECRET_KEY` | General secret key | Required |

## Authentication

Default test credentials:
- Email: `test@vaani.com`
- Password: `password123`

## File Structure

```
web-ui/nextjs-voice-panel/
├── server.js          # Main server file
├── package.json       # Dependencies and scripts
├── .env              # Environment variables template
└── README.md         # This file
```

## Deployment

This backend is configured for deployment on Render.com and other cloud platforms.

### Render Deployment

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set build command: `npm install`
4. Set start command: `npm start`
5. Add environment variables in Render dashboard

## Security Features

- Helmet.js for security headers
- Rate limiting (100 requests per 15 minutes)
- JWT token authentication
- CORS protection
- Input validation and sanitization
- Graceful error handling

## Development

### Adding New Endpoints

1. Add route handler in `server.js`
2. Use `authenticateToken` middleware for protected routes
3. Follow existing error handling patterns
4. Update this README with new endpoint documentation

### Testing

```bash
# Test health endpoint
curl http://localhost:5000/health

# Test login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@vaani.com","password":"password123"}'

# Test protected endpoint (replace TOKEN with actual JWT)
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:5000/api/system/status
```

## Troubleshooting

### Common Issues

1. **Port already in use**: Change PORT in .env file
2. **CORS errors**: Update FRONTEND_URL in .env file
3. **File not found errors**: Ensure Python backend has generated content files
4. **JWT errors**: Check JWT_SECRET is set and consistent

### Logs

The server uses Morgan for HTTP request logging. Check console output for detailed request/response information.

## License

MIT License - see main project LICENSE file.
