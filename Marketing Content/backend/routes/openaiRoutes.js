const express = require('express');
const openaiRoutes = express.Router();
const authService = require('../services/authService')
const openaiAssistantService = require('../services/api/openaiAssistantService.js');
const contentService = require('../services/contentService.js');

// Apply the authentication middleware globally to all routes in this router
openaiRoutes.use(authService.handleAuthenticateToken)

// Define routes for getting post, generating, and saving post
openaiRoutes.post('/contents/disperse', contentService.disperseContentInfo);

module.exports = openaiRoutes;