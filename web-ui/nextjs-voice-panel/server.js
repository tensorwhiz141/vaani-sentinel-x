#!/usr/bin/env node

/**
 * Vaani Sentinel-X Backend Server
 * Express.js server for the multilingual content generation system
 * 
 * Features:
 * - JWT Authentication
 * - CORS enabled
 * - Rate limiting
 * - Security headers
 * - API endpoints for content management
 * - File serving for generated content
 * 
 * Author: Vaani Sentinel-X Team
 * Date: 2025-07-31
 */

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const compression = require('compression');
const rateLimit = require('express-rate-limit');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const path = require('path');
const fs = require('fs-extra');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;
const JWT_SECRET = process.env.JWT_SECRET || 'your-jwt-secret-change-in-production';

// Security middleware
app.use(helmet({
  contentSecurityPolicy: false, // Disable CSP for development
  crossOriginEmbedderPolicy: false
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later.'
});
app.use('/api/', limiter);

// CORS configuration
app.use(cors({
  origin: process.env.FRONTEND_URL || ['http://localhost:3000', 'http://localhost:3001'],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// Body parsing middleware
app.use(compression());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Logging
app.use(morgan('combined'));

// Static file serving for generated content
const contentPath = path.join(__dirname, '../../content');
const scheduledPostsPath = path.join(__dirname, '../../scheduled_posts');
const analyticsPath = path.join(__dirname, '../../analytics_db');
const dataPath = path.join(__dirname, '../../data');

app.use('/content', express.static(contentPath));
app.use('/scheduled-posts', express.static(scheduledPostsPath));
app.use('/analytics', express.static(analyticsPath));
app.use('/data', express.static(dataPath));

// Test user credentials (in production, use a proper database)
const TEST_USER = {
  email: 'test@vaani.com',
  password: '$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', // password123
  id: 1,
  name: 'Test User'
};

// JWT middleware
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) {
      return res.status(403).json({ error: 'Invalid or expired token' });
    }
    req.user = user;
    next();
  });
};

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ 
    status: 'OK', 
    timestamp: new Date().toISOString(),
    service: 'Vaani Sentinel-X Backend',
    version: '1.0.0'
  });
});

// Authentication endpoints
app.post('/api/auth/login', async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: 'Email and password are required' });
    }

    // Check credentials
    if (email !== TEST_USER.email) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    const isValidPassword = await bcrypt.compare(password, TEST_USER.password);
    if (!isValidPassword) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Generate JWT token
    const token = jwt.sign(
      { id: TEST_USER.id, email: TEST_USER.email, name: TEST_USER.name },
      JWT_SECRET,
      { expiresIn: '24h' }
    );

    res.json({
      message: 'Login successful',
      token,
      user: {
        id: TEST_USER.id,
        email: TEST_USER.email,
        name: TEST_USER.name
      }
    });
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Verify token endpoint
app.get('/api/auth/verify', authenticateToken, (req, res) => {
  res.json({ 
    valid: true, 
    user: req.user 
  });
});

// Helper function to safely read JSON files
const readJsonFile = async (filePath) => {
  try {
    if (await fs.pathExists(filePath)) {
      const data = await fs.readJson(filePath);
      return data;
    }
    return null;
  } catch (error) {
    console.error(`Error reading ${filePath}:`, error);
    return null;
  }
};

// Helper function to get all files in a directory
const getDirectoryFiles = async (dirPath) => {
  try {
    if (await fs.pathExists(dirPath)) {
      const files = await fs.readdir(dirPath);
      return files.filter(file => file.endsWith('.json'));
    }
    return [];
  } catch (error) {
    console.error(`Error reading directory ${dirPath}:`, error);
    return [];
  }
};

// Content API endpoints
app.get('/api/content/structured', authenticateToken, async (req, res) => {
  try {
    const structuredPath = path.join(contentPath, 'structured', 'content_blocks.json');
    const data = await readJsonFile(structuredPath);
    
    if (!data) {
      return res.status(404).json({ error: 'Structured content not found' });
    }
    
    res.json(data);
  } catch (error) {
    console.error('Error fetching structured content:', error);
    res.status(500).json({ error: 'Failed to fetch structured content' });
  }
});

// Translated content endpoint
app.get('/api/translated-content', authenticateToken, async (req, res) => {
  try {
    const translatedPath = path.join(dataPath, 'translated_content.json');
    const data = await readJsonFile(translatedPath);

    if (!data) {
      return res.status(404).json({ error: 'Translated content not found' });
    }

    res.json(data);
  } catch (error) {
    console.error('Error fetching translated content:', error);
    res.status(500).json({ error: 'Failed to fetch translated content' });
  }
});

// Personalized content endpoint
app.get('/api/personalized-content', authenticateToken, async (req, res) => {
  try {
    const personalizedPath = path.join(dataPath, 'personalized_content.json');
    const data = await readJsonFile(personalizedPath);

    if (!data) {
      return res.status(404).json({ error: 'Personalized content not found' });
    }

    res.json(data);
  } catch (error) {
    console.error('Error fetching personalized content:', error);
    res.status(500).json({ error: 'Failed to fetch personalized content' });
  }
});

