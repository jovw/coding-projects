const sequelize = require('./sequelize'); // Import the shared instance
const User = require('../User');
const Product = require('../Product');
const Audience = require('../Audience');
const Content = require('../Content');

// Define relationships
User.hasMany(Product, { as: 'Products', foreignKey: 'userId' });
Product.belongsTo(User, { foreignKey: 'userId' });

User.hasMany(Audience, { as: 'Audiences', foreignKey: 'userId' });
Audience.belongsTo(User, { foreignKey: 'userId' });

Product.hasMany(Content, { as: 'Contents', foreignKey: 'productId' });
Content.belongsTo(Product);

// Sync all models
async function syncAll() {
    try {
        await sequelize.sync({ force: false });
        console.log("All models were synchronized successfully.");
    } catch (error) {
        console.error('Unable to sync the database:', error);
    }
}

syncAll();

module.exports = sequelize;
