const express = require('express');
const productRoutes = express.Router();
const productCollection = require('../services/productCollection');
const authService = require('../services/authService')



// Apply the authentication middleware globally to all routes in this router
productRoutes.use(authService.handleAuthenticateToken)
//POST request to add one user's product
productRoutes.post('/users/products', productCollection.addUserProducts)
//POST request to edit one user's product by id
productRoutes.post('/users/products/:productId', productCollection.editUserProductsById)
//Del request to remove all product
productRoutes.delete('/products', productCollection.deleteAllProducts)
//Del request to remove one user's product by ID
productRoutes.delete('/users/products/:productId', productCollection.deleteUserProductById)
//GET and display all products
productRoutes.get('/products', productCollection.getProducts);
//GET and display one specific user's products on profile page
productRoutes.get('/users/products', productCollection.getUserProducts);
//GET and display one specific user's products by ID on profile page
productRoutes.get('/users/products/:productId', productCollection.getUserProductsById);


module.exports = productRoutes;