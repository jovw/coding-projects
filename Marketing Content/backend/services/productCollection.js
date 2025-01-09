const axios = require('axios');
const User = require('../models/User');
const Product = require('../models/Product');


exports.addUserProducts = async (req, res) => {
    try {
        console.log("addUserProducts", req.user.sub);
        
        // Find the user by their Google sub
        const user = await User.findOne({ where: { googlesub: req.user.sub } });
        
        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }

        // Create the new product associated with the user
        const newProduct = await Product.create({
            productName: req.body.productName,
            productDescription: req.body.productDescription,
            userId: user.id  // Ensure the product is associated with the user
        });

        res.status(200).json(newProduct);
    } catch (error) {
        console.error('Error adding product:', error);
        res.status(500).json({ message: 'Server error while adding product.' });
    }
};

exports.editUserProductsById = async (req, res) => {
    try {
        const user = await User.findOne({ where: { googlesub: req.user.sub } });
    
        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }
    
        const productId = req.params.productId;
        const product = await Product.findOne({ where: { id: productId, userId: user.id } });
    
        if (!product) {
            return res.status(404).json({ message: 'Product not found or does not belong to the user' });
        }
    
        const { productName, productDescription } = req.body;
    
        await product.update({
            productName: productName || product.productName, // Keep existing name if not provided
            productDescription: productDescription || product.productDescription // Keep existing description if not provided
        });
    
        res.status(200).json({ message: `Product with ID ${productId} has been updated.`, product });
    } catch (error) {
        console.error('Error updating user product:', error);
        res.status(500).json({ message: 'Server error while updating user product.' });
    }
    
};


exports.deleteAllProducts = async (req, res) => {
    try {
        await Product.destroy({ where: {} });
        res.status(200).json({ message: 'All products have been deleted.' });
    } catch (error) {
        console.error('Error deleting all products:', error);
        res.status(500).json({ message: 'Server error while deleting all products.' });
    }
};

exports.deleteUserProductById = async (req, res) => {
    try {
        const user = await User.findOne({ where: { googlesub: req.user.sub } });

        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }

        const productId = req.params.productId;
        const product = await Product.findOne({ where: { id: productId, userId: user.id } });

        if (!product) {
            return res.status(404).json({ message: 'Product not found or does not belong to the user' });
        }

        await Product.destroy({ where: { id: productId } });
        res.status(200).json({ message: `Product with ID ${productId} has been deleted.` });
    } catch (error) {
        console.error('Error deleting user product:', error);
        res.status(500).json({ message: 'Server error while deleting user product.' });
    }
};



exports.getProducts = async (req, res) => {
    console.log("getProducts")
    Product.findAll().then(products => {
        res.json(products);
    }) 
}

exports.getUserProducts = async (req, res) => {
    try {
        console.log("getUserProducts");
        const user = await User.findOne({
            where: { googlesub: req.user.sub },
            include: { model: Product, as: 'Products' }
        });

        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }
        res.json(user.Products);
    } catch (error) {
        console.error('Error fetching user products:', error);
        res.status(500).json({ message: 'Server error while retrieving products.' });
    }
};

exports.getUserProductsById = async (req, res) => {
    try {
        console.log("getUserProducts");
        const user = await User.findOne({
            where: { googlesub: req.user.sub },
            include: { model: Product, as: 'Products' }
        });

        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }

        const productId = req.params.productId;
        const product = await Product.findOne({ where: { id: productId, userId: user.id } });

        if (!product) {
            return res.status(404).json({ message: 'Product not found or does not belong to the user' });
        }
        res.json(product);
    } catch (error) {
        console.error('Error fetching user products:', error);
        res.status(500).json({ message: 'Server error while retrieving products.' });
    }
};


exports.getProductByIdArg = async (userId, productId) => {
    try {
        console.log("getUserProducts");
        const user = await User.findOne({
            where: { googlesub: userId },
            include: { model: Product, as: 'Products' }
        });

        if (!user) {
            console.error('User not found');
            return null; // Return null or a specific error object
        }

        const product = await Product.findOne({ where: { id: productId, userId: user.id } });

        if (!product) {
            console.error('Product not found or does not belong to the user');
            return null; // Return null or a specific error object
        }

        return product;
    } catch (error) {
        console.error('Error fetching user products:', error);
        throw error; // Or return a specific error object
    }
};