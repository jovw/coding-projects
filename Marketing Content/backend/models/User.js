const { Sequelize, DataTypes, Model } = require('sequelize');
const sequelize = require('./dbconfig/sequelize'); 

class User extends Model {}

User.init({
    firstName: {
        type: DataTypes.STRING,
        allowNull: false,  // Corrected typo here
    },
    lastName: {
        type: DataTypes.STRING,
        allowNull: true,  // Explicitly allowing null if needed
    },
    email: {
        type: DataTypes.STRING,
        allowNull: false,
        unique: true,
    },
    profilePicUrl: {
        type: DataTypes.STRING,
        allowNull: true,  // Explicitly allowing null if needed
    },
    googlesub: {
        type: DataTypes.STRING,
        allowNull: false,
        unique: true,
    },
    companyName: {
        type: DataTypes.STRING,
        allowNull: false,
    },
    companyDescription: {
        type: DataTypes.STRING,
        allowNull: true,  // Explicitly allowing null if needed
    }
}, {
    sequelize,
    modelName: 'User',
});

// Export and Sync
module.exports = User;