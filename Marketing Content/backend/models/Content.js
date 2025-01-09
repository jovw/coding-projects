const { Sequelize, DataTypes, Model } = require('sequelize');
const sequelize = require('./dbconfig/sequelize');

class Content extends Model { }

Content.init({
    postTitle: {
        type: DataTypes.STRING,
        allowNull: false,
    },
    postCaption: {
        type: DataTypes.STRING,
        allowNull: false,
    },
    image: { //change datatype to string instead of blob
        type: DataTypes.STRING,
        allowNull: true,
    },
    imageDescription: {
        type: DataTypes.STRING,
        allowNull: false,
    }
}, {
    sequelize,
    modelName: 'Content'
});

module.exports = Content;