// TTS simulation endpoint
app.get('/api/tts-simulation', authenticateToken, async (req, res) => {
  try {
    const ttsPath = path.join(dataPath, 'tts_simulation_output.json');
    const data = await readJsonFile(ttsPath);

    if (!data) {
      return res.status(404).json({ error: 'TTS simulation data not found' });
    }

    res.json(data);
  } catch (error) {
    console.error('Error fetching TTS simulation data:', error);
    res.status(500).json({ error: 'Failed to fetch TTS simulation data' });
  }
});

// Strategy recommendations endpoint
app.get('/api/strategy-recommendations', authenticateToken, async (req, res) => {
  try {
    const strategyPath = path.join(dataPath, 'weekly_strategy_recommendation.json');
    const data = await readJsonFile(strategyPath);

    if (!data) {
      return res.status(404).json({ error: 'Strategy recommendations not found' });
    }

    res.json(data);
  } catch (error) {
    console.error('Error fetching strategy recommendations:', error);
    res.status(500).json({ error: 'Failed to fetch strategy recommendations' });
  }
});

// Analytics endpoints
app.get('/api/analytics/metrics', authenticateToken, async (req, res) => {
  try {
    const metricsPath = path.join(analyticsPath, 'post_metrics.json');
    const data = await readJsonFile(metricsPath);

    if (!data) {
      return res.status(404).json({ error: 'Analytics metrics not found' });
    }

    res.json(data);
  } catch (error) {
    console.error('Error fetching analytics metrics:', error);
    res.status(500).json({ error: 'Failed to fetch analytics metrics' });
  }
});

app.get('/api/analytics/suggestions', authenticateToken, async (req, res) => {
  try {
    const suggestionsPath = path.join(analyticsPath, 'strategy_suggestions.json');
    const data = await readJsonFile(suggestionsPath);

    if (!data) {
      return res.status(404).json({ error: 'Strategy suggestions not found' });
    }

    res.json(data);
  } catch (error) {
    console.error('Error fetching strategy suggestions:', error);
    res.status(500).json({ error: 'Failed to fetch strategy suggestions' });
  }
});

// Scheduled posts endpoint
app.get('/api/scheduled-posts', authenticateToken, async (req, res) => {
  try {
    const files = await getDirectoryFiles(scheduledPostsPath);
    const posts = [];

    for (const file of files) {
      const filePath = path.join(scheduledPostsPath, file);
      const data = await readJsonFile(filePath);
      if (data) {
        posts.push({ filename: file, ...data });
      }
    }

    res.json(posts);
  } catch (error) {
    console.error('Error fetching scheduled posts:', error);
    res.status(500).json({ error: 'Failed to fetch scheduled posts' });
  }
});

// Content ready endpoint (by language)
app.get('/api/content/ready/:language', authenticateToken, async (req, res) => {
  try {
    const { language } = req.params;
    const languageDir = path.join(contentPath, 'content_ready', language);

    if (!await fs.pathExists(languageDir)) {
      return res.status(404).json({ error: `Content for language '${language}' not found` });
    }

    const files = await getDirectoryFiles(languageDir);
    const content = [];

    for (const file of files) {
      const filePath = path.join(languageDir, file);
      const data = await readJsonFile(filePath);
      if (data) {
        content.push({ filename: file, ...data });
      }
    }

    res.json(content);
  } catch (error) {
    console.error('Error fetching content ready:', error);
    res.status(500).json({ error: 'Failed to fetch content ready' });
  }
});

// Translation previews endpoint
app.get('/api/translation-previews', authenticateToken, async (req, res) => {
  try {
    const previewsDir = path.join(contentPath, 'translation_previews');
    const files = await getDirectoryFiles(previewsDir);
    const previews = [];

    for (const file of files) {
      const filePath = path.join(previewsDir, file);
      const data = await readJsonFile(filePath);
      if (data) {
        previews.push({ filename: file, ...data });
      }
    }

    res.json(previews);
  } catch (error) {
    console.error('Error fetching translation previews:', error);
    res.status(500).json({ error: 'Failed to fetch translation previews' });
  }
});

// System status endpoint
app.get('/api/system/status', authenticateToken, async (req, res) => {
  try {
    const status = {
      timestamp: new Date().toISOString(),
      service: 'Vaani Sentinel-X Backend',
      version: '1.0.0',
      uptime: process.uptime(),
      memory: process.memoryUsage(),
      directories: {
        content: await fs.pathExists(contentPath),
        scheduledPosts: await fs.pathExists(scheduledPostsPath),
        analytics: await fs.pathExists(analyticsPath),
        data: await fs.pathExists(dataPath)
      }
    };

    res.json(status);
  } catch (error) {
    console.error('Error fetching system status:', error);
    res.status(500).json({ error: 'Failed to fetch system status' });
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong'
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    error: 'Not found',
    message: `Route ${req.originalUrl} not found`
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Vaani Sentinel-X Backend Server running on port ${PORT}`);
  console.log(`📊 Health check: http://localhost:${PORT}/health`);
  console.log(`🔐 Login endpoint: http://localhost:${PORT}/api/auth/login`);
  console.log(`📁 Content served from: ${contentPath}`);
  console.log(`🌍 Environment: ${process.env.NODE_ENV || 'development'}`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('SIGINT received, shutting down gracefully');
  process.exit(0);
});
