const { Sequelize, DataTypes, Model } = require('sequelize');
const sequelize = require('./dbconfig/sequelize'); 

class Product extends Model {}

Product.init({
    productName: {
        type: DataTypes.STRING,
        allowNull: false,
    },
    productDescription: {
        type: DataTypes.STRING,
        allowNull: false,
    },
}, {
    sequelize,
    modelName: 'Product'
});

module.exports = Product;
