const { Sequelize, DataTypes, Model } = require('sequelize');
const sequelize = require('./dbconfig/sequelize'); 

class Audience extends Model {}

Audience.init({
    audienceName: {
        type: DataTypes.STRING,
        allowNull: false,  // Corrected typo here
    },
    audienceDescription: {
        type: DataTypes.STRING,
        allowNull: false,  // Corrected typo here
    },
}, {
    sequelize,
    modelName: 'Audience',
});


module.exports = Audience;
