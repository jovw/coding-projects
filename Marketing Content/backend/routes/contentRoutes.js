const express = require('express');
const contentRoutes = express.Router();
const authService = require('../services/authService')
const contentCollection = require('../services/contentCollection')

// Apply the authentication middleware globally to all routes in this router
contentRoutes.use(authService.handleAuthenticateToken)
//Add the content for a specific user's products on profile page
contentRoutes.post('/users/products/:productId/content', contentCollection.addProductContent);

//GET and display all contents for a specific product by productId
contentRoutes.get('/users/products/:productId/contents', contentCollection.getProductContentByProductId);

//GET and display the user's all contents
contentRoutes.get('/users/contents', contentCollection.getContents);

module.exports = contentRoutes;