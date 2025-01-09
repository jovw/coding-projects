const express = require('express');
const googleAuthRoutes = express.Router();
const authService = require('../services/authService');

googleAuthRoutes.get('/login', authService.handleLogin);              // ../auth/google/login
googleAuthRoutes.get('/oauth', authService.handleOAuth);              // ../auth/google/oauth 
googleAuthRoutes.get('/logout', authService.handleLogout);             // ../auth/google/logout
googleAuthRoutes.get('/callback', authService.handleOAuth);

module.exports = googleAuthRoutes;
