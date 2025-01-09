const express = require('express');
const audienceRoutes = express.Router();
const audienceCollection = require('../services/audienceCollection')
const authService = require('../services/authService')


// Apply the authentication middleware globally to all routes in this router
audienceRoutes.use(authService.handleAuthenticateToken)
//POST request to add audience data
audienceRoutes.post('/users/audiences', audienceCollection.addUserAudiences)
//POST request to edit audience data by id
audienceRoutes.post('/users/audiences/:audienceId', audienceCollection.editUserAudiencesById)
//Del request to add one user's product
audienceRoutes.delete('/audiences', audienceCollection.deleteAllAudiences)
//Del request to add one user's product
audienceRoutes.delete('/users/audiences/:audienceId', audienceCollection.deleteUserAudienceById)
//GET and display all audiences
audienceRoutes.get('/audiences', audienceCollection.getAudiences);
//GET and display one user's audience information related to user's products
audienceRoutes.get('/users/audiences', audienceCollection.getUserAudiences)
//GET and display one user's audience by Id
audienceRoutes.get('/users/audiences/:audienceId', audienceCollection.getUserAudiencesById)

module.exports = audienceRoutes;