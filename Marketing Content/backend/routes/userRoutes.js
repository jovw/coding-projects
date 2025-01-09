const express = require('express');
const userRoutes = express.Router();
const userCollection = require('../services/userCollection');
const authService = require('../services/authService')


// Apply the authentication middleware globally to all routes in this router
userRoutes.use(authService.handleAuthenticateToken)
//For debug, show all users
userRoutes.post('/users', userCollection.addUser);
//For debug, show all users
userRoutes.get('/users', userCollection.getAllUsers);
//GET and display specific user data on profile page
userRoutes.get('/users/sub', userCollection.getUserBySubHttp);
//POST request to add company data to a specific user
userRoutes.post('/users/company', userCollection.addUserCompany)
//GET and display one user's audience information related to user's products
userRoutes.get('/users/company', userCollection.getUserCompany)

module.exports = userRoutes;